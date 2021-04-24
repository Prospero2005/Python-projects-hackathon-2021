"""
Модуль для работы с классом базы данных
"""

import sqlite3
import hashlib
import os
from config import Config


class Db:
    """
    Класс работы с базой данных
    """

    def __init__(self, dbname: str) -> None:
        """
        Метод инициализирует экземпляр класса Db,
        и создает подключение к базе данных

        :param dbname: имя базы данных. Если не найдено - создается новая.

        :return: None
        """

        if Config.DEBUG: print('Db __init__')
        try:
            self.conn = sqlite3.connect(dbname, check_same_thread=False)
            self.cur = self.conn.cursor()
            self.salt = None
            self._create_table()
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

    def _create_table(self) -> None:
        """
        Метод создает таблицу users, если она не существует

        :return: None
        """

        if Config.DEBUG: print('Db _create_table')
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL,
            password TEXT NOT NULL,
            scores INTEGER DEFAULT 0,
            s_orient TEXT DEFAULT 'H',
            s_level INTEGER DEFAULT 1,
            s_lang TEXT DEFAULT 'EN',
            s_schema TEXT DEFAULT 'light',
            s_msg INTEGER DEFAULT 0);
            """)
        self.conn.commit()

    def _write_into_db(self, query: str, data: tuple) -> None:
        """
        Метод записывает данные в базу данных

        :param query:   текст запроса
        :param data:    кортеж с данными

        :return: None
        """

        if Config.DEBUG: print('Db _write_into_db')
        self.cur.execute(query, data)
        self.conn.commit()

    def _generate_hash(self, password: bytes, salt: bytes) -> bytes:
        """
        Метод генерирует шифрованный пароль

        :param password: пароль, который нужно зашифровать
        :param salt:     соль

        :return:
                Возвращает зашифрованный пароль в виде хеш-ключа
        """

        if Config.DEBUG: print('Db _generate_hash')
        return hashlib.pbkdf2_hmac('sha256', password, salt, 100000)

    def check_login_in_base(self, login: str) -> bool:
        """
        Метод проверяет наличие пользователя в базе

        :param login: логин пользователя, который нужно проверить

        :return:
            Возвращает True, если пользователь найден, и False, если пользователя нет в базе. 
        """

        sql = "SELECT login FROM users WHERE login=?;"
        self.cur.execute(sql, (login,))
        user_data = self.cur.fetchone()
        if user_data:
            return user_data
        return False

    def check_user_auth(self, login: str, password: str) -> bool:
        """
        Метод аутентификации пользователя, проверяет логин и пароль.
        Логин ищется в базе, если находится. сверяются хешированные пароли.

        :param login:    логин пользователя, который нужно проверить
        :param password: пароль пользователя

        :return:
            Если пользователь аутентифицирован, возвращает данные пользователя, 
            если аутентификация не пройдена - возвращает False. 
        """

        if Config.DEBUG: print('Db check_user_auth')
        sql = "SELECT * FROM users WHERE login=?;"
        self.cur.execute(sql, (login,))
        user_data = self.cur.fetchone()
        if user_data:
            salt = user_data[2][:32]
            pswd = self._generate_hash(password.encode('utf-8'), salt)
            if (login == user_data[1]) and (salt + pswd) == user_data[2]:
                return user_data
        return False

    def add_into_base(self, login: str, password: str) -> None:
        """
        Метод добавляет пользователя в базу при регистрации
        
        :param login:    логин пользователя
        :param password: пароль пользователя

        :return: None
        """

        if Config.DEBUG: print('Db add_into_base')
        self.salt = os.urandom(32)
        pswd = self._generate_hash(password.encode('utf-8'), self.salt)
        sql = "INSERT INTO users (login, password) VALUES(?, ?);"
        self._write_into_db(sql, (login, self.salt+pswd))

    def update_user_data(self, usr: str, scrs: int, vh: str,
                         lvl: int, lng: str, schm: str, msg: int) -> None:
        """
        Метод заносит в базу данные пользователя при изменении настроек или игровых значений

        :param: usr:    логин пользователя
        :param: scrs:   количество очков
        :param: vh:     ориентация окна
        :param: lvl:    уровень игры
        :param: lng:    язык символов
        :param: schm:   тема оформления интерфейса
        :param: msg:    Признак показа сообщений

        :return: None
        """

        if Config.DEBUG: print('Db update_user_data')
        sql = "UPDATE users SET scores=?, s_orient=?, s_level=?, s_lang=?, s_schema=?, s_msg=? WHERE login=?"
        user_data = (scrs, vh, lvl, lng, schm, msg, usr)
        self._write_into_db(sql, user_data)
