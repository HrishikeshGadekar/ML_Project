#!/home/busportal/Music/pypy3.5-v7.0.0-linux64/bin/pypy3
from seleniumWebService import  seleniumWebService as sws
import time
import Epoch as E
from pandas import datetime
from stringInString import stringInString as S
import mysql.connector as msc
import json
import re
import os
try:
    conn = msc.connect(host='localhost', user='root', password='transpolinux', database='test')
    cur = conn.cursor()
except:
    conn = msc.connect(host='localhost', user='root', password='iitm', database='test')
    cur = conn.cursor()

class googMapsDataGet ( sws  ):

    def printMethod(func ):
        def wrapper( *args , **kwargs ):
            y = func( *args , **kwargs)
            print( y )
            return y
        return wrapper
    def DataGet ( cls ,  Url  ):
        cls.openBrowser( Url )
        data1 = cls.Browser.find_element_by_tag_name('jsl').text
        cls.closeBrowser()
        cls.openBrowser( googMapsDataGet.urlLNtoDAT(Url) )
        data2 = cls.Browser.find_element_by_tag_name('jsl').text
        cls.closeBrowser()
        return [data1 , data2 ]
    #@printMethod
    def processData (self,  Data , route  ) :
        query = 'insert into gMapsData'+route +'(CurrentTime ,TTNow , TT30 )Values(' + '"' + datetime.strftime(
            datetime.now(), "%d-%m-%y  %H:%M") + '"' + "," + S(re.findall('[0-9]*\smin', Data[0])[0]) + ","
        try:
            query = query + S(re.findall('typically\s[0-9]*\s-\s[0-9]*\smin', Data[1])[0].split('typically ')[1]) + ")"
        except:
            query = query + S(re.findall('typically\s[0-9]*\smin', Data[1])[0].split('typically ')[1]) + ")"
        cur.execute(query)
        conn.commit()

    def tableCreateifNotAvail(self , tableName ):
        query = googMapsDataGet.query(tableName)
        cur.execute(query)
        conn.commit()
    def mainFlow(self ):
        os.chdir('/home/busportal/Desktop/transportAnalysis/googleMapsProj')
        self.S = googMapsDataGet.stretchRead()
        for each in self.S:
            self.tableCreateifNotAvail(each[0])
            self.processData (self.DataGet(each[1]) , each[0])
        conn.close()

    #@printMethod
    def query (route):
        sql = """create table if not exists gMapsData"""+route+"""(ID int auto_increment , 
        CurrentTime varchar(250) ,TTNow varchar(250) ,TT30 varchar(250), primary key(ID))"""
        return sql
    #@printMethod
    def stretchRead():
        with open( 'stretchesURL' , 'r') as file :
            data = json.loads( file.read())
        return data
    @printMethod
    def urlLNtoDAT(LeavNow):
        Head = LeavNow.split('data=')[0]+'data=!3m1!4b1!4m6!4m5!2m3!6e0!7e2!8j'
        Tail =  str(E.EpochtimeCurrent() + 1800 )+ "!3e0?hl=en"
        return Head + Tail
#"https://www.google.com/maps/dir/13.01232,80.22695/12.97533,80.22082/@12.9947204,80.2047328,14z/data=!4m2!4m1!3e0?hl=en"
#https://www.google.com/maps/dir/13.01232,80.22695/12.97533,80.22082/@12.9938533,80.2047327,14z/data=!3m1!4b1!4m6!4m5!2m3!6e0!7e2!8j1556878800!3e0?hl=en
#"https://www.google.co.in/maps/dir/13.0086106,80.2318974/13.0066961,80.2459096/@13.0053027,80.2428825,17z/data=!4m2!4m1!3e0?hl=en"
G = googMapsDataGet()
import time

# G.mainFlow()



G.mainFlow()
