import sqlite3 
import pandas as pd 
conn = sqlite3.connect('data.db',check_same_thread=False)
# conn.row_factory =sqlite3.Row #dictionary cursor
c = conn.cursor()
class HoldingDao:
    def getHoldingInfo(username,currency):
        #default return list[tuple(,)]
        c.execute('SELECT * FROM holdinginfo WHERE username =? AND currency=?',(username,currency,))
        userInfo=c.fetchall()
        return userInfo

    def getHoldingInfoDict(username,currency):
        #return dict
        #oldest transaction will show first
        conn.row_factory =sqlite3.Row #dictionary cursor
        c = conn.cursor()
        c.execute('SELECT * FROM holdinginfo WHERE username =? AND currency=? ORDER BY createddate ASC',(username,currency,))
        userInfo=c.fetchall()
        conn.row_factory = None
        return userInfo
    

    def getTotalQuantity(username,currency):
        #return float totalquantity
        conn.row_factory =sqlite3.Row #dictionary cursor
        c = conn.cursor()
        c.execute('SELECT * FROM holdinginfo WHERE username =? AND currency=?',(username,currency,))
        userInfo=c.fetchall()
        totalQuantity=0
        for i in userInfo:
            totalQuantity+=i['quantity']
        conn.row_factory = None

        return totalQuantity

    def insertNewRow(username,box01,convert,quantity,price1,createddate,lastupdateddate):
        c.execute('INSERT INTO holdinginfo (username,currency,amount,quantity,boughtprice,createddate,lastupdateddate) VALUES (?,?,?,?,?,?,?)',(username,box01,convert,quantity,price1,createddate,lastupdateddate))
        conn.commit()

    def deleteRowByholding_id(holding_id):
        c.execute('DELETE FROM holdinginfo WHERE holding_id=?',(holding_id,))
        conn.commit()

    def updateQuantity(quantity,amount,lastupdateddate,holding_id):
        c.execute('UPDATE holdinginfo SET quantity=?, amount=?,lastupdateddate=? WHERE holding_id=?',(quantity,amount,lastupdateddate ,holding_id))
        conn.commit()

    
    def getAllHistoryByUsername(username,start_date,end_date):
        #return pd dataframe
        sql="SELECT username,currency,amount,quantity,boughtprice as price,createddate "\
        "FROM holdinginfo WHERE username = '{}' AND createddate BETWEEN '{}' AND '{}' ORDER BY currency, createddate DESC".format(username,start_date,end_date)
        dataframe =pd.read_sql_query(sql,conn)
        return dataframe
            
    def getAllHistoryByUsernameCurrency(username,currency,start_date,end_date):
        #return pd dataframe
        sql="SELECT username,currency,amount,quantity,boughtprice as price,createddate "\
        "FROM holdinginfo WHERE username = '{}' AND currency='{}' AND createddate BETWEEN '{}' AND '{}' ORDER BY currency, createddate DESC".format(username,currency,start_date,end_date)
        dataframe =pd.read_sql_query(sql,conn)
        return dataframe
   
    def getAllCurrency(username):
      #retrun list first row
        conn.row_factory = lambda cursor, row: row[0] #expected only one row 
        c = conn.cursor()
        c.execute('select DISTINCT (currency) from holdinginfo where username=?',(username,))
        currencyList=c.fetchall()
        conn.row_factory = None
        return currencyList
    
    def getSumByCurrency(username,currency):
        #retrun dict
        conn.row_factory =sqlite3.Row #dictionary cursor
        c = conn.cursor()
        c.execute('SELECT sum(amount) as totalAmount,sum(quantity) as totalQuantity FROM holdinginfo WHERE username=? AND currency=?',(username,currency,))
        sumAmount=c.fetchall()
        conn.row_factory = None
        return sumAmount[0]
    