# -*- coding: utf-8 -*-
"""
Created on Sat Mar 2 17:33: 2019

@author: Justin
"""
import os, sys, datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
# import bike2db

form_class = uic.loadUiType("bike.ui")[0]
locations = []

urla='https://www.bikeseoul.com/app/station/moveStationSearchView.do?currentPageNo='
urlb='&stationGrpSeq=#'
header = ['bid','Rent_name','bcnt','address','latitude','logitude']

class MyWindow(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('icon.png'))
        self.setupUi(self)
        print('init!')
        

        self.btn_extract.clicked.connect(self.crawl)
        self.btn_export.clicked.connect(self.get_result)
        #self.stat_qpb.setTextVisible(False)
        #self.btn_extract.clicked.connect(self.tqEvent)

    def crawl(self):
        start = int(self.arg_start.text())
        limit = int(self.arg_limit.text())
        self.stat_qpb.setMinimum(start)
        self.stat_qpb.setMaximum(limit)
        # if os.path.exists('seoulbike.csv'): os.remove('seoulbike.csv')
        # if os.path.exists('seoulbike.txt'): os.remove('seoulbike.txt')

        self.lb_start.setStyleSheet('QLabel#lb_start {color : black}')

        if start > limit:
            self.lb_start.setStyleSheet('QLabel#lb_start {color : red}')
        else:
            for n in range(start,limit+1):
                numer = n
                t = str(numer)

                siteOpen = urllib.request.urlopen(urla+t+urlb)
                soup = BeautifulSoup(siteOpen, 'html.parser')
                loc_table = soup.select('table.psboard1 > tbody')[0].find_all('tr')

                for row in loc_table:
                        loc_info = []
                        # <번호. 대여소명>
                        loc_name = row.select('td.pl10')[0].get_text(strip=True)
                        if '.' in loc_name:
                            loc_info.append(loc_name.split('.')[0]) # 번호
                            loc_info.append(loc_name.split('.')[-1].lstrip()) # 대여소명
                        else:
                            loc_info.append('n/a') # 번호가 없는 경우 'n/a'으로 처리
                            loc_info.append(loc_name)
                        # 거치대수
                        loc_info.append(row.select('td.tr')[0].get_text(strip=True))
                        # 주소
                        loc_info.append(row.select('td.mhid')[0].get_text(strip=True))
                        # 위도, 경도 좌표
                        loc_geo = row.find('a')['param-data'].split(',')
                        loc_info.append(loc_geo[0])
                        loc_info.append(loc_geo[1])
                        # point geom 데이터로 입력
                        # loc_geom = 'Point({xpos}, {ypos})'.format(xpos=loc_geo[0],ypos=loc_geo[1])
                        # loc_info.append(loc_geom)

                        # 리스트에 location 추가
                        locations.append(loc_info)

                # progress bar status        
                self.stat_qpb.setValue(n)
            
            # button extract단 비활성화, export단 활성화
            self.btn_extract.setEnabled(False)
            self.arg_start.setEnabled(False)
            self.arg_limit.setEnabled(False)

            self.btn_export.setEnabled(True)
            self.chk_exl.setEnabled(True)
            # self.chk_db.setEnabled(True)

    def get_result(self):
        if self.chk_exl.isChecked() == True:
            #locations.sort()
            df = pd.DataFrame.from_records(locations, columns = header)
            # 엑셀파일로 추출
            execl_name = 'seoulbike_{df}.xlsx'.format(df=datetime.datetime.now().strftime("%Y%m%d"))
            df.to_excel(execl_name, sheet_name='bike', encoding = 'utf-8', index=False)

            if self.chk_db.isChecked() == True:
                # DB연결정보 입력 활성화

                # DB에 push
                pass
                # cdb = bike2db.execl_to_post('','','','')
                # cdb.execl_to_postgis('seoulbike.xlsx','bike')
                

        self.btn_export.setEnabled(False)
        self.btn_extract.setEnabled(True)
        self.chk_db.setEnabled(False)
        self.chk_exl.setEnabled(False)
        self.arg_start.setEnabled(True)
        self.arg_limit.setEnabled(True)
        self.stat_qpb.reset()

        locations.clear()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()


    # _날짜로 저장기능 
    # cancel기능 
    # 쓰레드