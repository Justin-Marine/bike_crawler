# -*- coding: utf-8 -*-

### with 문 사용
import psycopg2 as pg
import pandas as pd

class execl_to_post:

    host = ""
    dbname = ""
    user = ""
    password = ""

    def __init__(self, host, dbname, user, password):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password

    def execl_to_postgis(self, inputexcel, sheetname):

        data = pd.read_excel(inputexcel,sheetname)

        conn = None 
        try: 
            with pg.connect("host={hst} dbname={dn} user={usr} password={pwd}".format(hst= self.host, dn=self.dbname, usr= self.user, pwd= self.password)) as conn:
                with conn.cursor() as cur: 
                    conn.autocommit = True 

                    cur.execute('drop table if exists bike;')
                    cur.execute('create table bike (id Serial, bid bigint, dname text, bcounts int, address text, latitude float, longitude float, geom geometry(Point, 4326)) with(OIDS=FALSE);')

                    for i,j in data.iterrows():
                        sql= "insert into bike (bid, dname, bcounts, address, latitude, longitude, geom)\
                            values ({bd}, '{name}', {bcounts}, '{address}', {lati}, {longi}, ST_SetSRID(ST_MakePoint({longi}, {lati}), 4326))".format(bd=data.bid[i],
                            name= data.Rent_name[i],
                            bcounts= data.bcnts[i],
                            address= data.address[i],
                            lati= data.latitude[i],
                            longi= data.logitude[i])
                        cur.execute(sql)
                        #rows = cur.fetchall() 
        except Exception as e: 
            print ('Error : ', e )

        # else: 
            #print (rows)
            # exit() 

        finally: 
            if conn: conn.close()

if __name__ == "__main__":
    #연결정보 입력
    host = input("Host 정보입력:")
    dbname = input("dbname 정보입력:")
    user = input("user 정보입력:")
    password = input("password 정보입력:")

    cdb = execl_to_post(host, dbname, user, password)
    print (host, dbname, user, password)

    excel_name = input("Excel name 정보입력(경로):")
    sheet_name = input("sheet name 정보입력:")
    cdb.execl_to_postgis(excel_name,sheet_name)