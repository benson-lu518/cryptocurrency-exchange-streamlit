import streamlit as st
from navigation.dashboard_yf import get_market, get_historical
from datetime import datetime,timezone,timedelta
from dao.UserDao import UserDao
from dao.TradingDao import TradingDao
from dao.HoldingDao import HoldingDao 


def getCurrentTime():
    #get current time 
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # to TW timezone 
    st2 = dt2.strftime('%Y-%m-%d %H:%M:%S') #to str
    dt2 = datetime.strptime(st2,'%Y-%m-%d %H:%M:%S') #to timestamp change format
    return dt2



# Crypto/USD Calculator
def page(username):
    # Crypto/USD Calculator
    st.title('💥 Cryptocurrency Trading System')
    col1, col2 = st.columns(2)

    tickers2 = ('BTC', 'ETH', 'SOL', 'ADA', 'DOT', 'MATIC', 'EGLD', 'DOGE', 'XRP', 'BNB')
    with col1: box01 = st.selectbox('From',tickers2, key = 'coin1') 
    with col2: box02 = st.text_input('To','USD',disabled =True) #default USD
    
    columns = st.columns((2, 1, 2))
    quantity = columns[0].number_input('Quantity')

    if box01 != 'USD' and box02 != 'USD':
        price1 = get_historical(box01, start_date= None, end_date = None, period = '1d')['Close'].iloc[-1]
        price2 = get_historical(box02, start_date= None, end_date = None, period = '1d')['Close'].iloc[-1]
        convert = float(quantity*price1/price2)
    elif box01 == 'USD' and box02 != 'USD':
        price2 = get_historical(box02, start_date= None, end_date = None, period = '1d')['Close'].iloc[-1]
        convert = float(quantity/price2)
    #box02 defaults to USD, box01 is the currency u trade
    elif box01 != 'USD' and box02 == 'USD':
        price1 = get_historical(box01, start_date= None, end_date = None, period = '1d')['Close'].iloc[-1]
        convert = float(quantity*price1)
    else:
        convert = quantity

    columns = st.columns((1, 1))
    columns[0].metric('',convert)  #show convert
    #convert=amount

    if st.button('Order'):
       if quantity==0:
           st.warning("Quantity can't be 0")
       else:
        addRecord(username,box01,convert,quantity,price1)
        updateHodingInfo(username,box01,convert,quantity,price1)

def addRecord(username,box01,convert,quantity,price1):
    #get current time
    dt2= getCurrentTime()

    #get current available cash
    cash=UserDao.getCashByUsername(username)
    
    #update cash
    remainCash=float(cash)-convert
    UserDao.updateCashByUsername(username,remainCash)
    
    #insert into tradingInfo
    TradingDao.insetTradingInfo(username,box01,convert,quantity,price1,dt2)

    st.success("Username: {} placed an order successfully ".format(username))

def updateHodingInfo(username,box01,convert,quantity,price1):
    dt2=getCurrentTime() 
    holdingInfo=HoldingDao.getHoldingInfo(username,box01)
    totalQuantity=HoldingDao.getTotalQuantity(username,box01)
            
    if len(holdingInfo)==0:#new currency 
        HoldingDao.insertNewRow(username,box01,convert,quantity,price1,dt2,dt2)
    else: 
        if quantity>0: #if buy 
            if totalQuantity>0: #also have + quantity holding
                HoldingDao.insertNewRow(username,box01,convert,quantity,price1,dt2,dt2)
            else: #have - quantity holding  
                eachQuantityRow=HoldingDao.getHoldingInfoDict(username,box01)
                remainingQuantity=0
                for i in eachQuantityRow:
                    if i['quantity']+ quantity==0: #need to be written off 
                        HoldingDao.deleteRowByholding_id(i['holding_id'])
                        break
                    elif i['quantity'] +quantity<0: #enough to buy then update
                        remainingQuantity=i['quantity']+quantity
                        HoldingDao.updateQuantity(remainingQuantity,dt2,i['holding_id'])
                        break
                    else: #last row holding quantity< sell quantity then delete current row and update last row 
                        quantity=i['quantity']+quantity
                        HoldingDao.deleteRowByholding_id(i['holding_id'])
                        print(remainingQuantity)
                        
        elif quantity<0: #if sell
            if totalQuantity<0: #also have - quantity holding
                HoldingDao.insertNewRow(username,box01,convert,quantity,price1,dt2,dt2)
            else: #have + quantity holding  
                eachQuantityRow=HoldingDao.getHoldingInfoDict(username,box01)
                remainingQuantity=0
                for i in eachQuantityRow:
                    if i['quantity']+quantity == 0: #need to be written off 
                        HoldingDao.deleteRowByholding_id(i['holding_id'])
                        break
                    elif i['quantity']+quantity>0: # enough to sell and update 
                        remainingQuantity=i['quantity']+quantity
                        # print(remainingQuantity) 
                        HoldingDao.updateQuantity(remainingQuantity,dt2,i['holding_id'])
                        break
                    else: #last row holding quantity< sell quantity then delete current row and update last row 
                        quantity=i['quantity']+quantity
                        HoldingDao.deleteRowByholding_id(i['holding_id'])
                        print(remainingQuantity)
                        

                