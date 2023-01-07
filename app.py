import yfinance as yf
import streamlit as st
import datetime

st.title("""간단한 주식차트 보기(테슬라)""")

Stock_Symbol = 'TSLA'
StockData = yf.Ticker(Stock_Symbol)
StockChart = StockData.history(period = '1d', start='2019-7-1',end='2021-12-25')

st.line_chart(StockChart.Close)
st.line_chart(StockChart.Volume)

## Date Input

today = st.date_input("날짜를 선택하세요.", datetime.datetime.now())
the_time = st.time_input("시간을 입력하세요.", datetime.time())