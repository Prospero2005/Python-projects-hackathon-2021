"""
Модуль для работы с классом окна авторизации / регистрации
"""

import tkinter as tk
from config import Config


class LoginDialog:
    """
    Класс работы с окном авторизации / регистрации
    """
    
    def __init__(self, master: object, width: int, height: int, btn_text: str, schema: str) -> None:
        """
        Метод инициализирует экземпляр класса LoginDialog,
        окна авторизации / регистрации пользователя

        :param master: родитель
        :param width: длина окна
        :param height: высота окна
        :param btn_text: текст надписи в зависимости от выбора
        :param schema: тема оформления

        :return: None
        """

        if Config.DEBUG: print('LoginDialog __init__')
        self._master = master
        self._wnd = tk.Toplevel(self._master)
        self._width = width
        self._height = height
        self._btn_text = btn_text
        self._schema = schema
        self._lgn = ''
        self._psw = ''

        self._create_window()

        self._wnd.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._wnd.bind('<Escape>', lambda e: self._on_closing())
        self._wnd.bind('<Return>', lambda e: self._action())
        self._wnd.wait_window()

    def _create_window(self) -> None:
        """
        Метод создает окно авторизации / регистрации

        :return: None
        """

        if Config.DEBUG: print('LoginDialog _create_window')
        self._wnd.wm_title(self._btn_text)
        self._wnd.resizable(False, False)
        self._wnd.grab_set()
        self._create_controls()
        self._apply_schema(self._schema)
        self._center_wnd()
        self._wnd.attributes("-alpha", 0.92)

    def _center_wnd(self) -> None:
        """
        Метод отрисовывает окно в центре экрана

        :return: None
        """

        if Config.DEBUG: print('LoginDialog _center_wnd')
        x = (self._wnd.winfo_screenwidth() // 2) - (self._width // 2)
        y = (self._wnd.winfo_screenheight() // 2) - (self._height // 2)
        self._wnd.geometry("{w}x{h}+{x}+{y}".format(w=self._width, h=self._height, x=x, y=y))
        self._wnd.update_idletasks()

    def _create_controls(self) -> None:
        """
        Метод создает элементы окна

        :return: None
        """

        if Config.DEBUG: print('LoginDialog _create_controls')
        self._lbl_login = tk.Label(self._wnd, text="Логин:", font='arial 12')
        self._lbl_login.grid(row=0, padx=2, pady=2, sticky=tk.W)
        
        self._login = tk.Entry(self._wnd, width=33)
        self._login.focus_set()
        self._login.grid(row=0, column=1, sticky=tk.W)
        
        self._lbl_passwd = tk.Label(self._wnd, text="Пароль:", font='arial 12')
        self._lbl_passwd.grid(row=1, padx=2, pady=2, sticky=tk.W)
        
        self._passwd = tk.Entry(self._wnd, width=33, show="#")
        self._passwd.grid(row=1, column=1, columnspan=2)
        
        self._button_auth = tk.Button(self._wnd, width=10, text=self._btn_text, command=self._action)
        self._button_auth.grid(row=3, column=1, pady=15, sticky=tk.W+tk.E)
        
        self._lbl_error = tk.Label(self._wnd, font='arial 10 bold')
        
        reg_login = self._wnd.register(self._callback_login)
        self._login.config(validate="key", validatecommand=(reg_login, '%P'))
        reg_psswd = self._wnd.register(self._callback_psswd)
        self._passwd.config(validate="key", validatecommand=(reg_psswd, '%P'))
        
    def _callback_psswd(self, text) -> bool:
        """
        Callback-метод для контроля длины текстового поля ввода пароля
        
        :param text: вводимый текст
        
        :return: возвращает True, если длина текста не превышает 32 символа,
                 в этом случае введенный символ отображается в текстовом поле.
                 Если возвращает False - символ не выводится. 
        """
        
        if Config.DEBUG: print('LoginDialog _callback_psswd')
        if len(text) <= 32:
            return True
        return False
    
    def _callback_login(self, text) -> bool:
        """
        Callback-метод для контроля длины текстового поля ввода логина
        
        :param text: вводимый текст
        
        :return: возвращает True, если длина текста не превышает 12 символов,
                 в этом случае введенный символ отображается в текстовом поле.
                 Если возвращает False - символ не выводится. 
        """
        
        if Config.DEBUG: print('LoginDialog _callback_login')
        if len(text) <= 12:
            return True
        return False

    def _apply_schema(self, schema: str) -> None:
        """
        Метод применяет оформление к элементам и форме

        :param schema: выбранная тема оформления

        :return: None
        """

        if Config.DEBUG: print('LoginDialog _apply_schema')
        self._wnd.configure(bg=self._master.schemes[schema]['popup_form']['bg'])

        self._lbl_login.configure(bg=self._master.schemes[schema]['lbl_auth']['bg'],
                                  fg=self._master.schemes[schema]['lbl_auth']['fg'])

        self._login.configure(bg=self._master.schemes[schema]['entry_auth']['bg'],
                              fg=self._master.schemes[schema]['entry_auth']['fg'])

        self._lbl_passwd.configure(bg=self._master.schemes[schema]['lbl_auth']['bg'],
                                  fg=self._master.schemes[schema]['lbl_auth']['fg'])

        self._passwd.configure(bg=self._master.schemes[schema]['entry_auth']['bg'],
                               fg=self._master.schemes[schema]['entry_auth']['fg'])

        self._lbl_error.configure(bg=self._master.schemes[schema]['lbl_err']['bg'],
                                  fg=self._master.schemes[schema]['lbl_err']['fg'])

        self._button_auth.configure(bg=self._master.schemes[schema]['btn_auth']['bg'],
                                    fg=self._master.schemes[schema]['btn_auth']['fg'])

    def _action(self) -> None:
        """
        Метод при нажатии на кнопку записывает в атрибуты экземпляра
        текущие значения и проверяет заполнение полей

        :return: None
        """

        if Config.DEBUG: print('LoginDialog _action')
        lgn = self._login.get()
        psw = self._passwd.get()
        if lgn.lower() == Config.ANONYMOUS.lower():
            self._lbl_error.configure(text="Имя пользователя зарезервировано")
            self._lbl_error.place(relx=.5, rely=.61, anchor="c", width=280, height=21)
            self._wnd.after(1000, lambda: self._lbl_error.place_forget())
            return None
        if lgn == '' or psw == '':
            self._lbl_error.configure(text="Заполните все поля")
            self._lbl_error.place(relx=.5, rely=.61, anchor="c", width=280, height=20)
            self._wnd.after(1000, lambda: self._lbl_error.place_forget())
            return None
        self._lbl_error.place_forget()
        self._lgn = lgn
        self._psw = psw
        self._wnd.destroy()

    def get_auth(self) -> tuple:
        """
        Метод возвращает текущие значения логина и пароля

        :return: возвращает кортеж текущих значений логина и пароля
        """

        if Config.DEBUG: print('LoginDialog get_auth')
        return self._lgn, self._psw

    def _on_closing(self) -> None:
        """
        Метод при закрытии окна по крестику или Escape

        :return: None
        """

        if Config.DEBUG: print('LoginDialog _on_closing')
        self._wnd.destroy()
