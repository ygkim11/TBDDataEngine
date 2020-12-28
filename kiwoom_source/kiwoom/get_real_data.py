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

from dotenv import load_dotenv
import pika

load_dotenv()

RABBIT_HOST = os.getenv('RABBIT_HOST', 'localhost')
RABBIT_USER = os.getenv('RABBIT_USER', 'guest')
RABBIT_PASS = os.getenv('RABBIT_PASS', 'guest')

credentials = pika.PlainCredentials(username=RABBIT_USER, password=RABBIT_PASS)
conn = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST, credentials=credentials))

kiwoom_stocks_channel = conn.channel()
kiwoom_stocks_channel.queue_declare(queue='kiwoom_stocks_data')

kiwoom_futures_channel = conn.channel()
kiwoom_futures_channel.queue_declare(queue='kiwoom_futures_data')

class Get_Real_Data(QAxWidget):
    def __init__(self):

        super().__init__()

        print("#"*6 , "Kiwoom Class initiated" , "#"*6)

        # self.stocks_futures_code = ["111R1000"]  # 삼성 선물 example
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
                'timestamp' : None,
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
            trade_date = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]["체결시간"])  # hhmmss string 형태

            current_price = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]["현재가"])  # +(-) 2500 string 형태
            current_price = str(abs(int(current_price)))

            # c = self.dynamicCall("GetCommRealData(QString, int)", sCode,
            #                      self.realType.REALTYPE[sRealType]["전일대비"])  # -(+)
            # c = abs(int(c))
            #
            # d = self.dynamicCall("GetCommRealData(QString, int)", sCode,
            #                      self.realType.REALTYPE[sRealType]["등락율"])  # -(+)
            # d = float(d)

            trade_sell_hoga1 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]["(최우선)매도호가"])  # -(+)
            trade_sell_hoga1 = abs(int(trade_sell_hoga1))

            trade_buy_hoga1 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]["(최우선)매수호가"])  # -(+)
            trade_buy_hoga1 = abs(int(trade_buy_hoga1))

            volume = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]["거래량"])  # -(+) 틱봉의 아주작은 거래량들!
            volume = str(abs(int(volume)))

            cum_volume = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]["누적거래량"])  # -(+)
            cum_volume = str(abs(int(cum_volume)))

            high = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]["고가"])  # -(+)
            high = str(abs(int(high)))

            open_price = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]["시가"])  # -(+)
            open_price = str(abs(int(open_price)))

            low = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]["저가"])  # -(+)
            low = str(abs(int(low)))


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

            # data = []
            #
            # data.append(sCode.strip())
            # data.append(date.strip())
            # data.append(current_price)
            # data.append(open_price)
            # data.append(high)
            # data.append(low)
            # data.append(volume)
            # data.append(cum_volume)
            # data.append(trade_sell_hoga1)
            # data.append(trade_buy_hoga1)

            #print(data)

            json_data = json.dumps(self.kiwoom_stocks_data[sCode.strip()])
            # print(json_data)

            # if sCode.strip() in self.stocks_code:
            #     kiwoom_stocks_channel.basic_publish(exchange='', routing_key="kiwoom_stocks_data", body=json_data)
            # else:
            #     kiwoom_futures_channel.basic_publish(exchange='', routing_key="kiwoom_futures_data", body=json_data)



            # tick_csv = open("./db/real_tick_data.csv", "a", newline="", encoding="utf8")
            #
            # with tick_csv:
            #     # self.header = [['date', 'close', 'open', 'high', 'low', 'volume', 'trade_volume', 'sujung_ratio', 'sujung_gubun']]
            #     write = csv.writer(tick_csv)
            #     # write.writerows(self.header)
            #     write.writerows([data])
            #
            # tick_csv.close()


        elif (sRealType == "주식호가잔량") | (sRealType == "주식선물호가잔량") :
            hoga_date = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]["호가시간"])

            ####매도호가
            sell_hoga1 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]["매도호가1"])
            sell_hoga1 = abs(int(sell_hoga1))

            sell_hoga2 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가2"])
            sell_hoga2 = abs(int(sell_hoga2))

            sell_hoga3 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가3"])
            sell_hoga3 = abs(int(sell_hoga3))

            sell_hoga4 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가4"])
            sell_hoga4 = abs(int(sell_hoga4))

            sell_hoga5 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가5"])
            sell_hoga5 = abs(int(sell_hoga5))

            sell_hoga6 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가6"])
            sell_hoga6 = abs(int(sell_hoga6))

            sell_hoga7 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가7"])
            sell_hoga7 = abs(int(sell_hoga7))

            sell_hoga8 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가8"])
            sell_hoga8 = abs(int(sell_hoga8))

            sell_hoga9 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가9"])
            sell_hoga9 = abs(int(sell_hoga9))

            sell_hoga10 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가10"])
            sell_hoga10 = abs(int(sell_hoga10))
            
            
            ###매수호가
            buy_hoga1 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가1"])
            buy_hoga1 = abs(int(buy_hoga1))

            buy_hoga2 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가2"])
            buy_hoga2 = abs(int(buy_hoga2))

            buy_hoga3 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가3"])
            buy_hoga3 = abs(int(buy_hoga3))

            buy_hoga4 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가4"])
            buy_hoga4 = abs(int(buy_hoga4))

            buy_hoga5 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가5"])
            buy_hoga5 = abs(int(buy_hoga5))

            buy_hoga6 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가6"])
            buy_hoga6 = abs(int(buy_hoga6))

            buy_hoga7 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가7"])
            buy_hoga7 = abs(int(buy_hoga7))

            buy_hoga8 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가8"])
            buy_hoga8 = abs(int(buy_hoga8))

            buy_hoga9 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가9"])
            buy_hoga9 = abs(int(buy_hoga9))

            buy_hoga10 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                 self.realType.REALTYPE[sRealType]["매수호가10"])
            buy_hoga10 = abs(int(buy_hoga10))


            ####매도호가수량
            sell_hoga1_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]["매도호가수량1"])
            sell_hoga1_stack = abs(int(sell_hoga1_stack))

            sell_hoga2_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가수량2"])
            sell_hoga2_stack = abs(int(sell_hoga2_stack))

            sell_hoga3_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가수량3"])
            sell_hoga3_stack = abs(int(sell_hoga3_stack))

            sell_hoga4_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가수량4"])
            sell_hoga4_stack = abs(int(sell_hoga4_stack))

            sell_hoga5_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가수량5"])
            sell_hoga5_stack = abs(int(sell_hoga5_stack))

            sell_hoga6_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가수량6"])
            sell_hoga6_stack = abs(int(sell_hoga6_stack))

            sell_hoga7_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가수량7"])
            sell_hoga7_stack = abs(int(sell_hoga7_stack))

            sell_hoga8_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가수량8"])
            sell_hoga8_stack = abs(int(sell_hoga8_stack))

            sell_hoga9_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가수량9"])
            sell_hoga9_stack = abs(int(sell_hoga9_stack))

            sell_hoga10_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매도호가수량10"])
            sell_hoga10_stack = abs(int(sell_hoga10_stack))


            ###매수호가수량
            buy_hoga1_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가수량1"])
            buy_hoga1_stack = abs(int(buy_hoga1_stack))

            buy_hoga2_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가수량2"])
            buy_hoga2_stack = abs(int(buy_hoga2_stack))

            buy_hoga3_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가수량3"])
            buy_hoga3_stack = abs(int(buy_hoga3_stack))

            buy_hoga4_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가수량4"])
            buy_hoga4_stack = abs(int(buy_hoga4_stack))

            buy_hoga5_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가수량5"])
            buy_hoga5_stack = abs(int(buy_hoga5_stack))

            buy_hoga6_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가수량6"])
            buy_hoga6_stack = abs(int(buy_hoga6_stack))

            buy_hoga7_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가수량7"])
            buy_hoga7_stack = abs(int(buy_hoga7_stack))

            buy_hoga8_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가수량8"])
            buy_hoga8_stack = abs(int(buy_hoga8_stack))

            buy_hoga9_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                self.realType.REALTYPE[sRealType]["매수호가수량9"])
            buy_hoga9_stack = abs(int(buy_hoga9_stack))

            buy_hoga10_stack = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                 self.realType.REALTYPE[sRealType]["매수호가수량10"])
            buy_hoga10_stack = abs(int(buy_hoga10_stack))
            

            #####etc
            if sRealType == "주식선물호가잔량":
                total_buy_hoga_stack = None
                total_sell_hoga_stack = None
                net_buy_hoga_stack = None
                net_sell_hoga_stack = None
                ratio_buy_hoga_stack = None
                ratio_sell_hoga_stack = None

            else:
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


            # ###데이터 정리
            #
            # tmp_hoga = []
            # tmp_hoga_etc = []
            #
            # tmp_hoga.append(sCode.strip())
            # tmp_hoga.append(hoga_date)
            # #호가
            # tmp_hoga.append(sell_hoga10)
            # tmp_hoga.append(sell_hoga9)
            # tmp_hoga.append(sell_hoga8)
            # tmp_hoga.append(sell_hoga7)
            # tmp_hoga.append(sell_hoga6)
            # tmp_hoga.append(sell_hoga5)
            # tmp_hoga.append(sell_hoga4)
            # tmp_hoga.append(sell_hoga3)
            # tmp_hoga.append(sell_hoga2)
            # tmp_hoga.append(sell_hoga1)
            # tmp_hoga.append(buy_hoga1)
            # tmp_hoga.append(buy_hoga2)
            # tmp_hoga.append(buy_hoga3)
            # tmp_hoga.append(buy_hoga4)
            # tmp_hoga.append(buy_hoga5)
            # tmp_hoga.append(buy_hoga6)
            # tmp_hoga.append(buy_hoga7)
            # tmp_hoga.append(buy_hoga8)
            # tmp_hoga.append(buy_hoga9)
            # tmp_hoga.append(buy_hoga10)
            # #호가잔량
            # tmp_hoga.append(sell_hoga10_stack)
            # tmp_hoga.append(sell_hoga9_stack)
            # tmp_hoga.append(sell_hoga8_stack)
            # tmp_hoga.append(sell_hoga7_stack)
            # tmp_hoga.append(sell_hoga6_stack)
            # tmp_hoga.append(sell_hoga5_stack)
            # tmp_hoga.append(sell_hoga4_stack)
            # tmp_hoga.append(sell_hoga3_stack)
            # tmp_hoga.append(sell_hoga2_stack)
            # tmp_hoga.append(sell_hoga1_stack)
            # tmp_hoga.append(buy_hoga1_stack)
            # tmp_hoga.append(buy_hoga2_stack)
            # tmp_hoga.append(buy_hoga3_stack)
            # tmp_hoga.append(buy_hoga4_stack)
            # tmp_hoga.append(buy_hoga5_stack)
            # tmp_hoga.append(buy_hoga6_stack)
            # tmp_hoga.append(buy_hoga7_stack)
            # tmp_hoga.append(buy_hoga8_stack)
            # tmp_hoga.append(buy_hoga9_stack)
            # tmp_hoga.append(buy_hoga10_stack)
            #
            # #Etc.
            # tmp_hoga_etc.append(sCode.strip())
            # tmp_hoga_etc.append(total_buy_hoga_stack)
            # tmp_hoga_etc.append(total_sell_hoga_stack)
            # tmp_hoga_etc.append(net_buy_hoga_stack)
            # tmp_hoga_etc.append(net_sell_hoga_stack)
            # tmp_hoga_etc.append(ratio_buy_hoga_stack)
            # tmp_hoga_etc.append(ratio_sell_hoga_stack)

            # print(tmp_hoga)
            # print(tmp_hoga_etc)

            json_data = json.dumps(self.kiwoom_stocks_data[sCode.strip()])
            print(json_data)
            # if sCode.strip() in self.stocks_code:
            #     kiwoom_stocks_channel.basic_publish(exchange='', routing_key="kiwoom_stocks_data", body=json_data)
            # else:
            #     kiwoom_futures_channel.basic_publish(exchange='', routing_key="kiwoom_futures_data", body=json_data)


            # hoga_csv = open("./db/real_hoga_data.csv", "a", newline="", encoding="utf8")
            #
            # with hoga_csv:
            #     # self.header = [['date', 'close', 'open', 'high', 'low', 'volume', 'trade_volume', 'sujung_ratio', 'sujung_gubun']]
            #     write = csv.writer(hoga_csv)
            #     # write.writerows(self.header)
            #     write.writerows([tmp_hoga])
            #
            # # hoga_csv.close()


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
        total_fu_code = np.array(total_fu_code).reshape(1,-1)[0].tolist()
        # total_fu_code = li
        return total_fu_code