from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.properties import (StringProperty, ObjectProperty)
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout

import tkinter
from tkinter import filedialog
from os import path

import json


class ProjectCard(MDCard, RoundedRectangularElevationBehavior):
    bookName = ObjectProperty()
    pageNumber = ObjectProperty()
    chapNumber = ObjectProperty()
    newPath = ObjectProperty()

    mainObj = ObjectProperty()

    def open_project(self):
        tkinter.Tk().withdraw()
        folder_path = filedialog.askdirectory()
        self.newPath.set_text(self, folder_path)
        print(folder_path)
        return

    def toMain(self):
        newProject = {
            "book_name": self.bookName.text,
            "page_number": int(self.pageNumber.text),
            "chap_number": int(self.chapNumber.text),
            "proj_path": self.newPath.text,
            "cur_page": 1,
            "cur_chap": 0,
            "left_page": "",
            "right_page": ""
        }

        MDApp.get_running_app().root.statedata.newProject = newProject
        with open(f'{newProject["proj_path"]}/configs.json', 'w+') as write_file:
            json.dump(newProject, write_file)
        self.mainObj.ids.main_layout.disabled = ''
        self.mainObj.remove_widget(self.mainObj.ids.new_project)





class NewProject(MDFloatLayout):
    mainObj = ObjectProperty()
    pass
