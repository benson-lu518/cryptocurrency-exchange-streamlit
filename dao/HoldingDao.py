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
        #oldest transaction will show first
        #return dict
        conn.row_factory =sqlite3.Row #dictionary cursor
        c = conn.cursor()
        c.execute('SELECT * FROM holdinginfo WHERE username =? AND currency=? ORDER BY createddate ASC',(username,currency,))
        userInfo=c.fetchall()
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
        return totalQuantity

    def insertNewRow(username,box01,convert,quantity,price1,createddate,lastupdateddate):
        c.execute('INSERT INTO holdinginfo (username,currency,amount,quantity,boughtprice,createddate,lastupdateddate) VALUES (?,?,?,?,?,?,?)',(username,box01,convert,quantity,price1,createddate,lastupdateddate))
        conn.commit()

    def deleteRowByholding_id(holding_id):
        c.execute('DELETE FROM holdinginfo WHERE holding_id=?',(holding_id,))
        conn.commit()

    def updateQuantity(quantity,lastupdateddate,holding_id):
        c.execute('UPDATE holdinginfo SET quantity=?, lastupdateddate=? WHERE holding_id=?',(quantity,lastupdateddate ,holding_id))
        conn.commit()
