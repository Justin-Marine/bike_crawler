# -*- coding: utf-8 -*-
"""
Created on Thu May  3 23:40:20 2018

@author: Justin
"""

from tqdm import tqdm # 진행률 표시
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd


print('마지막 페이지수?')
limit = input()
limit = int(limit)
locations = []

urla='https://www.bikeseoul.com/app/station/moveStationSearchView.do?currentPageNo='
urlb='&stationGrpSeq=#'
header = ['bid','rentname','bcnts','address','latitude','longitude']

for n in tqdm(range(1,limit+1)):
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
    
# csv파일로 추출
df = pd.DataFrame.from_records(locations, columns = header)
df.to_csv('seoulbike.csv', index=False)