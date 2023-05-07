from dao.HoldingDao import HoldingDao
from navigation.dashboard_yf import get_market, get_historical
import yfinance as yf

coin = "BTC" + "-USD"
stock = yf.Ticker(coin)

historical=stock.history().columns
print(historical)
