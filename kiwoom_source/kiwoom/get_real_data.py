import os
import sys
import json

from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from config.errorCode_prac import *
from PyQt5.QtTest import *
from config.kiwoomType_prac import *
import csv
import datetime as dt
import numpy as np
from kiwoom.save_csv import save_kiwoom_stocks_data_to_csv, save_kiwoom_futures_data_to_csv

from dotenv import load_dotenv
import pika

load_dotenv()

# REMOTE_RABBIT_HOST = os.getenv('REMOTE_RABBITMQ_HOST', 'localhost')
# REMOTE_RABBIT_USER = os.getenv('REMOTE_RABBITMQ_USER', 'guest')
# REMOTE_RABBIT_PASS = os.getenv('REMOTE_RABBITMQ_PASSWORD', 'guest')
#
# RABBIT_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
# RABBIT_PORT = os.getenv('RABBITMQ_PORT', 'localhost')
# RABBIT_USER = os.getenv('RABBITMQ_USER', 'guest')
# RABBIT_PASS = os.getenv('RABBITMQ_PASSWORD', 'guest')
#
# credentials = pika.PlainCredentials(username=RABBIT_USER, password=RABBIT_PASS)
# conn = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT, credentials=credentials))
#
# kiwoom_stocks_channel = conn.channel()
# kiwoom_stocks_channel.queue_declare(queue='kiwoom_stocks_data')
#
# kiwoom_futures_channel = conn.channel()
# kiwoom_futures_channel.queue_declare(queue='kiwoom_futures_data')

class Get_Real_Data(QAxWidget):
    def __init__(self):

        super().__init__()

        print("#"*6 , "Kiwoom Class initiated" , "#"*6)

        # self.stocks_futures_code = ['101R3000', '101R6000', '101R9000']  # 지수 선물 example
        # self.sample_stock_code_2 = ["005930", "245620", "170030", "336370"]  # 삼성 , edgc, 현대공업, 두산솔루스
        self.kiwoom_stocks_data = {}

        self.all_event_loop = QEventLoop()

        self.realType = RealType()

        self.get_ocx_instance()
        self.event_slots()
        self.real_events_slots()

        self.signal_login_commConnect()
        # self.get_account_info()

        #스크린번호
        self.screen_real_stock = "5000"
        self.screen_start_stop_real = "1000"

        self.stocks_code = self.get_code_list_by_market(0) + self.get_code_list_by_market(10)
        self.futures_code = self.get_futures_code_list("") #blank = 전 종목
        self.stocks_futures_code = self.stocks_code + self.futures_code



        #Base Dict 생성
        for code in self.stocks_futures_code:
            self.kiwoom_stocks_data[code] = {
                'code': None,
                'trade_date': None,
                'timestamp': None,
                'current_price': None,
                'open_price': None,
                'high': None,
                'low': None,
                'volume': None,
                'cum_volume': None,
                'trade_sell_hoga1': None,
                'trade_buy_hoga1': None,
                'hoga_date': None,
                'sell_hoga10': None,
                'sell_hoga9': None,
                'sell_hoga8': None,
                'sell_hoga7': None,
                'sell_hoga6': None,
                'sell_hoga5': None,
                'sell_hoga4': None,
                'sell_hoga3': None,
                'sell_hoga2': None,
                'sell_hoga1': None,
                'buy_hoga1': None,
                'buy_hoga2': None,
                'buy_hoga3': None,
                'buy_hoga4': None,
                'buy_hoga5': None,
                'buy_hoga6': None,
                'buy_hoga7': None,
                'buy_hoga8': None,
                'buy_hoga9': None,
                'buy_hoga10': None,
                'sell_hoga10_stack': None,
                'sell_hoga9_stack': None,
                'sell_hoga8_stack': None,
                'sell_hoga7_stack': None,
                'sell_hoga6_stack': None,
                'sell_hoga5_stack': None,
                'sell_hoga4_stack': None,
                'sell_hoga3_stack': None,
                'sell_hoga2_stack': None,
                'sell_hoga1_stack': None,
                'buy_hoga1_stack': None,
                'buy_hoga2_stack': None,
                'buy_hoga3_stack': None,
                'buy_hoga4_stack': None,
                'buy_hoga5_stack': None,
                'buy_hoga6_stack': None,
                'buy_hoga7_stack': None,
                'buy_hoga8_stack': None,
                'buy_hoga9_stack': None,
                'buy_hoga10_stack': None,
                'total_buy_hoga_stack': None,
                'total_sell_hoga_stack': None,
                'net_buy_hoga_stack': None,
                'net_sell_hoga_stack': None,
                'ratio_buy_hoga_stack': None,
                'ratio_sell_hoga_stack': None
            }

        self.dynamicCall("SetRealReg(QString,QString,QString,QString)", self.screen_start_stop_real, "",
                         self.realType.REALTYPE['장시작시간']['장운영구분'], "0")  # 처음등록할땐 0 이후에 추가는 1!


        #Screen Num 할당 및 실시간 RealReg 등록
        stock_cnt = 0
        screen_num = int(self.screen_real_stock)
        for i, code in enumerate(self.stocks_futures_code):
            if (stock_cnt % 50) == 0: #Screen Num 할당; 50종목당 ScreenNum 1 추가
                screen_num += 1

            fids = str(self.realType.REALTYPE['주식체결']['체결시간']) + ";" + str(self.realType.REALTYPE['주식호가잔량']['매수호가1'])

            # 실시간 등록은 SetRealReg
            self.dynamicCall("SetRealReg(QString,QString,QString,QString)", screen_num, code, fids,
                             "1")  # 처음등록할땐 0 이후에 추가는 1!
            # self.dynamicCall("SetRealReg(QString,QString,QString,QString)", screen_num, code, fids2,
            #                  "1")  # 처음등록할땐 0 이후에 추가는 1!

            print("실시간 등록 코드: %s, 스크린번호: %s, fid번호: %s" % (code, screen_num, fids))

            stock_cnt += 1



    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def login_slot(self,errCode):
        print(errors(errCode))

        self.login_event_loop.exit()

    def signal_login_commConnect(self):
        self.dynamicCall("CommConnect()")

        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def event_slots(self):
        self.OnEventConnect.connect(self.login_slot)

    def real_events_slots(self):
        self.OnReceiveRealData.connect(self.realdata_slot)


    def realdata_slot(self, sCode, sRealType, sRealData):
        if sRealType == "장시작시간":
            fid = self.realType.REALTYPE[sRealType]['장운영구분']
            value = self.dynamicCall("GetCommRealData(QString, int)", sCode, fid)

            if value == "0":
                print("장 시작 전")
            elif value == "3":
                print("장 시작!")
            elif value == "2":
                print("3시 20분!!, 동시호가")
            elif value == "4":
                print("3시 30분 장 종료!")


        elif (sRealType == "주식체결") | (sRealType == "선물시세"):

            processor = int if sCode in self.stocks_code else float

            trade_date = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]["체결시간"])  # hhmmss string 형태

            current_price = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]["현재가"])  # +(-) 2500 string 형태
            current_price = abs(processor(current_price))

            trade_sell_hoga1 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]["(최우선)매도호가"])  # -(+)
            trade_sell_hoga1 = abs(processor(trade_sell_hoga1))

            trade_buy_hoga1 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                self.realType.REALTYPE[sRealType]["(최우선)매수호가"])  # -(+)
            trade_buy_hoga1 = abs(processor(trade_buy_hoga1))

            volume = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                self.realType.REALTYPE[sRealType]["거래량"])  # -(+) 틱봉의 아주작은 거래량들!
            volume = abs(processor(volume))

            cum_volume = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]["누적거래량"])  # -(+)
            cum_volume = abs(processor(cum_volume))

            high = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]["고가"])  # -(+)
            high = abs(processor(high))

            open_price = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]["시가"])  # -(+)
            open_price = abs(processor(open_price))

            low = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]["저가"])  # -(+)
            low = abs(processor(low))


            ###Trade dict update
            update_trade_kiwoom_dict = {
                'code': sCode.strip(),
                'trade_date': trade_date.strip(),
                'timestamp': dt.datetime.now().strftime("%Y%m%d%H%M%S.%f")[:-3],
                'current_price': current_price,
                'open_price': open_price,
                'high': high,
                'low': low,
                'volume': volume,
                'cum_volume': cum_volume,
                'trade_sell_hoga1': trade_sell_hoga1,
                'trade_buy_hoga1': trade_buy_hoga1
            }

            self.kiwoom_stocks_data[sCode.strip()].update(update_trade_kiwoom_dict)

            json_data = json.dumps(self.kiwoom_stocks_data[sCode.strip()])

            if sCode.strip() in self.stocks_code:
                save_kiwoom_stocks_data_to_csv(json_data)
                # kiwoom_stocks_channel.basic_publish(exchange='', routing_key="kiwoom_stocks_data", body=json_data)
            else:
                save_kiwoom_futures_data_to_csv(json_data)
                # kiwoom_futures_channel.basic_publish(exchange='', routing_key="kiwoom_futures_data", body=json_data)


        elif (sRealType == "주식호가잔량") | (sRealType == "주식선물호가잔량") | (sRealType == "선물호가잔량") :
            hoga_date = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]["호가시간"])

            processor = int if sCode in self.stocks_code else float

            ####매도호가
            sell_hoga1 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]["매도호가1"])
            sell_hoga1 = abs(processor(sell_hoga1))

            sell_hoga2 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가2"])
            sell_hoga2 = abs(processor(sell_hoga2))

            sell_hoga3 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가3"])
            sell_hoga3 = abs(processor(sell_hoga3))

            sell_hoga4 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가4"])
            sell_hoga4 = abs(processor(sell_hoga4))

            sell_hoga5 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                          self.realType.REALTYPE[sRealType]["매도호가5"])
            sell_hoga5 = abs(processor(sell_hoga5))

            if (sRealType == "주식호가잔량"):
                sell_hoga6 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                    self.realType.REALTYPE[sRealType]["매도호가6"])
                sell_hoga6 = abs(processor(sell_hoga6))

                sell_hoga7 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                    self.realType.REALTYPE[sRealType]["매도호가7"])
                sell_hoga7 = abs(processor(sell_hoga7))

                sell_hoga8 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                    self.realType.REALTYPE[sRealType]["매도호가8"])
                sell_hoga8 = abs(processor(sell_hoga8))

                sell_hoga9 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                    self.realType.REALTYPE[sRealType]["매도호가9"])
                sell_hoga9 = abs(processor(sell_hoga9))

                sell_hoga10 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                    self.realType.REALTYPE[sRealType]["매도호가10"])
                sell_hoga10 = abs(processor(sell_hoga10))
            else:
                sell_hoga6 = None
                sell_hoga7 = None
                sell_hoga8 = None
                sell_hoga9 = None
                sell_hoga10 = None
            
            
            ###매수호가
            buy_hoga1 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가1"])
            buy_hoga1 = abs(processor(buy_hoga1))

            buy_hoga2 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가2"])
            buy_hoga2 = abs(processor(buy_hoga2))

            buy_hoga3 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가3"])
            buy_hoga3 = abs(processor(buy_hoga3))

            buy_hoga4 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가4"])
            buy_hoga4 = abs(processor(buy_hoga4))

            buy_hoga5 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가5"])
            buy_hoga5 = abs(processor(buy_hoga5))

            if (sRealType == "주식호가잔량"):
                buy_hoga6 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                    self.realType.REALTYPE[sRealType]["매수호가6"])
                buy_hoga6 = abs(processor(buy_hoga6))

                buy_hoga7 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                    self.realType.REALTYPE[sRealType]["매수호가7"])
                buy_hoga7 = abs(processor(buy_hoga7))

                buy_hoga8 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                    self.realType.REALTYPE[sRealType]["매수호가8"])
                buy_hoga8 = abs(processor(buy_hoga8))

                buy_hoga9 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                    self.realType.REALTYPE[sRealType]["매수호가9"])
                buy_hoga9 = abs(processor(buy_hoga9))

                buy_hoga10 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                     self.realType.REALTYPE[sRealType]["매수호가10"])
                buy_hoga10 = abs(processor(buy_hoga10))
            else:
                buy_hoga6 = None
                buy_hoga7 = None
                buy_hoga8 = None
                buy_hoga9 = None
                buy_hoga10 = None




            ####매도호가수량
            sell_hoga1_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]["매도호가수량1"])
            sell_hoga1_stack = abs(processor(sell_hoga1_stack))

            sell_hoga2_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가수량2"])
            sell_hoga2_stack = abs(processor(sell_hoga2_stack))

            sell_hoga3_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가수량3"])
            sell_hoga3_stack = abs(processor(sell_hoga3_stack))

            sell_hoga4_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가수량4"])
            sell_hoga4_stack = abs(processor(sell_hoga4_stack))

            sell_hoga5_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가수량5"])
            sell_hoga5_stack = abs(processor(sell_hoga5_stack))

            if (sRealType == "주식호가잔량"):
                sell_hoga6_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                    self.realType.REALTYPE[sRealType]["매도호가수량6"])
                sell_hoga6_stack = abs(processor(sell_hoga6_stack))

                sell_hoga7_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                    self.realType.REALTYPE[sRealType]["매도호가수량7"])
                sell_hoga7_stack = abs(processor(sell_hoga7_stack))

                sell_hoga8_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                    self.realType.REALTYPE[sRealType]["매도호가수량8"])
                sell_hoga8_stack = abs(processor(sell_hoga8_stack))

                sell_hoga9_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                    self.realType.REALTYPE[sRealType]["매도호가수량9"])
                sell_hoga9_stack = abs(processor(sell_hoga9_stack))

                sell_hoga10_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                     self.realType.REALTYPE[sRealType]["매도호가수량10"])
                sell_hoga10_stack = abs(processor(sell_hoga10_stack))
            else:
                sell_hoga6_stack = None
                sell_hoga7_stack = None
                sell_hoga8_stack = None
                sell_hoga9_stack = None
                sell_hoga10_stack = None



            ###매수호가수량
            buy_hoga1_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가수량1"])
            buy_hoga1_stack = abs(processor(buy_hoga1_stack))

            buy_hoga2_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가수량2"])
            buy_hoga2_stack = abs(processor(buy_hoga2_stack))

            buy_hoga3_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가수량3"])
            buy_hoga3_stack = abs(processor(buy_hoga3_stack))

            buy_hoga4_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가수량4"])
            buy_hoga4_stack = abs(processor(buy_hoga4_stack))

            buy_hoga5_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가수량5"])
            buy_hoga5_stack = abs(processor(buy_hoga5_stack))

            if (sRealType == "주식호가잔량"):
                buy_hoga6_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                    self.realType.REALTYPE[sRealType]["매수호가수량6"])
                buy_hoga6_stack = abs(processor(buy_hoga6_stack))

                buy_hoga7_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                    self.realType.REALTYPE[sRealType]["매수호가수량7"])
                buy_hoga7_stack = abs(processor(buy_hoga7_stack))

                buy_hoga8_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                    self.realType.REALTYPE[sRealType]["매수호가수량8"])
                buy_hoga8_stack = abs(processor(buy_hoga8_stack))

                buy_hoga9_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                    self.realType.REALTYPE[sRealType]["매수호가수량9"])
                buy_hoga9_stack = abs(processor(buy_hoga9_stack))

                buy_hoga10_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                     self.realType.REALTYPE[sRealType]["매수호가수량10"])
                buy_hoga10_stack = abs(processor(buy_hoga10_stack))
            else:
                buy_hoga6_stack = None
                buy_hoga7_stack = None
                buy_hoga8_stack = None
                buy_hoga9_stack = None
                buy_hoga10_stack = None

            

            #####etc
            if (sRealType == "주식호가잔량"):
                total_buy_hoga_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                    self.realType.REALTYPE[sRealType]["매수호가총잔량"])
                total_buy_hoga_stack = abs(int(total_buy_hoga_stack))

                total_sell_hoga_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                    self.realType.REALTYPE[sRealType]["매도호가총잔량"])
                total_sell_hoga_stack = abs(int(total_sell_hoga_stack))

                net_buy_hoga_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                              self.realType.REALTYPE[sRealType]["순매수잔량"])
                net_buy_hoga_stack = abs(int(net_buy_hoga_stack))

                net_sell_hoga_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                              self.realType.REALTYPE[sRealType]["순매도잔량"])
                net_sell_hoga_stack = abs(int(net_sell_hoga_stack))

                ratio_buy_hoga_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                       self.realType.REALTYPE[sRealType]["매수비율"])
                ratio_buy_hoga_stack = abs(float(ratio_buy_hoga_stack))

                ratio_sell_hoga_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                        self.realType.REALTYPE[sRealType]["매도비율"])
                ratio_sell_hoga_stack = abs(float(ratio_sell_hoga_stack))
            else:
                total_buy_hoga_stack = None
                total_sell_hoga_stack = None
                net_buy_hoga_stack = None
                net_sell_hoga_stack = None
                ratio_buy_hoga_stack = None
                ratio_sell_hoga_stack = None

            ###hoga dict update
            update_hoga_kiwoom_dict = {
                'code': sCode.strip(),
                'hoga_date': hoga_date,
                'timestamp': dt.datetime.now().strftime("%Y%m%d%H%M%S.%f")[:-3],
                'sell_hoga10': sell_hoga10,
                'sell_hoga9': sell_hoga9,
                'sell_hoga8': sell_hoga8,
                'sell_hoga7': sell_hoga7,
                'sell_hoga6': sell_hoga6,
                'sell_hoga5': sell_hoga5,
                'sell_hoga4': sell_hoga4,
                'sell_hoga3': sell_hoga3,
                'sell_hoga2': sell_hoga2,
                'sell_hoga1': sell_hoga1,
                'buy_hoga1': buy_hoga1,
                'buy_hoga2': buy_hoga2,
                'buy_hoga3': buy_hoga3,
                'buy_hoga4': buy_hoga4,
                'buy_hoga5': buy_hoga5,
                'buy_hoga6': buy_hoga6,
                'buy_hoga7': buy_hoga7,
                'buy_hoga8': buy_hoga8,
                'buy_hoga9': buy_hoga9,
                'buy_hoga10': buy_hoga10,
                'sell_hoga10_stack': sell_hoga10_stack,
                'sell_hoga9_stack': sell_hoga9_stack,
                'sell_hoga8_stack': sell_hoga8_stack,
                'sell_hoga7_stack': sell_hoga7_stack,
                'sell_hoga6_stack': sell_hoga6_stack,
                'sell_hoga5_stack': sell_hoga5_stack,
                'sell_hoga4_stack': sell_hoga4_stack,
                'sell_hoga3_stack': sell_hoga3_stack,
                'sell_hoga2_stack': sell_hoga2_stack,
                'sell_hoga1_stack': sell_hoga1_stack,
                'buy_hoga1_stack': buy_hoga1_stack,
                'buy_hoga2_stack': buy_hoga2_stack,
                'buy_hoga3_stack': buy_hoga3_stack,
                'buy_hoga4_stack': buy_hoga4_stack,
                'buy_hoga5_stack': buy_hoga5_stack,
                'buy_hoga6_stack': buy_hoga6_stack,
                'buy_hoga7_stack': buy_hoga7_stack,
                'buy_hoga8_stack': buy_hoga8_stack,
                'buy_hoga9_stack': buy_hoga9_stack,
                'buy_hoga10_stack': buy_hoga10_stack,
                'total_buy_hoga_stack': total_buy_hoga_stack,
                'total_sell_hoga_stack': total_sell_hoga_stack,
                'net_buy_hoga_stack': net_buy_hoga_stack,
                'net_sell_hoga_stack': net_sell_hoga_stack,
                'ratio_buy_hoga_stack': ratio_buy_hoga_stack,
                'ratio_sell_hoga_stack': ratio_sell_hoga_stack
            }

            self.kiwoom_stocks_data[sCode.strip()].update(update_hoga_kiwoom_dict)

            json_data = json.dumps(self.kiwoom_stocks_data[sCode.strip()])

            if sCode.strip() in self.stocks_code:
                save_kiwoom_stocks_data_to_csv(json_data)
                # kiwoom_stocks_channel.basic_publish(exchange='', routing_key="kiwoom_stocks_data", body=json_data)
            else:
                save_kiwoom_futures_data_to_csv(json_data)
                # kiwoom_futures_channel.basic_publish(exchange='', routing_key="kiwoom_futures_data", body=json_data)

    def get_code_list_by_market(self, market_code):
        '''
        종목코드 반환  (개발가이드 > 기타함수> 종목정보관련함수)
        :param market_code: 장내: 0 코스닥: 10
        :return:
        '''
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market_code)
        code_list = code_list.split(";")[:-1]

        return code_list

    def get_futures_code_list(self, blank):

        stock_futures_code_list = self.dynamicCall("GetSFutureList(Qstring, int)", blank)
        stock_futures_code_list = stock_futures_code_list.split("|") #[:-1]
        stock_futures_code_list = list(map(lambda x: x.split('^')[0],stock_futures_code_list))

        fu_code_ls = list(set(map(lambda x: x[1:3], stock_futures_code_list)))[1:] # "" 공백 원소 건너뛰기

        total_fu_code = []
        for fu_code in fu_code_ls:
            tmp = []
            for i in range(len(stock_futures_code_list)):
                fu_code_i = stock_futures_code_list[i][1:3]
                if fu_code_i == fu_code:
                    tmp.append(stock_futures_code_list[i])
                else:
                    pass
            total_fu_code.append(tmp)

        total_fu_code = list(map(lambda x: x[:3], total_fu_code)) #더 원월물까지 포함하고 싶으면 3을 바꾸면됨

        flatten_fu_code = []
        for fu_code in total_fu_code:
            flatten_fu_code = flatten_fu_code + fu_code

        return flatten_fu_code

    def get_futures_index_list(self):

        fu_idx_list = self.dynamicCall("GetFutureList()")
        fu_idx_list = fu_idx_list.split(";")[:-1]

        fu_idx = list(set(map(lambda x: x[1:3], fu_idx_list))) # "" 공백 원소 건너뛰기
        total_fu_idx_code = []
        for fu_code in fu_idx:
            tmp = []
            for i in range(len(fu_idx_list)):
                fu_code_i = fu_idx_list[i][1:3]
                if fu_code_i == fu_code:
                    tmp.append(fu_idx_list[i])
                else:
                    pass
            total_fu_idx_code.append(tmp)

        total_fu_idx_code = list(map(lambda x: x[:3], total_fu_idx_code))  # 더 원월물까지 포함하고 싶으면 3을 바꾸면됨

        flatten_fu_idx_code = []
        for fu_code in total_fu_idx_code:
            flatten_fu_idx_code = flatten_fu_idx_code + fu_code


        return flatten_fu_idx_code
