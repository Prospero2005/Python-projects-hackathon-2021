"""
Модуль для работы с классом окна редактора тем оформления
"""

import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
import json
from config import Config


class SchemaEditor:
    """
    Класс работы с редактором тем оформления
    """
    
    def __init__(self, master: object, width: int, height: int, logged: bool) -> None:
        """
        Метод инициализирует экземпляр класса SchemaEditor,

        :param master: родитель
        :param width:  длина окна
        :param height: высота окна
        :param logged: признак зарегистрированного пользователя

        :return: None
        """
        
        if Config.DEBUG: print('SchemaEditor __init__')
        self._master = master
        self._wnd = tk.Toplevel(self._master)
        self._width = width
        self._height = height
        self._schemes = self._master.schemes
        self._loaded = False
        self._logged = logged
        self._schema = None
        self._e_name = tk.StringVar()
        self._e_alias = tk.StringVar()
        self._colorchooser = None
        self._changed = False
        
        self._create_window()
                
        self._wnd.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._wnd.bind('<Escape>', lambda e: self._on_closing())
        self._wnd.bind('<Button>', self._on_click)
        
        self._wnd.wait_window()
        
    
    def _create_window(self) -> None:
        """
        Метод создает окно редактора тем оформления

        :return: None
        """

        if Config.DEBUG: print('SchemaEditor _create_window')
        self._wnd.wm_title("Редактор тем оформления")
        self._wnd.resizable(False, False)
        self._wnd.grab_set()
        self._create_controls()
        self._center_wnd()
    
    def _create_controls(self) -> None:
        """
        Метод создает элементы окна редактора
        
        :return: None
        """

        if Config.DEBUG: print('SchemaEditor _create_controls')
        
        state_controls = ['disabled', 'normal']
        
        self._lbl_schema = tk.Label(self._wnd, text="Выберите тему оформления >", font='arial 11')
        self._lbl_schema.grid(row=0, column=0, columnspan=2, padx=8, pady=4, sticky=tk.W)
        
        self._cb_schm = ttk.Combobox(self._wnd, width=15, height=2, state="readonly",
                                     font='arial 12 bold', values=list(self._schemes.keys()))
        self._cb_schm.grid(row=0, column=2, columnspan=3, padx=5, pady=5, sticky=tk.W+tk.E)
        self._btn_edit = tk.Button(self._wnd, text="Редактировать тему", width=15, command=self._edit_schema)
        self._btn_edit.grid(row=0, column=5, padx=10, pady=5, sticky=tk.W+tk.E)      
        
        self._gb_main = tk.LabelFrame(self._wnd, text="Оформление:", font='arial 10')
        self._gb_main.grid(row=1, columnspan=6, padx=8, pady=4)
      
        self._gb_zero = tk.LabelFrame(self._gb_main, font='arial 10')
        self._gb_zero.grid(row=0, columnspan=6, padx=5, pady=3, sticky=tk.W + tk.E)
        self._lbl_schema_name = tk.Label(self._gb_zero, text="Название темы:", font='arial 10')
        self._lbl_schema_name.grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)       
        self._schema_name = tk.Entry(self._gb_zero, textvariable=self._e_name, width=25)
        self._schema_name.grid(row=0, column=1, padx=5, sticky=tk.W)
        self._lbl_schema_alias = tk.Label(self._gb_zero, text="Псевдоним:", font='arial 10')
        self._lbl_schema_alias.grid(row=0, column=2, padx=5, pady=3, sticky=tk.W)
        self._schema_alias = tk.Entry(self._gb_zero, textvariable=self._e_alias, width=30)
        self._schema_alias.grid(row=0, column=3, padx=5, sticky=tk.W)  
         
        self._gb_main_form = tk.LabelFrame(self._gb_main, text="Основная форма", font='arial 10')
        self._gb_main_form.grid(row=1, column=0, padx=5, pady=3)
        self._lbl_main_form_bg = tk.Label(self._gb_main_form, text="Фон:", font='arial 10')
        self._lbl_main_form_bg.grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        self._main_form_bg = tk.Label(self._gb_main_form, textvariable='_main_form_bg',
                                      font='arial 10', width=3, relief=tk.RAISED)
        self._main_form_bg.grid(row=0, column=1, padx=5, sticky=tk.W)
        self._lbl_main_form_fg = tk.Label(self._gb_main_form, text="Текст:", font='arial 10')
        self._lbl_main_form_fg.grid(row=0, column=2, padx=5, pady=3, sticky=tk.W)
        self._main_form_fg = tk.Label(self._gb_main_form, textvariable='_main_form_fg',
                                      font='arial 10', width=3, relief=tk.RAISED)
        self._main_form_fg.grid(row=0, column=3, padx=5, sticky=tk.W)
         
        self._gb_popup_form = tk.LabelFrame(self._gb_main, text="Доп. формы", font='arial 10')
        self._gb_popup_form.grid(row=1, column=1, padx=5, pady=3)
        self._lbl_popup_form_bg = tk.Label(self._gb_popup_form, text="Фон:", font='arial 10')
        self._lbl_popup_form_bg.grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        self._popup_form_bg = tk.Label(self._gb_popup_form, textvariable='_popup_form_bg',
                                       font='arial 10', width=3, relief=tk.RAISED)
        self._popup_form_bg.grid(row=0, column=1, padx=5, sticky=tk.W)
        self._lbl_popup_form_fg = tk.Label(self._gb_popup_form, text="Текст:", font='arial 10')
        self._lbl_popup_form_fg.grid(row=0, column=2, padx=5, pady=3, sticky=tk.W)
        self._popup_form_fg = tk.Label(self._gb_popup_form, textvariable='_popup_form_fg',
                                       font='arial 10', width=3, relief=tk.RAISED)
        self._popup_form_fg.grid(row=0, column=3, padx=5, sticky=tk.W)
         
        self._gb_btn_start = tk.LabelFrame(self._gb_main, text="Кнопка 'Старт'", font='arial 10')
        self._gb_btn_start.grid(row=1, column=2, padx=5, pady=3)
        self._lbl_btn_start_bg = tk.Label(self._gb_btn_start, text="Фон:", font='arial 10')
        self._lbl_btn_start_bg.grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        self._btn_start_bg = tk.Label(self._gb_btn_start, textvariable='_btn_start_bg',
                                      font='arial 10', width=3, relief=tk.RAISED)
        self._btn_start_bg.grid(row=0, column=1, padx=5, sticky=tk.W)
        self._lbl_btn_start_fg = tk.Label(self._gb_btn_start, text="Текст:", font='arial 10')
        self._lbl_btn_start_fg.grid(row=0, column=2, padx=5, pady=3, sticky=tk.W)
        self._btn_start_fg = tk.Label(self._gb_btn_start, textvariable='_btn_start_fg',
                                      font='arial 10', width=3, relief=tk.RAISED)
        self._btn_start_fg.grid(row=0, column=3, padx=5, sticky=tk.W)
      
        self._gb_scores = tk.LabelFrame(self._gb_main, text="Очки", font='arial 10')
        self._gb_scores.grid(row=2, column=0, padx=5, pady=3)
        self._lbl_scores_bg = tk.Label(self._gb_scores, text="Фон:", font='arial 10')
        self._lbl_scores_bg.grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        self._scores_bg = tk.Label(self._gb_scores, textvariable='_scores_bg',
                                   font='arial 10', width=3, relief=tk.RAISED)
        self._scores_bg.grid(row=0, column=1, padx=5, sticky=tk.W)
        self._lbl_scores_fg = tk.Label(self._gb_scores, text="Текст:", font='arial 10')
        self._lbl_scores_fg.grid(row=0, column=2, padx=5, pady=3, sticky=tk.W)
        self._scores_fg = tk.Label(self._gb_scores, textvariable='_scores_fg',
                                   font='arial 10', width=3, relief=tk.RAISED)
        self._scores_fg.grid(row=0, column=3, padx=5, sticky=tk.W)

        self._gb_user = tk.LabelFrame(self._gb_main, text="Имя пользователя", font='arial 10')
        self._gb_user.grid(row=2, column=1, padx=5, pady=3)
        self._lbl_user_bg = tk.Label(self._gb_user, text="Фон:", font='arial 10')
        self._lbl_user_bg.grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        self._user_bg = tk.Label(self._gb_user, textvariable='_user_bg',
                                 font='arial 10', width=3, relief=tk.RAISED)
        self._user_bg.grid(row=0, column=1, padx=5, sticky=tk.W)
        self._lbl_user_fg = tk.Label(self._gb_user, text="Текст:", font='arial 10')
        self._lbl_user_fg.grid(row=0, column=2, padx=5, pady=3, sticky=tk.W)
        self._user_fg = tk.Label(self._gb_user, textvariable='_user_fg',
                                 font='arial 10', width=3, relief=tk.RAISED)
        self._user_fg.grid(row=0, column=3, padx=5, sticky=tk.W)
         
        self._gb_level = tk.LabelFrame(self._gb_main, text="Уровень", font='arial 10')
        self._gb_level.grid(row=2, column=2, padx=5, pady=3)
        self._lbl_level_bg = tk.Label(self._gb_level, text="Фон:", font='arial 10')
        self._lbl_level_bg.grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        self._level_bg = tk.Label(self._gb_level, textvariable='_level_bg',
                                  font='arial 10', width=3, relief=tk.RAISED)
        self._level_bg.grid(row=0, column=1, padx=5, sticky=tk.W)
        self._lbl_level_fg = tk.Label(self._gb_level, text="Текст:", font='arial 10')
        self._lbl_level_fg.grid(row=0, column=2, padx=5, pady=3, sticky=tk.W)
        self._level_fg = tk.Label(self._gb_level, textvariable='_level_fg',
                                  font='arial 10', width=3, relief=tk.RAISED)
        self._level_fg.grid(row=0, column=3, padx=5, sticky=tk.W)

        self._gb_text = tk.LabelFrame(self._gb_main, text="Текст шаблона", font='arial 10')
        self._gb_text.grid(row=3, columnspan=6, padx=5, pady=3, sticky=tk.W + tk.E)
        self._lbl_text_bg0 = tk.Label(self._gb_text, text="Фон для регистрозависимого уровня:", font='arial 10')
        self._lbl_text_bg0.grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        self._text_bg0 = tk.Label(self._gb_text, textvariable='_text_bg0',
                                  font='arial 10', width=5, relief=tk.RAISED)
        self._text_bg0.grid(row=0, column=1, padx=5, sticky=tk.W)
        self._lbl_text_bg1 = tk.Label(self._gb_text, text="Фон для обычного уровня:", font='arial 10')
        self._lbl_text_bg1.grid(row=0, column=2, padx=10, pady=3, sticky=tk.W)
        self._text_bg1 = tk.Label(self._gb_text, textvariable='_text_bg1',
                                  font='arial 10', width=5, relief=tk.RAISED)
        self._text_bg1.grid(row=0, column=3, padx=5, sticky=tk.W)      

        self._gb_input = tk.LabelFrame(self._gb_main, text="Поле ввода текста", font='arial 10')
        self._gb_input.grid(row=4, column=0, padx=5, pady=3)
        self._lbl_input_bg = tk.Label(self._gb_input, text="Фон:", font='arial 10')
        self._lbl_input_bg.grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        self._input_bg = tk.Label(self._gb_input, textvariable='_input_bg',
                                  font='arial 10', width=3, relief=tk.RAISED)
        self._input_bg.grid(row=0, column=1, padx=5, sticky=tk.W)
        self._lbl_input_fg = tk.Label(self._gb_input, text="Текст:", font='arial 10')
        self._lbl_input_fg.grid(row=0, column=2, padx=5, pady=3, sticky=tk.W)
        self._input_fg = tk.Label(self._gb_input, textvariable='_input_fg',
                                  font='arial 10', width=3, relief=tk.RAISED)
        self._input_fg.grid(row=0, column=3, padx=5, sticky=tk.W)
         
        self._gb_status = tk.LabelFrame(self._gb_main, text="Статусбар", font='arial 10')
        self._gb_status.grid(row=4, column=1, padx=5, pady=3, sticky=tk.W)
        self._lbl_status_bg = tk.Label(self._gb_status, text="Фон:", font='arial 10')
        self._lbl_status_bg.grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        self._status_bg = tk.Label(self._gb_status, textvariable='_status_bg',
                                   font='arial 10', width=3, relief=tk.RAISED)
        self._status_bg.grid(row=0, column=1, padx=5, sticky=tk.W)
        self._lbl_status_fg = tk.Label(self._gb_status, text="Текст:", font='arial 10')
        self._lbl_status_fg.grid(row=0, column=2, padx=5, pady=3, sticky=tk.W)
        self._status_fg = tk.Label(self._gb_status, textvariable='_status_fg',
                                   font='arial 10', width=3, relief=tk.RAISED)
        self._status_fg.grid(row=0, column=3, padx=5, sticky=tk.W)
 
        self._gb_auth = tk.LabelFrame(self._gb_main, text="Авторизация", font='arial 10')
        self._gb_auth.grid(row=4, column=2, padx=5, pady=3, sticky=tk.W)
        self._lbl_auth_bg = tk.Label(self._gb_auth, text="Фон:", font='arial 10')
        self._lbl_auth_bg.grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        self._auth_bg = tk.Label(self._gb_auth, textvariable='_auth_bg',
                                 font='arial 10', width=3, relief=tk.RAISED)
        self._auth_bg.grid(row=0, column=1, padx=5, sticky=tk.W)
        self._lbl_auth_fg = tk.Label(self._gb_auth, text="Текст:", font='arial 10')
        self._lbl_auth_fg.grid(row=0, column=2, padx=5, pady=3, sticky=tk.W)
        self._auth_fg = tk.Label(self._gb_auth, textvariable='_auth_fg',
                                 font='arial 10', width=3, relief=tk.RAISED)
        self._auth_fg.grid(row=0, column=3, padx=5, sticky=tk.W)
         
        self._gb_err = tk.LabelFrame(self._gb_main, text="Ошибка ввода", font='arial 10')
        self._gb_err.grid(row=5, column=0, padx=5, pady=3)
        self._lbl_err_bg = tk.Label(self._gb_err, text="Фон:", font='arial 10')
        self._lbl_err_bg.grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        self._err_bg = tk.Label(self._gb_err, textvariable='_err_bg',
                                font='arial 10', width=3, relief=tk.RAISED)
        self._err_bg.grid(row=0, column=1, padx=5, sticky=tk.W)
        self._lbl_err_fg = tk.Label(self._gb_err, text="Текст:", font='arial 10')
        self._lbl_err_fg.grid(row=0, column=2, padx=5, pady=3, sticky=tk.W)
        self._err_fg = tk.Label(self._gb_err, textvariable='_err_fg',
                                font='arial 10', width=3, relief=tk.RAISED)
        self._err_fg.grid(row=0, column=3, padx=5, sticky=tk.W)
         
        self._gb_entry_auth = tk.LabelFrame(self._gb_main, text="Поле ввода логина/пароля", font='arial 10')
        self._gb_entry_auth.grid(row=5, column=1, padx=5, pady=3)
        self._lbl_entry_auth_bg = tk.Label(self._gb_entry_auth, text="Фон:", font='arial 10')
        self._lbl_entry_auth_bg.grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        self._entry_auth_bg = tk.Label(self._gb_entry_auth, textvariable='_entry_auth_bg',
                                       font='arial 10', width=3, relief=tk.RAISED)
        self._entry_auth_bg.grid(row=0, column=1, padx=5, sticky=tk.W)
        self._lbl_entry_auth_fg = tk.Label(self._gb_entry_auth, text="Текст:", font='arial 10')
        self._lbl_entry_auth_fg.grid(row=0, column=2, padx=5, pady=3, sticky=tk.W)
        self._entry_auth_fg = tk.Label(self._gb_entry_auth, textvariable='_entry_auth_fg',
                                       font='arial 10', width=3, relief=tk.RAISED)
        self._entry_auth_fg.grid(row=0, column=3, padx=5, sticky=tk.W)
         
        self._gb_btn_auth = tk.LabelFrame(self._gb_main, text="Кнопка формы авторизации", font='arial 10')
        self._gb_btn_auth.grid(row=5, column=2, padx=5, pady=3)
        self._lbl_btn_auth_bg = tk.Label(self._gb_btn_auth, text="Фон:", font='arial 10')
        self._lbl_btn_auth_bg.grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        self._btn_auth_bg = tk.Label(self._gb_btn_auth, textvariable='_btn_auth_bg',
                                     font='arial 10', width=3, relief=tk.RAISED)
        self._btn_auth_bg.grid(row=0, column=1, padx=5, sticky=tk.W)
        self._lbl_btn_auth_fg = tk.Label(self._gb_btn_auth, text="Текст:", font='arial 10')
        self._lbl_btn_auth_fg.grid(row=0, column=2, padx=5, pady=3, sticky=tk.W)
        self._btn_auth_fg = tk.Label(self._gb_btn_auth, textvariable='_btn_auth_fg',
                                     font='arial 10', width=3, relief=tk.RAISED)
        self._btn_auth_fg.grid(row=0, column=3, padx=5, sticky=tk.W)
        
        self._gb_rb_sett = tk.LabelFrame(self._gb_main, text="Радиокнопки", font='arial 10')
        self._gb_rb_sett.grid(row=6, column=0, padx=5, pady=3)
        self._lbl_rb_sett_bg = tk.Label(self._gb_rb_sett, text="Фон:", font='arial 10')
        self._lbl_rb_sett_bg.grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        self._rb_sett_bg = tk.Label(self._gb_rb_sett, textvariable='_rb_sett_bg',
                                    font='arial 10', width=3, relief=tk.RAISED)
        self._rb_sett_bg.grid(row=0, column=1, padx=5, sticky=tk.W)
        self._lbl_rb_sett_fg = tk.Label(self._gb_rb_sett, text="Текст:", font='arial 10')
        self._lbl_rb_sett_fg.grid(row=0, column=2, padx=5, pady=3, sticky=tk.W)
        self._rb_sett_fg = tk.Label(self._gb_rb_sett, textvariable='_rb_sett_fg',
                                    font='arial 10', width=3, relief=tk.RAISED)
        self._rb_sett_fg.grid(row=0, column=3, padx=5, sticky=tk.W)
         
        self._gb_cb_sett = tk.LabelFrame(self._gb_main, text="Выпадающие списки", font='arial 10')
        self._gb_cb_sett.grid(row=6, column=1, padx=5, pady=3)
        self._lbl_cb_sett_bg = tk.Label(self._gb_cb_sett, text="Фон:", font='arial 10')
        self._lbl_cb_sett_bg.grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        self._cb_sett_bg = tk.Label(self._gb_cb_sett, textvariable='_cb_sett_bg',
                                    font='arial 10', width=3, relief=tk.RAISED)
        self._cb_sett_bg.grid(row=0, column=1, padx=5, sticky=tk.W)
        self._lbl_cb_sett_fg = tk.Label(self._gb_cb_sett, text="Текст:", font='arial 10')
        self._lbl_cb_sett_fg.grid(row=0, column=2, padx=5, pady=3, sticky=tk.W)
        self._cb_sett_fg = tk.Label(self._gb_cb_sett, textvariable='_cb_sett_fg',
                                    font='arial 10', width=3, relief=tk.RAISED)
        self._cb_sett_fg.grid(row=0, column=3, padx=5, sticky=tk.W)
         
        self._gb_box_sett = tk.LabelFrame(self._gb_main, text="Рамки групп", font='arial 10')
        self._gb_box_sett.grid(row=6, column=2, padx=5, pady=3)
        self._lbl_box_sett_bg = tk.Label(self._gb_box_sett, text="Фон:", font='arial 10')
        self._lbl_box_sett_bg.grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        self._box_sett_bg = tk.Label(self._gb_box_sett, textvariable='_box_sett_bg',
                                     font='arial 10', width=3, relief=tk.RAISED)
        self._box_sett_bg.grid(row=0, column=1, padx=5, sticky=tk.W)
        self._lbl_box_sett_fg = tk.Label(self._gb_box_sett, text="Текст:", font='arial 10')
        self._lbl_box_sett_fg.grid(row=0, column=2, padx=5, pady=3, sticky=tk.W)
        self._box_sett_fg = tk.Label(self._gb_box_sett, textvariable='_box_sett_fg',
                                     font='arial 10', width=3, relief=tk.RAISED)
        self._box_sett_fg.grid(row=0, column=3, padx=5, sticky=tk.W)
         
        self._gb_btn_sett = tk.LabelFrame(self._gb_main, text="Кнопка окна настроек", font='arial 10')
        self._gb_btn_sett.grid(row=7, column=0, padx=5, pady=3)
        self._lbl_btn_sett_bg = tk.Label(self._gb_btn_sett, text="Фон:", font='arial 10')
        self._lbl_btn_sett_bg.grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        self._btn_sett_bg = tk.Label(self._gb_btn_sett,  textvariable='_btn_sett_bg',
                                     font='arial 10', width=3, relief=tk.RAISED)
        self._btn_sett_bg.grid(row=0, column=1, padx=5, sticky=tk.W)
        self._lbl_btn_sett_fg = tk.Label(self._gb_btn_sett, text="Текст:", font='arial 10')
        self._lbl_btn_sett_fg.grid(row=0, column=2, padx=5, pady=3, sticky=tk.W)
        self._btn_sett_fg = tk.Label(self._gb_btn_sett, textvariable='_btn_sett_fg',
                                     font='arial 10', width=3, relief=tk.RAISED)
        self._btn_sett_fg.grid(row=0, column=3, padx=5, sticky=tk.W)
        
        self._btn_save = tk.Button(self._wnd, width=5, text="Сохранить тему",
                                   command=lambda arg=False: self._save(arg))
        self._btn_save.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)
        
        self._btn_save_json = tk.Button(self._wnd, width=5, text="Сохранить в файл",
                                        command=lambda arg=True: self._save(arg))
        self._btn_save_json.grid(row=3, column=2, columnspan=3, padx=5, pady=5, sticky=tk.W+tk.E)
        
        self._btn_close = tk.Button(self._wnd, width=5, text="Применить", command=self._set_schema)
        self._btn_close.grid(row=3, column=5, padx=10, pady=5, sticky=tk.W+tk.E)
        
        self._cb_schm.set(list(self._schemes.keys())[0])
        
        self._btn_save_json.configure(state=state_controls[self._logged])

        self._schema_name.configure(state=state_controls[self._logged])
        self._schema_alias.configure(state=state_controls[self._logged])
        
        reg = self._wnd.register(self._callback)
        self._schema_name.config(validate="key", validatecommand=(reg, '%P'))
        self._schema_alias.config(validate="key", validatecommand=(reg, '%P'))

    def _center_wnd(self) -> None:
        """
        Метод отрисовывает окно в центре экрана

        :return: None
        """

        if Config.DEBUG: print('SchemaEditor _center_wnd')
        x = (self._wnd.winfo_screenwidth() // 2) - (self._width // 2)
        y = (self._wnd.winfo_screenheight() // 2) - (self._height // 2)
        self._wnd.geometry("{w}x{h}+{x}+{y}".format(w=self._width, h=self._height, x=x, y=y))
        
        self._wnd.update_idletasks()
    
    def _edit_schema(self) -> None:
        """
        Метод загружает цвета выбранной темы для редактирования

        :return: None
        """
        
        if Config.DEBUG: print('SchemaEditor _edit_schema')
        schema = self._cb_schm.get()
        if schema:
            alias = self._schemes[schema]['name']
            self._e_name.set(schema)
            self._e_alias.set(alias)
            
            self._main_form_bg.configure(bg=self._schemes[schema]['main_form']['bg'])
            self._main_form_fg.configure(bg=self._schemes[schema]['main_form']['fg'])
            self._popup_form_bg.configure(bg=self._schemes[schema]['popup_form']['bg'])
            self._popup_form_fg.configure(bg=self._schemes[schema]['popup_form']['fg'])
            self._btn_start_bg.configure(bg=self._schemes[schema]['btn_start']['bg'])
            self._btn_start_fg.configure(bg=self._schemes[schema]['btn_start']['fg'])
            self._scores_bg.configure(bg=self._schemes[schema]['lbl_scores']['bg'])
            self._scores_fg.configure(bg=self._schemes[schema]['lbl_scores']['fg'])
            self._user_bg.configure(bg=self._schemes[schema]['lbl_user']['bg'])
            self._user_fg.configure(bg=self._schemes[schema]['lbl_user']['fg'])
            self._level_bg.configure(bg=self._schemes[schema]['lbl_level']['bg'])
            self._level_fg.configure(bg=self._schemes[schema]['lbl_level']['fg'])
            self._text_bg0.configure(bg=self._schemes[schema]['lbl_text']['0'])
            self._text_bg1.configure(bg=self._schemes[schema]['lbl_text']['1'])
            self._input_bg.configure(bg=self._schemes[schema]['user_input']['bg'])
            self._input_fg.configure(bg=self._schemes[schema]['user_input']['fg'])
            self._status_bg.configure(bg=self._schemes[schema]['lbl_status']['bg'])
            self._status_fg.configure(bg=self._schemes[schema]['lbl_status']['fg'])
            self._auth_bg.configure(bg=self._schemes[schema]['lbl_auth']['bg'])
            self._auth_fg.configure(bg=self._schemes[schema]['lbl_auth']['fg'])
            self._err_bg.configure(bg=self._schemes[schema]['lbl_err']['bg'])
            self._err_fg.configure(bg=self._schemes[schema]['lbl_err']['fg'])
            self._entry_auth_bg.configure(bg=self._schemes[schema]['entry_auth']['bg'])
            self._entry_auth_fg.configure(bg=self._schemes[schema]['entry_auth']['fg'])
            self._btn_auth_bg.configure(bg=self._schemes[schema]['btn_auth']['bg'])
            self._btn_auth_fg.configure(bg=self._schemes[schema]['btn_auth']['fg'])
            self._rb_sett_bg.configure(bg=self._schemes[schema]['rb_sett']['bg'])
            self._rb_sett_fg.configure(bg=self._schemes[schema]['rb_sett']['fg'])
            self._cb_sett_bg.configure(bg=self._schemes[schema]['cb_sett']['bg'])
            self._cb_sett_fg.configure(bg=self._schemes[schema]['cb_sett']['fg'])
            self._box_sett_bg.configure(bg=self._schemes[schema]['box_sett']['bg'])
            self._box_sett_fg.configure(bg=self._schemes[schema]['box_sett']['fg'])
            self._btn_sett_bg.configure(bg=self._schemes[schema]['btn_sett']['bg'])
            self._btn_sett_fg.configure(bg=self._schemes[schema]['btn_sett']['fg'])
        self._loaded = True

    def _callback(self, text) -> bool:
        """
        Callback-метод для контроля длины текстовых полей
        "название темы" и "псевдоним"
        
        :param text: вводимый текст
        
        :return: возвращает True, если длина текста не превышает 25 символов,
                 в этом случае введенный символ отображается в текстовом поле.
                 Если возвращает False - символ не выводится. 
        """
        
        if Config.DEBUG: print('SchemaEditor _callback')
        if len(text) <= 25:
            return True
        return False       
            
    def get_schema(self) -> str:
        """
        Метод возвращает название темы
        
        :return: возвращает название темы
        """
        
        if Config.DEBUG: print('SchemaEditor get_schema')
        return self._schema
            
    def _save(self, in_file) -> None:
        """
        Метод сохраняет тему в файл .json с названием темы
        
        :param in_file: признак сохранения в файл

        :return: None
        """
        
        if Config.DEBUG: print('SchemaEditor _save')
        schema_name = self._schema_name.get()
        schema_alias = self._schema_alias.get()
        if schema_name.strip() == '':
            self._lbl_schema_name.configure(fg='red')
            self._wnd.after(1000, lambda: self._lbl_schema_name.configure(fg='black'))
        if schema_alias.strip() == '':
            self._lbl_schema_alias.configure(fg='red')
            self._wnd.after(1000, lambda: self._lbl_schema_alias.configure(fg='black'))
        if schema_name in Config.SCHEMES and self._changed:
            schema_name += ' (изменено)'
            schema_alias += ' (изменено)'
            
        if schema_name and schema_alias:
            schema = {
                schema_name: {
                    'name': schema_alias,
                    'main_form': {'bg': self._main_form_bg['bg'], 'fg': self._main_form_fg['bg']},
                    'popup_form': {'bg': self._popup_form_bg['bg'], 'fg': self._popup_form_fg['bg']},
                    'btn_start': {'bg': self._btn_start_bg['bg'], 'fg': self._btn_start_fg['bg']},
                    'lbl_scores': {'bg': self._scores_bg['bg'], 'fg': self._scores_fg['bg']},
                    'lbl_user': {'bg': self._user_bg['bg'], 'fg': self._user_fg['bg']},
                    'lbl_level': {'bg': self._level_bg['bg'], 'fg': self._level_fg['bg']},
                    'lbl_text': {'0': self._text_bg0['bg'], '1': self._text_bg1['bg']},
                    'user_input': {'bg': self._input_bg['bg'], 'fg': self._input_fg['bg']},
                    'lbl_status': {'bg': self._status_bg['bg'], 'fg': self._status_fg['bg']},
                    'lbl_auth': {'bg': self._auth_bg['bg'], 'fg': self._auth_fg['bg']},
                    'lbl_err': {'bg': self._err_bg['bg'], 'fg': self._err_fg['bg']},
                    'entry_auth': {'bg': self._entry_auth_bg['bg'], 'fg': self._entry_auth_fg['bg']},
                    'btn_auth': {'bg': self._btn_auth_bg['bg'], 'fg': self._btn_auth_fg['bg']},
                    'rb_sett': {'bg': self._rb_sett_bg['bg'], 'fg': self._rb_sett_fg['bg']},
                    'cb_sett': {'bg': self._cb_sett_bg['bg'], 'fg': self._cb_sett_fg['bg']},
                    'box_sett': {'bg': self._box_sett_bg['bg'], 'fg': self._box_sett_fg['bg']},
                    'btn_sett': {'bg': self._btn_sett_bg['bg'], 'fg': self._btn_sett_fg['bg']},
                        }
                }
            if self._changed:
                self._master.schemes.update(schema)
            
        if in_file and schema_name:
            with open(schema_name + '.json', 'w') as f:
                json.dump(schema, f)
                messagebox.showinfo(message='Файл сохранен в файле {schema_name}.json'.format(schema_name=schema_name))
        
        if schema_name and self._changed:
            if schema_name not in self._cb_schm['values']:
                self._cb_schm['values'] += (schema_name,)
            self._cb_schm.set(schema_name)
        self._changed = False

    def _set_schema(self) -> None:
        """
        Метод устанавливает выбранную тему
        
        :return: None
        """
        
        if Config.DEBUG: print('SchemaEditor _set_schema')
        self._schema = self._cb_schm.get()
        self._on_closing()

    def _on_click(self, event) -> None:
        """
        Метод обрабатывает нажатие и вызывает окно для изменения цвета

        :return: None
        """
        
        if Config.DEBUG: print('SchemaEditor _on_click')
        if event.widget.widgetName == 'label' and self._loaded and self._colorchooser is None:
            ctrl_name = event.widget.cget("textvariable")
            if ctrl_name != '':
                ctrl = getattr(self, str(ctrl_name))
                self._colorchooser = colorchooser
                (rgb, hx) = self._colorchooser.askcolor(ctrl['bg'])
                self._colorchooser = None
                if hx:
                    ctrl.configure(bg=hx)
                    self._changed = True
                    schema = self._cb_schm.get()
                    if schema in Config.SCHEMES.keys():                        
                        alias = self._schemes[schema]['name']
                        self._e_name.set(schema + ' (изменено)')
                        self._e_alias.set(alias + ' (изменено)')

    def _on_closing(self) -> None:
        """
        Метод при закрытии окна по крестику или Escape

        :return: None
        """

        if Config.DEBUG: print('SchemaEditor _on_closing')
        self._wnd.destroy()
        