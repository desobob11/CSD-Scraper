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
    
        tb = QTableView()

        columns = ["File Name", "Id"]

        model = QStandardItemModel()
        tb.setModel(model)

        for i in columns:
            item = QStandardItem(i)
            item.setEditable(False)
            model.setColumnCount(4)
            model.setHorizontalHeaderLabels(["File Name", "Alias", "Application", "Schema", "Table"])

        '''
            Load in config data from file
        '''
        file_lines = None
        with open("pickles/file.txt", "r") as src:
            file_lines = src.readlines()
        
        '''
            Fill the table view with the data
        '''
        confirmed_names = []
        for i in file_lines:
            item_row = []
            for cell in i.split(":"):
                item_row.append(QStandardItem(cell))
            confirmed_names.append(item_row[0].text())
            model.appendRow(item_row)
        

        
  


        '''
            Check for scrapers in the directory
        '''
        files = self.get_scrapers()

        for i in files:
            if i not in confirmed_names:
                name = QStandardItem(i)
                alias = QStandardItem("")
                application = QStandardItem("")
                schema = QStandardItem("")
                table = QStandardItem("")
                model.appendRow([name, alias, application, schema, table])

   
        tb.setFixedWidth(575)
        tb.setFixedHeight(500)

        layout.addWidget(tb)
    

        view.setLayout(layout)


        view.setWindowTitle("HLSM - Main")

        print(confirmed_names)
        
        return view




