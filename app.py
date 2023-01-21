import streamlit as st                              # 스트림릿 임포트
from flatlib.datetime import Datetime

date = Datetime('2015/03/13', '17:00', '+00:00')

st.text(date)