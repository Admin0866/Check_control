import os

from kivy.lang import Builder
from kivy.config import Config
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.filemanager import MDFileManager
import sqlite3

Config.set('kivy', 'keyboard_mode', 'systemanddock')
Window.size = (480, 680)

# class Database:
#     def __init__(self, db_name):
#         self.conn = sqlite3.connect(db_name)
#         self.cursor = self.conn.cursor()
#
#     def create_table(self):
#         query = """
#         CREATE TABLE IF NOT EXISTS cheque (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             text TEXT NOT NULL,
#             meaning INTEGER NOT NULL
#         );
#         """
#         self.cursor.execute(query)
#         self.conn.commit()
#
#     def insert_user(self, name, age):
#         query = """
#         INSERT INTO cheque (text, meaning)
#         VALUES (?, ?);
#         """
#         self.cursor.execute(query, (text, meaning))
#         self.conn.commit()
#
#     def get_users(self):
#         query = """
#         SELECT * FROM cheque;
#         """
#         self.cursor.execute(query)
#         result = self.cursor.fetchall()
#         return result

class Shopping(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path
        )

    def build(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Gray'

        # self.db_name = "database.db"
        # global database
        # database = Database(self.db_name)
        # database.create_table()

        self.gl = MDGridLayout(rows=6, md_bg_color = (220/255, 230/255, 220/255, 1))

        self.tb = MDTopAppBar(title = "CHEQUE CONTROL", anchor_title = "left", size_hint_y = None, height = 1, specific_text_color = "white",
                              left_action_items = [["menu", lambda x: self.callback(x)]], md_bg_color = (209/255, 212/255, 208/255, 1))

        self.menu = MDDropdownMenu(
            items=[
                {
                    "viewclass": "OneLineListItem",
                    "text": "Открыть",
                    "height": dp(35),
                    "on_release": self.file_manager_open,
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Сохранить",
                    "height": dp(35),
                    "on_release": self.menu_seve,
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Удалить",
                    "height": dp(35),
                    "on_release": self.menu_delet,
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Закрыть",
                    "height": dp(35),
                    "on_release": self.on_menu_close,
                }
            ],
            width_mult=2,
        )

        self.al = MDAnchorLayout(anchor_x='left', anchor_y='top', padding=[10, 15, 5, 5], size_hint_y=None, height=40, md_bg_color = (220/255, 230/255, 220/255, 1))
        self.lb = MDLabel(text='0', halign='left', valign='center', size_hint=(1, .2))
        self.al.add_widget(self.lb)

        self.grl = MDGridLayout(cols = 5, padding = [5, 5, 0, 10], spacing=1, size_hint_y = None, height = 20, md_bg_color = (209/255, 212/255, 208/255, 1))
        self.grl.add_widget(MDLabel(text = 'товар', halign='center', size_hint_x = None, width = 180, size_hint_y = None, height = 10))
        self.grl.add_widget(MDLabel(text='ед.',halign='center', size_hint_y=None, height=10))
        self.grl.add_widget(MDLabel(text='к-во',halign='center',  size_hint_y=None, height=10))
        self.grl.add_widget(MDLabel(text='цена',halign='center', size_hint_y=None, height=10))
        self.grl.add_widget(MDLabel(text='сумма',halign='center', size_hint_y=None, height=10))

        self.gr = MDGridLayout(rows=8, cols=5, padding = (5, 5, 5, 5), spacing = 1, size_hint_y=None, height=500, md_bg_color = (220/255, 230/255, 220/255, 1))
        self.gr.text_input1 = MDTextField(size_hint_x = None, width=180, size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.text_input1)
        self.gr.text_input2 = MDTextField(halign='center', size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.text_input2)
        self.gr.number1 = MDTextField(text='0', halign='center', size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.number1)
        self.gr.number2 = MDTextField(text='0', halign='center', size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.number2)
        self.gr.result1 = MDLabel(text='0', halign='center', size_hint_y = None, height = 50)
        self.gr.add_widget(self.gr.result1)

        self.gr.text_input3 = MDTextField(size_hint_x = None, width=180, size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.text_input3)
        self.gr.text_input4 = MDTextField(halign='center', size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.text_input4)
        self.gr.number3 = MDTextField(text='0', halign='center', size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.number3)
        self.gr.number4 = MDTextField(text='0', halign='center', size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.number4)
        self.gr.result2 = MDLabel(text='0', halign='center', size_hint_y = None, height = 50)
        self.gr.add_widget(self.gr.result2)

        self.gr.text_input5 = MDTextField(size_hint_x = None, width=180, size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.text_input5)
        self.gr.text_input6 = MDTextField(halign='center', size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.text_input6)
        self.gr.number5 = MDTextField(text='0', halign='center', size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.number5)
        self.gr.number6 = MDTextField(text='0', halign='center', size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.number6)
        self.gr.result3 = MDLabel(text='0', halign='center', size_hint_y = None, height = 50)
        self.gr.add_widget(self.gr.result3)

        self.gr.text_input7 = MDTextField(size_hint_x = None, width=180, size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.text_input7)
        self.gr.text_input8 = MDTextField(halign='center', size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.text_input8)
        self.gr.number7 = MDTextField(text='0', halign='center', size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.number7)
        self.gr.number8 = MDTextField(text='0', halign='center', size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.number8)
        self.gr.result4 = MDLabel(text='0', halign='center', size_hint_y = None, height = 50)
        self.gr.add_widget(self.gr.result4)

        self.gr.text_input9 = MDTextField(size_hint_x = None, width=180, size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.text_input9)
        self.gr.text_input10 = MDTextField(halign='center', size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.text_input10)
        self.gr.number9 = MDTextField(text='0', halign='center', size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.number9)
        self.gr.number10 = MDTextField(text='0', halign='center', size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.number10)
        self.gr.result5 = MDLabel(text='0', halign='center', size_hint_y = None, height = 50)
        self.gr.add_widget(self.gr.result5)

        self.gr.text_input11 = MDTextField(size_hint_x = None, width=180, size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.text_input11)
        self.gr.text_input12 = MDTextField(halign='center', size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.text_input12)
        self.gr.number11 = MDTextField(text='0', halign='center', size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.number11)
        self.gr.number12 = MDTextField(text='0', halign='center', size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.number12)
        self.gr.result6 = MDLabel(text='0', halign='center', size_hint_y = None, height = 50)
        self.gr.add_widget(self.gr.result6)

        self.gr.text_input13 = MDTextField(size_hint_x = None, width=180, size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.text_input13)
        self.gr.text_input14 = MDTextField(halign='center', size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.text_input14)
        self.gr.number13 = MDTextField(text='0', halign='center', size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.number13)
        self.gr.number14 = MDTextField(text='0', halign='center', size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.number14)
        self.gr.result7 = MDLabel(text='0', halign='center', size_hint_y = None, height = 50)
        self.gr.add_widget(self.gr.result7)

        self.gr.text_input15 = MDTextField(size_hint_x = None, width=180, size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.text_input15)
        self.gr.text_input16 = MDTextField(halign='center', size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.text_input16)
        self.gr.number15 = MDTextField(text='0', halign='center', size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.number15)
        self.gr.number16 = MDTextField(text='0', halign='center', size_hint_y = None, height = 2)
        self.gr.add_widget(self.gr.number16)
        self.gr.result8 = MDLabel(text='0', halign='center', size_hint_y = None, height = 50)
        self.gr.add_widget(self.gr.result8)

        self.bl = MDBoxLayout(spacing = 10, padding = (150, 0, 0, 10), size_hint_x = 1)
        self.btn1 = MDRaisedButton(text = 'СБРОС', size_hint_y = None, height = 40)
        self.btn2 = MDRaisedButton(text = 'ВВОД', size_hint_y = None, height = 40)
        self.btn1.bind(on_press=self.clear_text)
        self.btn2.bind(on_press=self.add_numbers)
        self.bl.add_widget(self.btn1)
        self.bl.add_widget(self.btn2)

        self.gl.add_widget(self.tb)
        self.gl.add_widget(self.al)
        self.gl.add_widget(self.grl)
        self.gl.add_widget(self.gr)
        self.gl.add_widget(self.bl)

        return self.gl

    def add_numbers(self, instance):
        result = float(self.gr.number1.text) * float(self.gr.number2.text)
        self.gr.result1.text = str(result)
        result = float(self.gr.number3.text) * float(self.gr.number4.text)
        self.gr.result2.text = str(result)
        result = float(self.gr.number5.text) * float(self.gr.number6.text)
        self.gr.result3.text = str(result)
        result = float(self.gr.number7.text) * float(self.gr.number8.text)
        self.gr.result4.text = str(result)
        result = float(self.gr.number9.text) * float(self.gr.number10.text)
        self.gr.result5.text = str(result)
        result = float(self.gr.number11.text) * float(self.gr.number12.text)
        self.gr.result6.text = str(result)
        result = float(self.gr.number13.text) * float(self.gr.number14.text)
        self.gr.result7.text = str(result)
        result = float(self.gr.number15.text) * float(self.gr.number16.text)
        self.gr.result8.text = str(result)

        result = float(self.gr.result1.text) + float(self.gr.result2.text) +\
                 float(self.gr.result3.text) + float(self.gr.result4.text) +\
                 float(self.gr.result5.text) + float(self.gr.result6.text) +\
                 float(self.gr.result7.text) + float(self.gr.result8.text)

        self.lb.text = str(result)

    def clear_text(self, text_input):
        self.gr.text_input1.text = ""
        self.gr.text_input2.text = ""
        self.gr.number1.text = "0"
        self.gr.number2.text = "0"
        self.gr.result1.text = "0"

        self.gr.text_input3.text = ""
        self.gr.text_input4.text = ""
        self.gr.number3.text = "0"
        self.gr.number4.text = "0"
        self.gr.result2.text = "0"

        self.gr.text_input5.text = ""
        self.gr.text_input6.text = ""
        self.gr.number5.text = "0"
        self.gr.number6.text = "0"
        self.gr.result3.text = "0"

        self.gr.text_input7.text = ""
        self.gr.text_input8.text = ""
        self.gr.number7.text = "0"
        self.gr.number8.text = "0"
        self.gr.result4.text = "0"

        self.gr.text_input9.text = ""
        self.gr.text_input10.text = ""
        self.gr.number9.text = "0"
        self.gr.number10.text = "0"
        self.gr.result5.text = "0"

        self.gr.text_input11.text = ""
        self.gr.text_input12.text = ""
        self.gr.number11.text = "0"
        self.gr.number12.text = "0"
        self.gr.result6.text = "0"

        self.gr.text_input13.text = ""
        self.gr.text_input14.text = ""
        self.gr.number13.text = "0"
        self.gr.number14.text = "0"
        self.gr.result7.text = "0"

        self.gr.text_input15.text = ""
        self.gr.text_input16.text = ""
        self.gr.number15.text = "0"
        self.gr.number16.text = "0"
        self.gr.result8.text = "0"

        self.lb.text = "0"

    def callback(self, button):
        self.menu.caller = button
        self.menu.open()

    def menu_callback(self, text_item):
        self.menu.dismiss()
        Snackbar(text=text_item).open()


    def file_manager_open(self):
        self.file_manager.show(os.path.expanduser("~"))  # менеджер вывода на экран
        self.manager_open = True

    def select_path(self, path: str):  # Он будет вызван, когда вы нажмете на имя файла
                                       # или кнопка выбора каталога.
                                       # параметр path: путь к выбранному каталогу или файлу
        '''
        It will be called when you click on the file name
        or the catalog selection button.

        :param path: path to the selected directory or file;
        '''

        self.exit_manager()
        toast(path)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.''' # Вызывается, когда пользователь достигает корня дерева каталогов.

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):  # Вызывается при нажатии кнопок на мобильном устройстве.
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()

    def menu_seve(self):
        print("Save as")

    def menu_delet(self):
        print("removal")

    def on_menu_close(self, *args):
        self.stop()

Shopping().run()