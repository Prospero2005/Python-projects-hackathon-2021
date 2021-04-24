"""
Модуль для работы с классом окна настроек
"""

import tkinter as tk
from tkinter import messagebox, ttk
from config import Config


class SettingsDialog:
    """
    Класс работы с окном настроек
    """    
    
    def __init__(self, master: object, width: int, height: int, user: str, schema: str) -> None:
        """
        Метод инициализирует экземпляр класса SettingsDialog, настроек игры

        :param master: родитель
        :param width:  длина окна
        :param height: высота окна
        :param user:   пользователь
        :param schema: тема оформления

        :return: None
        """

        if Config.DEBUG: print('SettingsDialog __init__')
        self._master = master
        self._wnd = tk.Toplevel(self._master)
        self._width = width
        self._height = height
        self._user = user
        self._orh_val = 0
        self._orv_val = 1
        self._rb_var = tk.IntVar()
        self._chk_var = tk.IntVar()
        self._orient = {0: 'H', 1: 'V'}
        self._langs = {'Английский': 'EN', 'Русский': 'RU'}
        self._schemes = {nm.get('name', 'Без имени'): schm  for (schm, nm) in self._master.schemes.items()}
        self._schema = schema
        self._show_msg = False
        self.style = ttk.Style()
        self._vh = None
        self._lvl = None
        self._lng = None
        self._schm = None

        self._wnd.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._wnd.bind('<Escape>', lambda e: self._on_closing())
        self._wnd.bind('<Return>', lambda e: self._action())

        self._create_window()

    def _create_window(self) -> None:
        """
        Метод создает окно настроек

        :return: None
        """

        if Config.DEBUG: print('SettingsDialog _create_window')
        self._wnd.wm_title("Настройки")
        self._wnd.resizable(False, False)
        self._wnd.grab_set()
        self._create_controls()
        self._apply_schema(self._schema)
        self._center_wnd()
        self._wnd.attributes("-alpha", 0.94)

    def _create_controls(self) -> None:
        """
        Метод создает элементы окна настроек

        :return: None
        """

        if Config.DEBUG: print('SettingsDialog _create_controls')
        
        self._init_ttk_style(self._schema)
        
        self._gb_orbox = tk.LabelFrame(self._wnd, text='Ориентация')

        self._rb_orh = tk.Radiobutton(self._gb_orbox, text="Горизонтально", font='arial 10 bold',
                                      variable=self._rb_var, value=self._orh_val, command=self._get_vh_value)

        self._rb_orv = tk.Radiobutton(self._gb_orbox, text="Вертикально", font='arial 10 bold',
                                      variable=self._rb_var, value=self._orv_val, command=self._get_vh_value)

        self._gb_lvlbox = tk.LabelFrame(self._wnd, text='Выбор уровня')
        
        self._cb_lvl = ttk.Combobox(self._wnd, state="readonly", height=2,  font='arial 11 bold',
                                    values=['Уровень 1', 'Уровень 2', 'Уровень 3', 'Уровень 4',
                                            'Уровень 5', 'Уровень 6', 'Уровень 7', 'Уровень 8'],
                                    style='S.TCombobox')

        self._gb_lngbox = tk.LabelFrame(self._wnd, text='Выбор языка')

        self._cb_lng = ttk.Combobox(self._wnd, state="readonly",  font='arial 10 bold',
                                    values=['Английский', 'Русский'], style='S.TCombobox')

        self._gb_schmbox = tk.LabelFrame(self._wnd, text='Выбор темы')

        self._cb_schm = ttk.Combobox(self._wnd, height=2, state="readonly", font='arial 11 bold',
                                     values=list(self._schemes.keys()),style='S.TCombobox')

        self._chk_show_msg = ttk.Checkbutton(self._wnd, variable=self._chk_var, style='S.TCheckbutton',
                                             text="Предупреждать о новой игре и регистрозависимом уровне")

        self._btn_ok = tk.Button(self._wnd, text='OK', command=self._action)

    def _show_controls(self) -> None:
        """
        Метод отрисовывает элементы окна настроек

        :return: None
        """

        if Config.DEBUG: print('SettingsDialog _show_controls')
        self._gb_orbox.place(relx=.02, rely=.27, width=140, height=100, anchor="w")
        self._rb_orh.place(relx=.99, rely=.2, width=129, height=25, anchor="e")
        self._rb_orv.place(relx=.94, rely=.7, width=127, height=25, anchor="e")
        self._gb_lvlbox.place(relx=.4, rely=.14, width=110, height=50, anchor="w")
        self._cb_lvl.place(relx=.66, rely=.17, width=100, height=25, anchor="e")
        self._gb_lngbox.place(relx=.69, rely=.14, width=110, height=50, anchor="w")
        self._cb_lng.place(relx=.95, rely=.17, width=100, height=25, anchor="e")
        self._gb_schmbox.place(relx=.4, rely=.4, width=225, height=50, anchor="w")
        self._cb_schm.place(relx=.94, rely=.43, width=210, height=25, anchor="e")
        self._chk_show_msg.place(relx=.9, rely=.63, width=350, height=25, anchor="e")
        self._btn_ok.place(relx=.88, rely=.85, anchor="c", width=75, height=35)
        self._wnd.update()
        self._wnd.wait_window()

    def _init_ttk_style(self, schema: dict) -> None:
        """
        Метод задает стили для элементов из класса ttk

        :param schema: выбранная тема оформления

        :return: None
        """

        if Config.DEBUG: print('SettingsDialog _init_ttk_style')

        self.style.configure('S.TCombobox', background=self._master.schemes[schema]['cb_sett']['bg'],
                                            foreground=self._master.schemes[schema]['cb_sett']['fg'])

        self.style.configure('S.TCheckbutton', background=self._master.schemes[schema]['box_sett']['bg'],
                                               foreground=self._master.schemes[schema]['box_sett']['fg'])
        
    def _apply_schema(self, schema: str) -> None:
        """
        Метод применяет оформление к элементам и форме

        :param schema: выбранная тема оформления

        :return: None
        """

        if Config.DEBUG: print('SettingsDialog _apply_schema')
        self._wnd.configure(bg=self._master.schemes[schema]['popup_form']['bg'])

        self._gb_orbox.configure(bg=self._master.schemes[schema]['box_sett']['bg'],
                                 fg=self._master.schemes[schema]['box_sett']['fg'])
        self._rb_orh.configure(bg=self._master.schemes[schema]['rb_sett']['bg'],
                               fg=self._master.schemes[schema]['rb_sett']['fg'])
        self._rb_orv.configure(bg=self._master.schemes[schema]['rb_sett']['bg'],
                               fg=self._master.schemes[schema]['rb_sett']['fg'])

        self._gb_lvlbox.configure(bg=self._master.schemes[schema]['box_sett']['bg'],
                                  fg=self._master.schemes[schema]['box_sett']['fg'])
        self._gb_lngbox.configure(bg=self._master.schemes[schema]['box_sett']['bg'],
                                  fg=self._master.schemes[schema]['box_sett']['fg'])
        self._gb_schmbox.configure(bg=self._master.schemes[schema]['box_sett']['bg'],
                                   fg=self._master.schemes[schema]['box_sett']['fg'])

        self._btn_ok.configure(bg=self._master.schemes[schema]['btn_sett']['bg'],
                               fg=self._master.schemes[schema]['btn_sett']['fg'])

    def _center_wnd(self) -> None:
        """
        Метод отрисовывает окно в центре экрана

        :return: None
        """

        if Config.DEBUG: print('SettingsDialog _center_wnd')
        x = (self._wnd.winfo_screenwidth() // 2) - (self._width // 2)
        y = (self._wnd.winfo_screenheight() // 2) - (self._height // 2)
        self._wnd.geometry("{w}x{h}+{x}+{y}".format(w=self._width, h=self._height, x=x, y=y))
        self._wnd.update_idletasks()
        self._wnd.focus_set()

    def set_parameters(self, vh: str, lvl: int, lng: str, schm: str, show_msg: bool) -> None:
        """
        Метод выставляет параметры пользователя при открытии окна настроек

        :param vh: ориентация окна
        :param lvl: уровень игры
        :param lng: язык символов
        :param schm: тема оформления
        :param show_msg: признак показа сообщений

        :return: None
        """

        if Config.DEBUG: print('SettingsDialog set_parameters')
        orient = {'H': 0, 'V': 1}
        lang = {'EN': 'Английский', 'RU': 'Русский'}
        schemes = {schema: name.get('name', 'Без имени') for (schema, name) in self._master.schemes.items()}

        self._vh = vh
        self._lvl = lvl
        self._lng = lng
        self._schema = schm
        self._show_msg = show_msg

        self._rb_var.set(orient.get(self._vh, 0))
        self._cb_lvl.set('Уровень ' + str(self._lvl))
        self._cb_lng.set(lang.get(self._lng, 'Английский'))
        self._cb_schm.set(schemes.get(self._schema))
        
        self._chk_var.set(self._show_msg)
        self._show_controls()

    def _action(self) -> None:
        """
        Метод при нажатии на кнопку записывает в атрибуты экземпляра текущие значения

        :return: None
        """

        if Config.DEBUG: print('SettingsDialog _action')
        self._vh = self._orient.get(self._rb_var.get(), 'H')
        self._lvl = int(self._cb_lvl.get().split()[1])
        self._lng = self._langs.get(self._cb_lng.get(), 'EN')
        self._schema = self._schemes.get(self._cb_schm.get(), 'light')
        self._show_msg = self._chk_var.get()
        self._wnd.destroy()

    def get_values(self) -> tuple:
        """
        Метод возвращает в кортеже из настроек пользователя текущие значения

        :return: Возвращает кортеж из настроек пользователя
        """

        if Config.DEBUG: print('SettingsDialog get_values')
        return self._vh, self._lvl, self._lng, self._schema, self._show_msg

    def _get_vh_value(self) -> None:
        """
        Метод получает новую ориентацию окна при изменении выбора

        :return: None
        """

        if Config.DEBUG: print('SettingsDialog _get_vh_value')
        self._vh = self._orient.get(self._rb_var.get(), 0)
    
    def _on_closing(self) -> None:
        """
        Метод при закрытии окна по крестику или Escape

        :return: None
        """

        if Config.DEBUG: print('SettingsDialog _on_closing')
        self._wnd.destroy()
