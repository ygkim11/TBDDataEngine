from kiwoom.get_real_data import *
import sys
from PyQt5.QtWidgets import *

class Main():
    def __init__(self):
        print('실행할 메인 클래스')


        #python 위치참조?
        self.app = QApplication(sys.argv)

        self.get_real_data = Get_Real_Data()

        self.app.exec_()


if __name__ == '__main__':
    Main()


