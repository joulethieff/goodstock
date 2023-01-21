import streamlit as st                              # 스트림릿 임포트
from flatlib.datetime import Datetime
import pandas as pd
from flatlib.datetime import Datetime               # 날짜 시간
from flatlib.geopos import GeoPos                   # 위치
from flatlib import const                           # 차트에서 포인트값
from flatlib.chart import Chart

from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
import datetime
import streamlit as st                              # 스트림릿 임포트

import swisseph as swe
swe.set_ephe_path('/home/appuser/venv/lib/python3.9/site-packages/flatlib/resources/swefiles')

# initialize Nominatim API, 지명과 관련된 api
geolocator = Nominatim(user_agent="geoapiExercises")
obj_tzf = TimezoneFinder()

### 스트림릿에서 날짜값들을 입력
col1,col2 = st.columns([2,10])                                               # 년 월 일로 나눔


##### 기본 정보 입력 ##
name = st.text_input('이름', '홍길동')  # 이름을 입력
byear = st.number_input('생년', min_value=0, max_value=3000, value=1980, step=1)  # 생년을 입력
bmonth = st.number_input('생월', min_value=1, max_value=12, value=1, step=1)  # 생월을 입력
bday = st.number_input('생일', min_value=1, max_value=31, value=1, step=1)  # 생월을 입력
bhour = st.number_input('시', min_value=0, max_value=23, value=0, step=1)  # 시를 입력
bmin = st.number_input('분', min_value=0, max_value=60, value=0, step=1)  # 분을 입력
bsec = st.number_input('초', min_value=0, max_value=60, value=0, step=1)  # 초를 입력
lad = st.text_input('태어난곳', '서울시')  # 위치명 입력
location = geolocator.geocode(lad)                                      # 위치에서 위경도 값을 가져옴
### 위치에서 문자열 타임존 가져오기
obj_tzf_result = obj_tzf.timezone_at(lng=location.longitude, lat=location.latitude) # 타임존 스트링으로 가져오기


### 해당 날짜를 타임존에 맞게 변경함. 로컬라이즈
seoul = pytz.timezone(obj_tzf_result)
dt = seoul.localize(datetime.datetime(byear, bmonth, bday,bhour,bmin,bsec))

### 플랫라이브러(점성술 차트 라이브러리)에 맞는 날짜형식으로 바꿈
date = Datetime(str(dt.year)+'/'+str(dt.month)+'/'+str(dt.day), str(dt.hour)+':'+str(dt.minute)+':'+str(dt.second),dt.utcoffset().total_seconds()/60/60)     # 플랫 라이브러리 형식의 날짜 입력

pos = GeoPos(location.latitude, location.longitude)   # 위경도 값 입력
chart = Chart(date, pos, hsys=const.HOUSES_KOCH,IDs=const.LIST_OBJECTS)

sun = chart.getObject(const.SUN)
st.text(sun)
