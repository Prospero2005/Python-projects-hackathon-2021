"""
Модуль конфигурации
"""


class Levels:
    """
    Класс с данными
    """
    
    ALPHABET = {'EN': 'ABCDEFGHIJKLMNOPQRSTUVWXWZ',
                'RU': 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'}

    WORDS = {'EN': ['people', 'member', 'animal', 'children', 'country',
                    'home', 'money', 'number', 'picture', 'product',
                    'school', 'sister', 'water', 'world', 'answer',
                    'color', 'family', 'friend', 'horse', 'mountain'],
             'RU': ['один', 'самолёт', 'тарелка', 'четыре', 'друзья',
                    'подъезд', 'корова', 'собака', 'царство', 'чайник',
                    'родина', 'выстрел', 'дорога', 'юбилей', 'ярмарка',
                    'десять', 'щавель', 'шахматы', 'восемь', 'сапоги'
                    ]}

    TEXT = {'EN': ['Dad has come!', 'How is it going?', 'Until we meet again',
                   'What are you up to?', 'See you soon!', 'And so on and so forth',
                   'On the other hand', 'As I said before', 'What do you know!',
                   'Next time lucky', 'As far as I remember', 'It looks like that',
                   'That goes without saying', 'There is no denying it'],
            'RU': ['Мама мыла раму', 'У Кати кукла', 'Барабан на столе',
                   'Листья лежат на земле', 'Весной прилетели птицы',
                   'В школе праздник', 'Сегодня у папы выходной',
                   'Едет красная машина', 'Велосипед поломался',
                   'Шла Саша по шоссе', 'Во дворе растет трава',
                   'На траве лежат дрова', 'Скоро наступит лето']}


class Config:
    """
    Класс конфигурации
    """
    
    DEBUG = False
    TITLE = "Игра 'Клавиатурный тренажер'."
    DBNAME = 'users.db'
    START_ORIENT = 'H'
    SHOW_MSG = 0
    START_LVL = 1
    MAX_COUNT = 10    
    ANONYMOUS = 'Anonymous'
    SCHEMA = 'light'
    
    LANG = ['EN', 'RU']
    
    LEVELS = {1: (Levels.ALPHABET, True),
              2: (Levels.ALPHABET, True),
              3: (Levels.ALPHABET, False),
              4: (Levels.ALPHABET, True),
              5: (Levels.ALPHABET, False),
              6: (Levels.WORDS, True),
              7: (Levels.WORDS, False),
              8: (Levels.TEXT, True)}

    ORIENTATION = {'H': {'root_width': 490, 'root_height': 200},
                   'V': {'root_width': 300, 'root_height': 300}}
    
    SCHEMES = {'light': {'name': 'Светлая тема',
                         'main_form': {'bg': '#B0AEE6', 'fg': 'white'},
                         'popup_form': {'bg': '#D0A1C6', 'fg': 'white'},
                         'btn_start': {'bg': '#FF5A40', 'fg': 'white'},
                         'lbl_scores': {'bg': '#FF5A40', 'fg': 'white'},
                         'lbl_user': {'bg': '#00816C', 'fg': 'white'},
                         'lbl_level': {'bg': '#FEBF5A', 'fg': '#310010'},
                         'lbl_text': {'0': 'purple', '1': 'green'},
                         'user_input': {'bg': '#A8A8A8', 'fg': 'black'},
                         'lbl_status': {'bg': '#B0AEE6', 'fg': 'black'},
                         'lbl_auth': {'bg': '#D0A1C6', 'fg': 'black'},
                         'lbl_err': {'bg': 'red', 'fg': 'white'},
                         'entry_auth': {'bg': '#D5D5D5', 'fg': 'black'},
                         'btn_auth': {'bg': '#0A6A37', 'fg': 'white'},
                         'rb_sett': {'bg': '#D0A1C6', 'fg': 'black'},
                         'cb_sett': {'bg': '#D0A1C6', 'fg': 'black'},
                         'box_sett': {'bg': '#D0A1C6', 'fg': 'black'},
                         'btn_sett': {'bg': '#0A6A37', 'fg': 'white'}
                         },
               'dark': {'name': 'Темная тема',
                        'main_form': {'bg': '#1C0D15', 'fg': 'white'},
                        'popup_form': {'bg': '#2A1630', 'fg': 'white'},
                        'btn_start': {'bg': '#181616', 'fg': '#D01C00'},
                        'lbl_scores': {'bg': '#181616', 'fg': '#D01C00'},
                        'lbl_user': {'bg': '#130069', 'fg': '#D4D4D4'},
                        'lbl_level': {'bg': '#790600', 'fg': '#D4D4D4'},
                        'lbl_text': {'0': '#3D0030', '1': '#003C1C'},
                        'user_input': {'bg': '#2A2A2A', 'fg': 'white'},
                        'lbl_status': {'bg': '#1C0D15', 'fg': '#D4D4D4'},
                        'lbl_auth': {'bg': '#2A1630', 'fg': '#FF0000'},
                        'lbl_err': {'bg': '#5D0048', 'fg': 'red'},
                        'entry_auth': {'bg': '#2B2B2B', 'fg': 'white'},
                        'btn_auth': {'bg': '#0A6A37', 'fg': 'white'},
                        'rb_sett': {'bg': '#2A1630', 'fg': '#FF0000'},
                        'cb_sett': {'bg': '#2A1630', 'fg': '#FF0000'},
                        'box_sett': {'bg': '#2A1630', 'fg': 'white'},
                        'btn_sett': {'bg': '#0A6A37', 'fg': 'white'}
                         }
               }



