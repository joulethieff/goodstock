# Your df that contains "Time" column
import streamlit as st
import pandas as pd
import datetime

#df = pd.DataFrame({"Time":[1, 2, 3, 4]})


st.header('문수보리 택일')

#start_date = st.date_input('Enter start date', value=datetime.datetime(2019,7,6))
#start_time = st.time_input('Enter start time', datetime.time(8, 45))

st.text_input('날짜를 입력하세요', '2023/01/01')
st.text_input('시간을 입력하세요', '23:23')






