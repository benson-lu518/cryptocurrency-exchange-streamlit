#tradedao
import sqlite3 
conn = sqlite3.connect('data.db',check_same_thread=False)
# conn.row_factory =sqlite3.Row #dictionary cursor
import pandas as pd 
c = conn.cursor()
class TradingDao:
    def insetTradingInfo(username,box01,convert,quantity,price1,dt2):
        c.execute('INSERT INTO tradinginfo (username,currency,amount,quantity,price,createddate) VALUES (?,?,?,?,?,?)',(username,box01,convert,quantity,price1,dt2))
        conn.commit()

    def getAllHistoryByUsername(username,start_date,end_date):
        #return pd dataframe
        sql="SELECT username,currency,amount,quantity,price,createddate "\
        "FROM tradinginfo WHERE username = '{}' AND createddate BETWEEN '{}' AND '{}' ORDER BY createddate DESC".format(username,start_date,end_date)
        dataframe =pd.read_sql_query(sql,conn)
        return dataframe
            
    def getAllHistoryByUsernameCurrency(username,currency,start_date,end_date):
        #return pd dataframe
        sql="SELECT username,currency,amount,quantity,price,createddate "\
        "FROM tradinginfo WHERE username = '{}' AND currency='{}' AND createddate BETWEEN '{}' AND '{}' ORDER BY createddate DESC".format(username,currency,start_date,end_date)
        dataframe =pd.read_sql_query(sql,conn)
        return dataframe
   
    def getAllCurrency(username):
      #retrun list first row
        conn.row_factory = lambda cursor, row: row[0] #expected only one row 
        c = conn.cursor()
        c.execute('select DISTINCT (currency) from tradinginfo where username=?',(username,))
        currencyList=c.fetchall()
        conn.row_factory = None
        return currencyList
    