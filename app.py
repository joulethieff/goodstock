import yfinance as yf
import streamlit as st

st.title("""간단한 주식차트 보기(테슬라)""")

Stock_Symbol = 'TSLA'
StockData = yf.Ticker(Stock_Symbol)
StockChart = StockData.history(period = '1d', start='2019-7-1',end='2021-12-25')

st.line_chart(StockChart.Close)
st.line_chart(StockChart.Volume)
