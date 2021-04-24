"""
Основной модуль игры
"""

import threading
import time
import os
import json
import random
import tkinter as tk
from tkinter import messagebox
from config import Config
from logindlg import LoginDialog
from settingsdlg import SettingsDialog
from dbfuncs import Db
from schemaedit import SchemaEditor


class Game(tk.Tk):
    """
    Основной класс игры
    """
    
    def __init__(self) -> None:
        """
        Метод инициализирует экземпляр класса Game

        :return: None
        """

        if Config.DEBUG: print('Game __init__')
        super().__init__()
        self.user = Config.ANONYMOUS
        self.level = Config.START_LVL
        self.level_data = Config.LEVELS.get(self.level)
        self.data, self.ignore_register = self.level_data
        self.lang = Config.LANG[0]
        self.total_scores = 0
        self.level_scores = 0
        self.count = 0
        self.show_msg = Config.SHOW_MSG
        self.max_count = Config.MAX_COUNT
        self.orientation = Config.START_ORIENT
        self.schemes = Config.SCHEMES.copy() or {}
        self.schema = Config.SCHEMA
        self.root_win_params = Config.ORIENTATION[self.orientation]
        self.width = self.root_win_params['root_width']
        self.height = self.root_win_params['root_height']
        self.letters = []
        self.first = True
        self.logged = False
        self.finished = False
        self.next_level = False
        self.pause = False
        self.interval = 0
        self.worker = None
        self.login_dialog = None
        self.settings_dialog = None
        self.main_menu = tk.Menu()
        self.user_menu = tk.Menu()

        self.create_interface()
        self.load_schemes()
        self.show_controls(self.orientation)
        self.show_menu(self.main_menu)
        self.db = Db(Config.DBNAME)
        self.new_game()

    def create_interface(self) -> None:
        """
        Метод создает окно и элементы окна

        :return: None
        """

        if Config.DEBUG: print('Game create_interface')

        self.title(Config.TITLE)
        self.resizable(False, False)

        self.btn_start = tk.Button(self, text="Старт", font='TkFixedFont 14', command=self.start)
        self.lbl_user = tk.Label(self, text='', font='arial 13', relief=tk.SUNKEN)
        self.lbl_scores = tk.Label(self, text='0', font='TkFixedFont 15', relief=tk.SUNKEN)
        self.lbl_left_count = tk.Label(self, text=self.max_count, font='TkFixedFont 15', relief=tk.SUNKEN)
        self.lbl_level = tk.Label(self, text='', font='TkFixedFont 15', relief=tk.SUNKEN)
        self.lbl_text = tk.Label(self, text='', font='Courier 22 bold', relief=tk.SUNKEN)
        self.user_input = tk.Entry(self, width=5, font='Courier 22 bold', justify=tk.CENTER)
        self.lbl_status = tk.Label(self, text=Config.TITLE, font='TkFixedFont 10')
        self.disable_controls(False, True)

    def show_controls(self, orientation: str) -> None:
        """
        Метод отрисовывает элементы окна в зависимости от ориентации окна

        :param orientation: ориентация окна

        :return: None
        """

        if Config.DEBUG: print('Game show_controls')
        if orientation == 'H':
            self.btn_start.place(relx=.09, rely=.18, anchor="c", width=80, height=50)
            self.lbl_user.place(relx=.333, rely=.18, anchor="c", width=150, height=50)
            self.lbl_level.place(relx=.625, rely=.18, anchor="c", width=130, height=50)
            self.lbl_scores.place(relx=.832, rely=.18, anchor="c", width=65, height=50)
            self.lbl_left_count.place(relx=.95, rely=.18, anchor="c", width=40, height=50)
            self.lbl_text.place(relx=.5, rely=.5, anchor="c", width=430, height=45)
            self.lbl_text.configure(font='Courier 22 bold')
            self.user_input.place(relx=.5, rely=.78, width=430, anchor="c")
            self.user_input.configure(font='Courier 22 bold')
            self.lbl_status.place(relx=.5, rely=.95, anchor="c", width=self.width, height=25)
            self.lbl_status.place_forget()
            self.title(Config.TITLE)
        else:
            self.btn_start.place(relx=.17, rely=.1, anchor="c", width=80, height=50)
            self.lbl_level.place(relx=.57, rely=.1, anchor="c", width=130, height=50)
            self.lbl_left_count.place(relx=.9, rely=.1, anchor="c", width=40, height=50)
            self.lbl_user.place(relx=.35, rely=.35, anchor="c", width=180, height=50)
            self.lbl_scores.place(relx=.85, rely=.35, anchor="c", width=65, height=50)
            self.lbl_text.place(relx=.5, rely=.6, anchor="c", width=290, height=40)
            self.lbl_text.configure(font='Courier 15 bold')
            self.user_input.place(relx=.5, rely=.8, width=290, anchor="c")
            self.user_input.configure(font='Courier 15 bold')
            self.lbl_status.place(relx=.5, rely=.97, anchor="c", width=self.width, height=20)
            self.title('')
        self.center_wnd()

    def apply_schema(self, schema: str) -> None:
        """
        Метод применяет оформление к элементам и форме

        :param schema: выбранная тема оформления

        :return: None
        """
        
        if Config.DEBUG: print('Game apply_schema')
        if schema not in self.schemes:
            self.schema = Config.SCHEMA
        else:
            self.schema = schema 

        self.configure(bg=self.schemes[self.schema]['main_form']['bg'])

        self.btn_start.configure(bg=self.schemes[self.schema]['btn_start']['bg'],
                                 fg=self.schemes[self.schema]['btn_start']['fg'])

        self.lbl_scores.configure(bg=self.schemes[self.schema]['lbl_scores']['bg'],
                                  fg=self.schemes[self.schema]['lbl_scores']['fg'])
        
        self.lbl_left_count.configure(bg=self.schemes[self.schema]['lbl_level']['bg'],
                                      fg=self.schemes[self.schema]['lbl_level']['fg'])

        self.lbl_user.configure(bg=self.schemes[self.schema]['lbl_user']['bg'],
                                fg=self.schemes[self.schema]['lbl_user']['fg'])

        self.lbl_level.configure(bg=self.schemes[self.schema]['lbl_level']['bg'],
                                 fg=self.schemes[self.schema]['lbl_level']['fg'])

        self.lbl_text.configure(bg=self.schemes[self.schema]['lbl_text'][str(int(self.ignore_register))], fg='white')

        self.user_input.configure(bg=self.schemes[self.schema]['user_input']['bg'],
                                  fg=self.schemes[self.schema]['user_input']['fg'])

        self.lbl_status.configure(bg=self.schemes[self.schema]['lbl_status']['bg'],
                                  fg=self.schemes[self.schema]['lbl_status']['fg'])

    def disable_controls(self, btn: bool, inp: bool, block_menu: bool=None) -> None:
        """
        Метод задает состояние кнопки "Старт", поля ввода символов и меню в процессе игры

        :param btn: состояние кнопки "Старт"
        :param inp: состояние поля ввода символов
        :param block_menu: состояние меню

        :return: None
        """

        if Config.DEBUG: print('Game disable_controls')
        state = ['normal', 'disabled']
        self.btn_start.configure(state=state[btn])
        self.user_input.configure(state=state[inp])
        menu = self.user_menu if self.logged else self.main_menu
        if block_menu is not None:
            menu.entryconfig(1, state=state[block_menu])
            menu.entryconfig(2, state=state[block_menu])

    def center_wnd(self) -> None:
        """
        Метод отрисовывает окно в центре экрана

        :return: None
        """
        
        if Config.DEBUG: print('Game center_wnd')
        x = (self.winfo_screenwidth() // 2) - (self.width // 2)
        y = (self.winfo_screenheight() // 2) - (self.height // 2)
        self.geometry("{w}x{h}+{x}+{y}".format(w=self.width, h=self.height, x=x, y=y))
        self.update_idletasks()

    def set_orientation(self, orientation: str) -> None:
        """
        метод задает ориентацию окна

        :param orientation: ориентация окна

        :return: None
        """

        if Config.DEBUG: print('Game set_orientation')
        self.root_win_params = Config.ORIENTATION[orientation]
        self.width = self.root_win_params['root_width']
        self.height = self.root_win_params['root_height']
        self.show_controls(orientation)

    def load_schemes(self) -> None:
        """
        Метод загружает файлы тем оформления и добавляет их к стандартным темам
        """
        
        if Config.DEBUG: print('Game load_schemes')
        self.schemes.update(self.schemes)
        for file in os.listdir('.'):
            if file.endswith(".json"):
                with open(file, encoding='utf-8') as f:
                    schema = json.load(f)
                    self.schemes.update(schema)
    
    def schema_editor(self) -> None:
        """
        Метод загружает редактор тем оформления, где можно изменить тему
        """
        
        if Config.DEBUG: print('Game schema_editor')
        self.withdraw()
        se = SchemaEditor(self, 590, 520, self.logged)
        schm = se.get_schema()
        self.load_schemes()
        if schm:
            self.schema = schm
            self.apply_schema(self.schema)
        self.deiconify()
        
    def settings(self) -> None:
        """
        Метод показывает окно настроек пользователя и обновляет данные в базе

        :return: None
        """

        if Config.DEBUG: print('Game settings')
        self.disable_controls(True, True)
        self.settings_dialog = SettingsDialog(self, 400, 200, self.user, self.schema)
        self.settings_dialog.set_parameters(self.orientation, self.level, self.lang, self.schema, self.show_msg)
        params = self.settings_dialog.get_values()
        self.orientation, self.level, self.lang, self.schema, self.show_msg = params
        self.db.update_user_data(self.user, self.total_scores, self.orientation,
                                 self.level, self.lang, self.schema, self.show_msg)
        self.init_user()
        if Config.DEBUG: print('params', params)
        self.disable_controls(False, True)

    def show_login(self, btn_text: str) -> LoginDialog:
        """
        Метод возвращает окно авторизации / регистрации пользователя

        :param btn_text: текст для кнопки в зависимости от типа окна (авторизация / регистрация)

        :return: возвращает экземпляр окна авторизации / регистрации пользователя
        """

        if Config.DEBUG: print('Game show_login')
        return LoginDialog(self, 280, 100, btn_text, self.schema)

    def register_user(self) -> None:
        """
        Метод для регистрации нового пользователя

        :return: None
        """

        if Config.DEBUG: print('Game register_user')
        self.disable_controls(True, True)
        self.login_dialog = self.show_login('Регистрация')
        auth_lgn, auth_psw = self.login_dialog.get_auth()
        if Config.DEBUG: print('auth_lgn', auth_lgn, 'auth_psw', auth_psw)
        if auth_lgn and auth_psw:
            result = self.db.check_login_in_base(auth_lgn)
            if not result:
                self.db.add_into_base(auth_lgn, auth_psw)
                if Config.DEBUG: print('register user')
                self.user = auth_lgn
                self.init_user()
                self.show_menu(self.user_menu)
                self.logged = True
            else:
                messagebox.showinfo(message="Пользователь существует")
                if Config.DEBUG: print('auth_lgn', auth_lgn)
        self.disable_controls(False, True)

    def login_user(self) -> None:
        """
        Метод для авторизации пользователя

        :return: None
        """

        if Config.DEBUG: print('Game login_user')
        self.disable_controls(True, True)
        self.login_dialog = self.show_login('Авторизация')
        auth_lgn, auth_psw = self.login_dialog.get_auth()
        if auth_lgn and auth_psw:
            result = self.db.check_user_auth(auth_lgn, auth_psw)
            if result:
                if Config.DEBUG: print(result)
                (_, self.user, _, self.total_scores, self.orientation,
                self.level, self.lang, self.schema, self.show_msg) = result
                self.init_user()
                self.show_menu(self.user_menu)
                self.logged = True
            else:
                messagebox.showinfo(message="Неверный логин или пароль")
        self.disable_controls(False, True)

    def logout_user(self) -> None:
        """
        Метод для выхода пользователя из учетной записи

        :return: None
        """

        if Config.DEBUG: print('Game logout_user')
        self.db.update_user_data(self.user, self.total_scores, self.orientation,
                                 self.level, self.lang, self.schema, self.show_msg)
        self.logged = False
        self.user = Config.ANONYMOUS
        self.level = Config.START_LVL
        self.orientation = Config.START_ORIENT
        self.schema = Config.SCHEMA
        self.total_scores = 0
        self.show_msg = False
        self.disable_controls(False, True)
        self.init_user()
        self.show_menu(self.main_menu)

    def init_user(self) -> None:
        """
        Метод для инициализации настроек пользователя

        :return: None
        """
        
        if Config.DEBUG: print('Game init_user')
        self.btn_start.configure(text='Старт')
        self.lbl_user.configure(text=self.user)
        self.lbl_scores.configure(text=f'{self.total_scores}')
        self.lbl_level.configure(text=f'Уровень: {self.level}')
        self.lbl_left_count.configure(text=self.max_count)
        self.lbl_text.configure(text='')
        self.user_input.delete(0, tk.END)
        self.set_orientation(self.orientation)
        self.level_data = Config.LEVELS.get(self.level)
        if self.level_data is not None:
            self.data, self.ignore_register = self.level_data
        self.apply_schema(self.schema)

    def create_common_menu(self) -> None:
        """
        Метод для создания общих пунктов меню

        :return: None
        """

        if Config.DEBUG: print('Game create_common_menu')
        self.submenu.add_command(label="Редактор тем", command=self.schema_editor)
        self.submenu.add_separator()
        self.submenu.add_command(label="Новая игра", command=self.new_game)
        self.submenu.add_separator()
        self.submenu.add_command(label="Закрыть", command=self.goodbye)

    def create_user_menu(self) -> None:
        """
        Метод для создания пунктов меню авторизированного пользователя

        :return: None
        """
        
        if Config.DEBUG: print('Game create_user_menu')
        self.submenu = tk.Menu(self.user_menu, tearoff=0)
        self.user_menu.add_cascade(label='Mеню', menu=self.submenu)
        self.submenu.delete(0, 7)
        self.submenu.add_command(label="Выход", command=self.logout_user)
        self.submenu.add_command(label="Настройки", command=self.settings)
        self.create_common_menu()

    def create_standart_menu(self) -> None:
        """
        Метод для создания пунктов меню неавторизированного пользователя

        :return: None
        """

        if Config.DEBUG: print('Game create_standart_menu')
        self.submenu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label='Mеню', menu=self.submenu)
        self.submenu.delete(0, 7)
        self.submenu.add_command(label="Регистрация", command=self.register_user)
        self.submenu.add_command(label="Логин", command=self.login_user)
        self.create_common_menu()

    def show_menu(self, menu: tk.Menu) -> None:
        """
        Метод для отображения меню пользователя

        :param menu: меню пользователя

        :return: None
        """

        if Config.DEBUG: print('Game show_menu')
        self.config(menu=menu)
        menu.delete(0, 2)
        if menu == self.user_menu:
            self.create_user_menu()
        else:
            self.create_standart_menu()
        menu.add_command(label='О программе', command=self.about)

    def init_game(self) -> None:
        """
        Метод для инициализации игры

        :return: None
        """

        if Config.DEBUG: print('Game init_game')
        if not self.next_level and not self.pause:
            self.lbl_scores.configure(text='0')
        self.lbl_text.configure(text='')
        self.lbl_left_count.configure(text=self.max_count)

        self.letters = []
        self.first = True
        self.finished = False
        self.next_level = False
        self.count = 0

    def new_game(self) -> None:
        """
        Метод для инициализации новой игры

        :return: None
        """

        if Config.DEBUG: print('Game new_game')
        new_game = True
        if self.show_msg:
            new_game = messagebox.askokcancel("Внимание!", "Уровень и очки будут сброшены!")
        if new_game:
            self.level = Config.START_LVL
            self.total_scores = 0
            self.level_scores = 0
            self.init_user()
            if self.logged:
                self.db.update_user_data(self.user, self.total_scores, self.orientation,
                                         self.level, self.lang, self.schema, self.show_msg)
        self.disable_controls(False, True, False)

    def start(self) -> None:
        """
        Метод для обработки запуска игры

        :return: None
        """
        
        if Config.DEBUG: print('Game start')
        if self.worker:
            if Config.DEBUG: print('worker.is_alive in start', self.worker.is_alive())
        self.init_game()
        self.disable_controls(True, False, True)
        self.init_user()
        if self.level_data and not self.level_data[1] and self.show_msg:
            messagebox.showwarning("Внимание!", "Следующий уровень регистрозависимый!")
        self.worker = threading.Thread(target=self.timer, daemon=True)
        self.worker.start()

    def set_interval(self) -> None:
        """
        Метод для установки интервала в зависимости от уровня

        :return: None
        """

        if Config.DEBUG: print('Game set_interval')
        text = ''.join(self.letters)
        if self.level in (1, 2):
            self.interval = len(text) + 1
        elif self.level in (3, 4, 5):
            self.interval = len(text) + 2
        elif self.level in (6, 7):
            self.interval = len(text) + int(not self.ignore_register)
        else:
            self.interval = int((len(text) + int(not self.ignore_register)) * 0.7)

    def set_scores(self) -> None:
        """
        Метод для начисления и отображения очков

        :return: None
        """

        if Config.DEBUG: print('Game set_count')
        self.level_scores = int(self.lbl_scores['text']) + len(self.letters) * (self.level // 2) + self.level
        self.lbl_scores.configure(text=self.level_scores)
        self.count += 1
        self.lbl_left_count.configure(text=self.max_count - self.count)

    def defeat(self) -> None:
        """
        Метод для обработки проигрыша в игре

        :return: None
        """

        if Config.DEBUG: print('Game defeat')
        if not self.finished:
            self.lbl_text.configure(bg='red')
            messagebox.showerror(message="Вы проиграли!")
            self.disable_controls(False, True, False)
            self.finished = True
            if self.user == Config.ANONYMOUS:
                self.level = Config.START_LVL
                self.total_scores = 0
            self.worker.do_run = False

    def check_equal(self) -> None:
        """
        Метод для обработки сравнения строки пользователя и шаблона

        :return: None
        """

        if Config.DEBUG: print('Game check_equal')
        text = ''.join(self.letters)
        user_text = self.user_input.get()
        if Config.DEBUG: print('level', self.level, 'data', self.level_data)
        if self.ignore_register:
            text = text.upper()
            user_text = user_text.upper()
        if text == user_text and user_text:
            self.set_scores()
        else:
            if not self.first:
                self.defeat()
            self.first = False

    def check_finish(self) -> None:
        """
        Метод для обработки проверки конца уровня в игре

        :return: None
        """

        if Config.DEBUG: print('Game check_finish')
        if self.count == self.max_count:
            self.finished = True
            self.user_input.delete(0, tk.END)
            messagebox.showinfo(message="ПОБЕДА!")
            if self.level < 8:
                self.next_level = messagebox.askyesno(message="Продолжаем?")
            if self.level < 8 and not self.next_level:
                self.btn_start.configure(text='Пауза')
            self.total_scores = self.level_scores
            self.level_scores = 0
            if not self.next_level:
                self.level += 1
                self.set_interval()
                self.pause = True
                self.worker.do_run = False
                self.disable_controls(self.level > 8, True, False)
            if self.level > 8:
                messagebox.showinfo(message="ИГРА ОКОНЧЕНА!")
                self.level -= 1
            if self.logged:
                self.db.update_user_data(self.user, self.total_scores, self.orientation,
                                         self.level, self.lang, self.schema, self.show_msg)
        if Config.DEBUG: print('self.finished', self.finished)
        self.update_idletasks()

    def get_new_word(self) -> None:
        """
        Метод для получения очередного текста шаблона в игре

        :return: None
        """

        if Config.DEBUG: print('Game get_new_word')
        self.letters = []
        if Config.DEBUG: print('get_new_word', self.level, self.level_data)
        for _ in range(self.level):
            char = random.choice(self.data[self.lang])
            if not self.ignore_register:
                tmp = []
                for c in char:
                    up_low = random.choice([c.lower, c.upper])
                    tmp.append(up_low())
                char = ''.join(tmp)
            self.letters.append(char)
            if self.level > 5:
                break
        self.set_interval()

    def check_word(self) -> None:
        """
        Метод для обработки проверки данных и окончания игры

        :return: None
        """

        if Config.DEBUG: print('Game check_word')
        self.check_equal()
        self.check_finish()
        if not self.finished:
            self.get_new_word()

    def timer(self) -> None:
        """
        Метод для обработки логики в игре

        :return: None
        """

        if Config.DEBUG: print('Game timer')
        if Config.DEBUG: print('next_level', self.next_level)
        if Config.DEBUG: print('self.interval', self.interval)
        while getattr(self.worker, "do_run", True):
            if Config.DEBUG: print('threading.active_count()', threading.active_count())
            self.user_input.focus()
            self.check_word()
            self.lbl_text.configure(text=''.join(self.letters))
            self.user_input.delete(0, tk.END)
            if not self.finished:
                time.sleep(self.interval)

            if self.next_level:
                self.worker.do_run = False

        if self.next_level:
            if Config.DEBUG: print('is_alive in timer', self.worker.is_alive())
            self.level += 1
            self.level_data = Config.LEVELS.get(self.level)
            if Config.DEBUG: print('self.level_data', self.level_data)
            if self.level_data is not None:
                self.set_interval()
                self.lbl_level.configure(text=f'Уровень: {self.level}')
                self.data, self.ignore_register = self.level_data
                if Config.DEBUG: print('self.level', self.level, 'self.interval', self.interval)
                self.start()
            else:
                messagebox.showinfo(message="ИГРА ОКОНЧЕНА!")
                self.disable_controls(True, True, False)

    def about(self) -> None:
        """
        Метод для вывода окна "О программе"

        :return: None
        """

        if Config.DEBUG: print('Game about')
        if self.worker and self.worker.is_alive():
            return None
        
        d1 = '{:->32}'.format('Дмитрий Бурса (@Prospero2005)')
        d2 = '{:->31}'.format('Сергей (@Posegrey)')
        d3 = '{:->23}'.format('Lenz (@Lenz_Gardfild)')
        d4 = '{:->20}'.format('Denis (@quqpup)')
        messagebox.showinfo("О программе",
                            "Игра 'Клавиатурный тренажер' (Версия 1.0)\n"
                            "Создана в рамках проекта 'МиниХакатон-2021'\n"
                            "(Телеграмм: https://t.me/pythonhackaton1)\n\n"
                            "Идея, логика, сборка {d1}\n\n"
                            "База данных {d2}\n\n"
                            "Подбор данных, тесты {d3}\n\n"
                            "Интерфейс, отладка {d4}".format(d1=d1, d2=d2, d3=d3, d4=d4))

    def goodbye(self) -> None:
        """
        Метод для обработки выхода и завершения игры

        :return: None
        """

        if Config.DEBUG: print('Game goodbye')
        self.db.cur.close()
        self.db.conn.close()
        self.quit()


if __name__ == '__main__':
    root = Game()
    root.mainloop()
