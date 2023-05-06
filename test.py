from dao.HoldingDao import HoldingDao
from navigation.dashboard_yf import get_market, get_historical

test=HoldingDao.getSumByCurrency('Ted','BTC')
totalAmount=test['totalAmount']
totalQuantity=test['totalQuantity']
price = get_historical('BTC', start_date= None, end_date = None, period = '1m')['Close'].iloc[-1]


profit=(price*totalQuantity-totalAmount)/totalAmount*100
print(profit)