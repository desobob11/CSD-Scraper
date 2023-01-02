'''
    4017b4538b36eb26b9fa5bb1ed7509c01ac9dbae60ed09272510a742a8535b6d
'''
'''
    Above is a hash denoting that this file is the code for the 
    driver setup application, so it should not include itself
    when finding valid scrapers in a directory
'''
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QObject
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
from hlsm_back import Back_End
import pathlib
import sys
import os


class hlsm_front():

    '''
        Some class-level constants in the constructor
    '''
    def __init__(self):
        self.BUTTON_WIDTH = 50
        self.BUTTON_HEIGHT = 25
        self.tb = QTableView()
        self.model = QStandardItemModel()
        self.tb.setModel(self.model)
        self.state_file = "pickles/state.bin"

    '''
        Create symbol QApplication and return it
    '''
    def create_app(self) -> QApplication:
        app = QApplication(sys.argv)
        return app

    def get_scrapers(self) -> list[str]:
        scraper_hash = "949eb6c5d3061308be1382734d5e6df61d56b15c16b7db0cf85a75bfdc0a34b0"
        setup_hash = "4017b4538b36eb26b9fa5bb1ed7509c01ac9dbae60ed09272510a742a8535b6d"
        cwd = os.getcwd()
        files = [i for i in os.listdir(cwd) if ".py" in i]

        scrapers = []
        for i in files:
            with open(i, "r") as file:
                contents = file.read()
                if (scraper_hash in contents and not setup_hash in contents):
                    scrapers.append(i)
        return scrapers

    '''
        def load_state(self) -> list[str]:
            file_lines = None
            with open(self.state_file, "rb") as src:
                file_lines = src.readlines()
            confirmed_names = []
            for i in file_lines:
                item_row = []
                for cell in i.split(":"):
                    item_row.append(QStandardItem(cell))
                confirmed_names.append(item_row[0].text())
                self.model.appendRow(item_row)
            return confirmed_names
    '''


    def load_state(self) -> list[str]:
        try:    
            file_lines = None
            file_contents = ""
            with open(self.state_file, "rb") as src:
                file_contents = Back_End.bin_decode(src)
            file_lines = file_contents.split("\n")
            print(file_lines)
            confirmed_names = []
            for i in file_lines:
                item_row = []
                for cell in i.split(":"):
                    item_row.append(QStandardItem(cell))
                confirmed_names.append(item_row[0].text())
                self.model.appendRow(item_row)
            return confirmed_names
        except:
            return None

    def cross_check(self, files_in_dir: list[str], state_files: list[str]) -> None:
            for i in files_in_dir:
                if state_files is None:
                    name = QStandardItem(i)
                    alias = QStandardItem(" ")
                    application = QStandardItem(" ")
                    schema = QStandardItem(" ")
                    table = QStandardItem(" ")
                    self.model.appendRow([name, alias, application, schema, table])
                elif i not in state_files:
                    name = QStandardItem(i)
                    alias = QStandardItem(" ")
                    application = QStandardItem(" ")
                    schema = QStandardItem(" ")
                    table = QStandardItem(" ")
                    self.model.appendRow([name, alias, application, schema, table])




    def write_state(self) -> None:
        file_contents = ""
        for i in range(self.model.rowCount()):
            str_row = ""
            for j in range(self.model.columnCount()):
                value = self.model.data(self.model.index(i, j))
                if value is not None:
                    str_row += value
                    str_row += ":"
            str_row = str_row.removesuffix(":")
            str_row += "\n"
            file_contents += str_row
        file_contents = file_contents.strip()
        
        with open(self.state_file, "wb") as bin:
            bin_list = Back_End.bin_encode(file_contents)
            for i in bin_list:
                bin.write(i)






    '''
        Function for outlining the main view of the program,
        tbh this could probably be the only view and probably
        should be the only view, program needs
        to be simple
    
    '''
    def main_view(self) -> QWidget:
        view = QWidget()
        view.setFixedWidth(600)
        view.setFixedHeight(600)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    
        columns = ["File Name", "Id"]

        for i in columns:
            item = QStandardItem(i)
            item.setEditable(False)
            self.model.setColumnCount(4)
            self.model.setHorizontalHeaderLabels(["File Name", "Alias", "Application", "Schema", "Table"])

        state_files = self.load_state()

        '''
            Check for scrapers in the directory
        '''
        files = self.get_scrapers()

        #self.cross_check(files, state_files)

        self.tb.setFixedWidth(575)
        self.tb.setFixedHeight(500)
        layout.addWidget(self.tb)
        view.setLayout(layout)
        view.setWindowTitle("HLSM - Main")

        return view

