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
import bike2db

form_class = uic.loadUiType("bike.ui")[0]
locations = []

urla='https://www.bikeseoul.com/app/station/moveStationSearchView.do?currentPageNo='
header = ['bid','Rent_name','bcnt','address','latitude','logitude']

class MyWindow(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('icon.png'))
        self.setupUi(self)

        self.btn_extract.clicked.connect(self.crawl)
        self.btn_export.clicked.connect(self.get_result)
        self.chk_db.clicked.connect(self.verify_db_chk)
        #self.stat_qpb.setTextVisible(False)
        #self.btn_extract.clicked.connect(self.tqEvent)

    def crawl(self):
        start = int(self.arg_start.text())
        limit = int(self.arg_limit.text())
        self.stat_qpb.setMinimum(start)
        self.stat_qpb.setMaximum(limit)

        self.lb_start.setStyleSheet('QLabel#lb_start {color : black}')
        self.memory.setText('None in memory')
        self.memory.setEnabled(False)
        self.stat_qpb.setRange(start,limit+1)

        if start > limit:
            self.lb_start.setStyleSheet('QLabel#lb_start {color : red}')
        else:
            for lps in range(start,limit+1):
                page = str(lps)

                siteOpen = urllib.request.urlopen(urla+page)
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
                self.stat_qpb.setValue(lps+1)
            
            # button extract단 비활성화, export단 활성화
            # self.btn_extract.setEnabled(False)
            # self.arg_start.setEnabled(False)
            # self.arg_limit.setEnabled(False)
            self.memory.setText('P{s} ~ P{e} in memory'.format(s= start, e= limit))
            self.memory.setEnabled(True)

            self.btn_export.setEnabled(True)
            self.chk_exl.setEnabled(True)
            self.chk_db.setEnabled(True)
            self.verify_db_chk()
                
    def verify_db_chk(self):
        if self.chk_db.isChecked() == True:
            self.host.setEnabled(True)
            self.db.setEnabled(True)
            self.user.setEnabled(True)
            self.pw.setEnabled(True)
            self.host_ipt.setEnabled(True)
            self.db_ipt.setEnabled(True)
            self.user_ipt.setEnabled(True)
            self.pw_ipt.setEnabled(True)
        else:
            self.disable_dbs()

    def disable_dbs(self):
        self.host.setEnabled(False)
        self.db.setEnabled(False)
        self.user.setEnabled(False)
        self.pw.setEnabled(False)
        self.host_ipt.setEnabled(False)
        self.db_ipt.setEnabled(False)
        self.user_ipt.setEnabled(False)
        self.pw_ipt.setEnabled(False)

    def get_result(self):
        if self.chk_exl.isChecked() == True:
            df = pd.DataFrame.from_records(locations, columns = header)
            # 엑셀파일로 추출
            execl_name = 'seoulbike_{df}.xlsx'.format(df=datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
            df.to_excel(execl_name, sheet_name='bike', encoding = 'utf-8', index=False)

            if self.chk_db.isChecked() == True:
                # DB연결정보 입력 활성화

                # DB에 push
                cdb = bike2db.execl_to_post(self.host_ipt.text(), self.db_ipt.text(), self.user_ipt.text(), self.pw_ipt.text())
                cdb.execl_to_postgis(execl_name,'bike')
                
        # 버튼 상태 초기화
        # self.btn_export.setEnabled(False)
        # self.btn_extract.setEnabled(True)
        # self.chk_db.setEnabled(False)
        # self.chk_exl.setEnabled(False)
        self.arg_start.setEnabled(True)
        self.arg_limit.setEnabled(True)
        self.stat_qpb.reset()
        self.disable_dbs()

        locations.clear()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()

    # cancel 기능 
    # 쓰레드