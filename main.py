import sys
from subprocess import call
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')
        self.setGeometry(300, 300, 300, 300)

        btn1 = QPushButton('Program 1', self)
        btn1.move(20, 20)
        btn1.clicked.connect(self.btn1_clicked)

        btn2 = QPushButton('Program 2', self)
        btn2.move(20, 60)
        btn2.clicked.connect(self.btn2_clicked)

    def btn1_clicked(self):
        call('python ./test_scripts/pika_receive.py', shell=True)

    def btn2_clicked(self):
        call('python ./test_scripts/pike_send.py', shell=True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec_()


# 키움 api에서 데이터를 rabbitmq로 전송
# 사이의 서비스 하나가 계속 consume하면서 딕셔너리 형식으로 데이터를 차곡차곡 쌓아감
# 꼭 시작 데이터와 마지막 데이터를 정해야 한다 (그 이상은 필요없는 데이터로 치부)
# 연결 1: 키움 api <--> real time data store(rpc server)
# trading engine이 데이터를 요청하면 real time data store에서 데이터를 만지고 보내주기
# 연결 2: real time data store(rpc server) <--> trading engine
# 여기서 요청할 수 있는 데이터
# set_start_end(start: int, end: int) --> void
# get_latest_data(value: str) --> list[int]
# tail_latest_data(count: int) --> list[list[int]]
# get_ticker_data_from_to(ticker: str, from: str, to: str) --> list[list[int]]
# tail_ticker(ticker: str, count: int) -> list[list[int]]
