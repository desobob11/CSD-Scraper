import hlsm_back as back
from hlsm_front import hlsm_front
from hlsm_back import Back_End

from PyQt6.QtWidgets import *
from PyQt6.QtCore import QObject
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
from hlsm_back import Back_End
import pathlib
import sys
import os




def main():
    
    app = QApplication(sys.argv)
    front_end = hlsm_front()
    binary = None
    text = None
    main_view = front_end.main_view()
    main_view.show()

    front_end.write_state()

    app.exec()




if __name__ == "__main__":
    main()





