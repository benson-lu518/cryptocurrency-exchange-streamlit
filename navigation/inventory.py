import streamlit as st
import pandas as pd 
from dao.HoldingDao import HoldingDao
from navigation.dashboard_yf import get_market, get_historical

def page(name):
    st.title('💥 Holding Information')
    tickers =HoldingDao.getAllCurrency(name)
    
    #get total profit
    totalLossOrGain,totalprofit=getTotalProfit(name,tickers)

    #left section
    tickers.insert(0,'ALL')
    # tickers=tuple(tickers)
    # tickers = ('ALL','BTC', 'ETH', 'SOL', 'ADA', 'DOT', 'MATIC', 'EGLD', 'DOGE', 'XRP', 'BNB')
    coin = st.sidebar.selectbox('Pick a coin from the list', tickers)
    start_date = st.sidebar.date_input('Start Date', value = pd.Timestamp.now()-pd.DateOffset(years=1), key = 'dstart_date')
    end_date = st.sidebar.date_input('End Date', value = pd.Timestamp.now()+pd.DateOffset(days=1)  , key = 'dend_date')
    dataset=load_data(name,coin,start_date,end_date)
    #get selected currency price
    currentPrice = get_historical(coin, start_date= None, end_date = None, period = '1m')['Close'].iloc[-1]


    top_menu = st.columns(3)
    # with top_menu[0]:
    #     sort = st.radio("Sort Data", options=["Yes", "No"], horizontal=1, index=1)
    # if sort == "Yes":
    with top_menu[0]:
        if coin!='ALL': #get selected currency price
            st.metric(coin+" Current Price: ",round(currentPrice,4))
        st.text("Total: "+str(len(dataset))+" Transactions")

    with top_menu[1]:
        sort_field = st.selectbox("Sort By", options=dataset.columns)
    with top_menu[2]:
        sort_direction = st.radio(
            "Direction", options=["⬇️","⬆️"], horizontal=True
        )
    dataset = dataset.sort_values(
        by=sort_field, ascending=sort_direction == "⬆️", ignore_index=True
    )

    #start index from 1 not 0
    dataset.index+=1 

    pagination = st.container()

    bottom_menu = st.columns((4, 1, 1))
    with bottom_menu[2]:
        batch_size = st.selectbox("Page Size", options=[25, 50, 100])
    with bottom_menu[1]:
        total_pages = (
            int(len(dataset) / batch_size)+1 if int(len(dataset) / batch_size) > 0 else 1
        )
        current_page = st.number_input(
            "Page", min_value=1, max_value=total_pages, step=1
        )
    with bottom_menu[0]:
        st.markdown(f"Page **{current_page}** of **{total_pages}** ")

        if (len(dataset)>0):
            pages = split_frame(dataset, batch_size+1)
            pagination.dataframe(data=pages[current_page - 1], use_container_width=True)
        else:
            st.write("No Trading Recode !")

    bottom_menu = st.columns(2)
    with bottom_menu[0]:
        st.metric('Total Profit', f'{round(totalLossOrGain,4):,}', f'{round(totalprofit,3)}%')
    with bottom_menu[1]:
        if coin!='ALL':
            #get selected coin profit        
            lossOrGain,profit=getOneProfit(name,coin,currentPrice)
            st.metric(str(coin)+" Profit: ", f'{round(lossOrGain,4):,}', f'{round(profit,3)}%')


def load_data(name,coin,start_date,end_date):
    if coin =='ALL':
        history = HoldingDao.getAllHistoryByUsername(name,start_date,end_date)
        # print(history)
    else:
        history = HoldingDao.getAllHistoryByUsernameCurrency(name,coin,start_date,end_date)
    
    return history


def split_frame(input_df, rows):
    df = [input_df.loc[i : i + rows - 1, :] for i in range(0, len(input_df), rows)]
    return df

def getTotalProfit(username,coin):
    totalLossOrGain=0
    totalShare=0
    for i in coin:
        total=HoldingDao.getSumByCurrency(username,i)
        totalAmount=total['totalAmount']
        totalQuantity=total['totalQuantity']
      
        currentPrice = get_historical(i, start_date= None, end_date = None, period = '1m')['Close'].iloc[-1]
        if totalQuantity>0:
            totalLossOrGain+=(currentPrice*totalQuantity-totalAmount) 
            totalShare=totalShare+totalAmount
            
        else:
            totalLossOrGain+=(currentPrice*totalQuantity-totalAmount)   
            totalShare=totalShare-totalAmount
           

    totalprofit=totalLossOrGain/totalShare*100
    return totalLossOrGain,totalprofit

def getOneProfit(username,coin,currentPrice):
    total=HoldingDao.getSumByCurrency(username,coin)
    totalAmount=total['totalAmount']
    totalQuantity=total['totalQuantity']
    totalLossOrGain=currentPrice*totalQuantity-totalAmount
    
    profit=0
    if totalQuantity>0:
       profit=totalLossOrGain/totalAmount*100    
    else:
        profit=totalLossOrGain/-totalAmount*100  

    return totalLossOrGain,profit
    