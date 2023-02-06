from datetime import datetime
import datetime
import pandas as pd
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from flatlib.datetime import Datetime               # 날짜 시간
from flatlib.geopos import GeoPos                   # 위치
from flatlib import const                           # 차트에서 포인트값
from flatlib.chart import Chart

from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

import streamlit as st                              # 스트림릿 임포트
import streamlit.components.v1 as components        # 스트림릿 컴포넌트

#import matplotlib.pyplot as plt
import numpy as np

import swisseph as swe

now = datetime.datetime.now()
today = date.today()


#스트림릿 클라우드에서는
swe.set_ephe_path('/home/appuser/venv/lib/python3.9/site-packages/flatlib/resources/swefiles')
# PC에서 라이브러리
#swe.set_ephe_path('c:/venv/helloword/venv/lib/site-packages/flatlib/resources/swefiles')

# 웹 화면을 전체적으로 크게 
st.set_page_config(layout="wide")

# initialize Nominatim API, 지명과 관련된 api
geolocator = Nominatim(user_agent="geoapiExercises")
obj_tzf = TimezoneFinder()


# 화면을 구분
tab1, tab2, tab3, tab4 = st.tabs(["만세력", "심운", "궁합","타로"])


##### 기본 정보 입력 #######
## 탭1 은 만세력정보를 만들어냄

with tab1:

    ### 스트림릿에서 날짜값들을 입력
    col1, col2 = st.columns([1, 8])  # 년 월 일로 나눔

    with col1:
        bdate = st.date_input("날짜00", min_value=datetime.date(1900, 1, 1))

        #btime = st.time_input("생시")
        hours = []
        mins = []
        for h in range(0, 24):
            hours.append(h)
        bhour = st.selectbox("시00", hours)

        for m in range(0, 60):
             mins.append(m)
        bmin = st.selectbox("분00", mins)
        lad = st.text_input('장소00', '서울시')  # 위치명 입력


    # 위치에서 위경도 값을 가져옴
    location = geolocator.geocode(lad)

    ### 위치에서 문자열 타임존 가져오기
    obj_tzf_result = obj_tzf.timezone_at(lng=location.longitude, lat=location.latitude) # 타임존 스트링으로 가져오기


    ### 해당 날짜를 타임존에 맞게 변경함. 로컬라이즈
    seoul = pytz.timezone(obj_tzf_result)
    #dt = seoul.localize(datetime.datetime(bdate.year, bdate.month, bdate.day,btime.hour,btime.minute,btime.second))
    dt = seoul.localize(datetime.datetime(bdate.year, bdate.month, bdate.day,bhour,bmin,0))

    ### 플랫라이브러(점성술 차트 라이브러리)에 맞는 날짜형식으로 바꿈
    date = Datetime(str(dt.year)+'/'+str(dt.month)+'/'+str(dt.day), str(dt.hour)+':'+str(dt.minute)+':'+str(dt.second),dt.utcoffset().total_seconds()/60/60)     # 플랫 라이브러리 형식의 날짜 입력

    pos = GeoPos(location.latitude, location.longitude)   # 위경도 값 입력
    chart = Chart(date, pos, hsys=const.HOUSES_KOCH,IDs=const.LIST_OBJECTS)

    #### 데이타 출력 ##
    with col2:
        #sun = chart.getObject(const.SUN)
        #st.text(sun)

        df = pd.DataFrame()
        df2 = pd.DataFrame()

        # 해당 달의 첫째날 구하기
        first_day = bdate.replace(day=1)  # 첫째날
        last_day = first_day + relativedelta(months=1) - relativedelta(days=1)  # 마지막날
        
        # 해당월의 날짜수 구하기
        j = int(last_day.strftime('%d')) - int(first_day.strftime('%d'))

        # 양력일의 데이타 날짜 구해서 입력
        #df2 = pd.DataFrame([first_day],["dfd"],columns=['양력','d'])
        df2 = pd.DataFrame({'양력' : [first_day],
                            '요일' : [first_day.strftime("%a")]})


        for i in range(1, j + 1):
            iday = first_day + relativedelta(days=i)
            df = pd.DataFrame({'양력' : [iday],
                               '요일' : [iday.strftime("%a")]})
            df2 = pd.concat([df2, df],ignore_index = True)


        st.dataframe(df2)



##### 기본 정보 입력 #######
## 탭2 은 심운정보를 만들어냄

with tab2:
    ### 스트림릿에서 날짜값들을 입력
    col1, col2, col3 = st.columns([1, 1, 8])  # 년 월 일로 나눔

    with col1:
        name = st.text_input('이름', '홍길동')  # 이름을 입력
        gender = st.selectbox('성별', ('남', '여'))  # 이름을 입력
        lad = st.text_input('태어난곳', '서울시')  # 위치명 입력

    with col2:
        bdate = st.date_input("생일", min_value=datetime.date(1900, 1, 1))

        # btime = st.time_input("생시")
        hours = []
        mins = []
        for h in range(0, 24):
            hours.append(h)
        bhour = st.selectbox("시간", hours)

        for m in range(0, 60):
            mins.append(m)
        bmin = st.selectbox("분", mins)

    # 위치에서 위경도 값을 가져옴
    location = geolocator.geocode(lad)

    ### 위치에서 문자열 타임존 가져오기
    obj_tzf_result = obj_tzf.timezone_at(lng=location.longitude, lat=location.latitude)  # 타임존 스트링으로 가져오기

    ### 해당 날짜를 타임존에 맞게 변경함. 로컬라이즈
    seoul = pytz.timezone(obj_tzf_result)
    # dt = seoul.localize(datetime.datetime(bdate.year, bdate.month, bdate.day,btime.hour,btime.minute,btime.second))
    dt = seoul.localize(datetime.datetime(bdate.year, bdate.month, bdate.day, bhour, bmin, 0))

    ### 플랫라이브러(점성술 차트 라이브러리)에 맞는 날짜형식으로 바꿈
    date = Datetime(str(dt.year) + '/' + str(dt.month) + '/' + str(dt.day),
                    str(dt.hour) + ':' + str(dt.minute) + ':' + str(dt.second),
                    dt.utcoffset().total_seconds() / 60 / 60)  # 플랫 라이브러리 형식의 날짜 입력

    pos = GeoPos(location.latitude, location.longitude)  # 위경도 값 입력
    chart = Chart(date, pos, hsys=const.HOUSES_KOCH, IDs=const.LIST_OBJECTS)

    #### 데이타 출력 ##
    with col3:
        # sun = chart.getObject(const.SUN)
        # st.text(sun)

        df = pd.DataFrame()
        df2 = pd.DataFrame()

        # 해당 달의 첫째날 구하기
        first_day = bdate.replace(day=1)  # 첫째날
        last_day = first_day + relativedelta(months=1) - relativedelta(days=1)  # 마지막날

        # 해당월의 날짜수 구하기
        j = int(last_day.strftime('%d')) - int(first_day.strftime('%d'))

        # 양력일의 데이타 날짜 구해서 입력
        df2 = pd.DataFrame([first_day], columns=['양력'])
        for i in range(1, j + 1):
            df = pd.DataFrame([first_day + relativedelta(days=i)], columns=['양력'])
            df2 = pd.concat([df2, df], ignore_index=True)

        st.dataframe(df2['양력'])

        # print(df2)
        # st.text(name)
        # st.text(gender)
        # for obj in chart.objects:
        # st.text(obj)

        # components.iframe("https://ilyai.github.io/quick-astro-charts/",width=400,height=400)
        # components.iframe("./astrochart/project/examples/radix/radix.html", width=400, height=400)

        # HtmlFile = open('./astrochart/project/examples/radix/radix.html', 'r')
        # raw_html = HtmlFile.read().encode("utf-8")
        # raw_html = base64.b64encode(raw_html).decode()
        # components.iframe("https://www.google.com/calendar/b/0/embed?showTitle=0&showPrint=0&showTabs=0&showCalendars=0&height=600&wkst=1&bgcolor=%23cccccc&src=xxxxxxxxx.com_613ubxxxxxxxxxxxxxxk%40group.calendar.google.com&color=%2328754E&ctz=Asia%2FSeoul", width=800, height=600)

