from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode, AgGridTheme
from korean_lunar_calendar import KoreanLunarCalendar # 음양력변환 라이브러리
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

CheonGan = ('庚','辛','壬','癸','甲','乙','丙','丁','戊','己') # 년도를 10으로 나눈 나머값
GeeGee = ('申','酉','戌','亥','子','丑','寅','卯','辰','巳','午','未') # 년도를 12로 나눈 나머지값

now = datetime.datetime.now()
today = date.today()


#스트림릿 클라우드에서는
swe.set_ephe_path('/home/appuser/venv/lib/python3.9/site-packages/flatlib/resources/swefiles')
# PC에서 라이브러리
#swe.set_ephe_path('c:/venv/helloword/venv/lib/site-packages/flatlib/resources/swefiles')

# 웹 화면을 전체적으로 크게 
st.set_page_config(layout="wide")
st.title("마음의 점성학 - 남두성 만세력")

# initialize Nominatim API, 지명과 관련된 api
geolocator = Nominatim(user_agent="geoapiExercises")
obj_tzf = TimezoneFinder()
# 음양력 변환객체생성
calendar_um = KoreanLunarCalendar()

# 화면을 구분
tab1, tab2, tab3, tab4 = st.tabs(["만세력", "심운", "궁합","타로"])



## 탭1 은 만세력정보를 만들어냄
######################################################################################################################

with tab1:   # 만세력 탭

    #st.header("만세력")

    ### 스트림릿에서 날짜값들을 입력
    col1, col2 = st.columns([1, 8])  # 년 월 일로 나눔

    ### tab1 ###
    with col1:

        byear = st.number_input("년",value=2023,min_value=1896,max_value=2050)
        bmonth = st.number_input("월",value=1,min_value=1,max_value=12)
        bday = '1'

        #bdate = st.date_input("양력날짜00", min_value=datetime.date(1900, 1, 1))
        #bdate = datetime.strptime(date_str, '%m-%d-%Y')

        #bdate = datetime(byear+'/'+bmonth+'/'+bday,'%Y/%m/%d')
        bdate = datetime.datetime.strptime(str(byear)+'/'+str(bmonth)+'/'+bday, '%Y/%m/%d')

        bhour = 0 # 초기 시간은 0
        bmin = 0 # 초기 분도 0

        #lad = st.text_input('장소00', '서울시',disabled=1)  # 위치명 입력


        # 위치에서 위경도 값을 가져옴
        location = geolocator.geocode('서울시')


        ### 위치에서 문자열 타임존 가져오기
        obj_tzf_result = obj_tzf.timezone_at(lng=location.longitude, lat=location.latitude) # 타임존 스트링으로 가져오기
        st.text_input('타임존',obj_tzf_result,disabled=1)


        ### 해당 날짜를 타임존에 맞게 변경함. 로컬라이즈
        seoul = pytz.timezone(obj_tzf_result)
        #dt = seoul.localize(datetime.datetime(bdate.year, bdate.month, bdate.day,btime.hour,btime.minute,btime.second))
        dt = seoul.localize(datetime.datetime(bdate.year, bdate.month, bdate.day,bhour,bmin,0))
        #st.text_input('오프셋',dt.utcoffset().total_seconds() / 60 / 60,disabled=1)
        #st.text(dt)


    ### tab1
    #### 데이타 출력  ##
    with col2:
        #sun = chart.getObject(const.SUN)
        #st.text(sun)

        of = ['월', '화', '수', '목', '금', '토', '일']
        YangYearGanGee = []
        YangMonthGangee = []
        ilGangee = []

        df = pd.DataFrame()  # 한달치를 통합해서 저장할 데이타프레임
        df2 = pd.DataFrame() # 1일의 정보를 입력하기 위한 데이타프레임

        # 해당 달의 첫째날 구하기
        first_day = bdate.replace(day=1)  # 첫째날
        last_day = first_day + relativedelta(months=1) - relativedelta(days=1)  # 마지막날


        # 해당월의 날짜수 구하기
        j = int(last_day.strftime('%d')) - int(first_day.strftime('%d')) +1
        #st.text(j)


        # 둘째날부터 마지막 날까지를 계속 데이타프레임에 추가
        iday = first_day
        for i in range(1, j+1):
            calendar_um.setSolarDate(iday.year,iday.month,iday.day)
            
            # 태양의 위치를 구하기 위해 반복
            ### 플랫라이브러(점성술 차트 라이브러리)에 맞는 날짜형식으로 바꿈
            date = Datetime(str(dt.year) + '/' + str(dt.month) + '/' + str(iday.day+1),
                            str(dt.hour) + ':' + str(dt.minute) + ':' + str(dt.second),
                            dt.utcoffset().total_seconds() / 60 / 60)  # 플랫 라이브러리 형식의 날짜 입력
            pos = GeoPos(location.latitude, location.longitude)  # 위경도 값 입력
            chart = Chart(date, pos, hsys=const.HOUSES_KOCH, IDs=const.LIST_OBJECTS)
            SUN00 = chart.getObject(const.SUN) 
            MOON00 = chart.getObject(const.MOON)

            # 해당년의 입춘간지 연도에 해당하는 간지를 구한다.
            # 해당일의 자정이 황경 270도 315도 사이에 있으면 천간 지지값을 -1 한다.
            if (270 <= SUN00.lon < 315) and dt.month in (1,2) :
                YangYearGanGee = CheonGan[(first_day.year - 1) % 10] + GeeGee[(first_day.year - 1) % 12] + '年'
            else:
                YangYearGanGee = CheonGan[first_day.year % 10] + GeeGee[first_day.year % 12] + '年'

            # 해당일의 월간지를 구한다.
            # 월건의 배치방법은  구하고자 하는 날의 다음날 0시의 황경을 구하고
            # 그 황경값의 소수점을 버리고 그 정수값이 아래와 표기한다.
            if 315 <= SUN00.lon < 345 :
                if YangYearGanGee[0] in ('甲','己') :
                    YangMonthGangee = '丙寅' + '月'
                elif YangYearGanGee[0] in ('乙','庚') :
                    YangMonthGangee = '戊寅' + '月'
                elif YangYearGanGee[0] in ('丙','辛') :
                    YangMonthGangee = '庚寅' + '月'
                elif YangYearGanGee[0] in ('丁','壬') :
                    YangMonthGangee = '壬寅' + '月'
                elif YangYearGanGee[0] in ('戊','癸') :
                    YangMonthGangee = '甲寅' + '月'
            elif 345 <= SUN00.lon or 0 <= SUN00.lon <15 :
                if YangYearGanGee[0] in ('甲', '己'):
                    YangMonthGangee = '丁卯' + '月'
                elif YangYearGanGee[0] in ('乙', '庚'):
                    YangMonthGangee = '己卯' + '月'
                elif YangYearGanGee[0] in ('丙', '辛'):
                    YangMonthGangee = '辛卯' + '月'
                elif YangYearGanGee[0] in ('丁', '壬'):
                    YangMonthGangee = '癸卯' + '月'
                elif YangYearGanGee[0] in ('戊', '癸'):
                    YangMonthGangee = '乙卯' + '月'
            elif 15 <= SUN00.lon < 45 :
                if YangYearGanGee[0] in ('甲', '己'):
                    YangMonthGangee = '戊辰' + '月'
                elif YangYearGanGee[0] in ('乙', '庚'):
                    YangMonthGangee = '庚辰' + '月'
                elif YangYearGanGee[0] in ('丙', '辛'):
                    YangMonthGangee = '壬辰' + '月'
                elif YangYearGanGee[0] in ('丁', '壬'):
                    YangMonthGangee = '甲辰' + '月'
                elif YangYearGanGee[0] in ('戊', '癸'):
                    YangMonthGangee = '丙辰' + '月'
            elif 45 <= SUN00.lon < 75 :
                if YangYearGanGee[0] in ('甲', '己'):
                    YangMonthGangee = '己巳' + '月'
                elif YangYearGanGee[0] in ('乙', '庚'):
                    YangMonthGangee = '辛巳' + '月'
                elif YangYearGanGee[0] in ('丙', '辛'):
                    YangMonthGangee = '癸巳' + '月'
                elif YangYearGanGee[0] in ('丁', '壬'):
                    YangMonthGangee = '乙巳' + '月'
                elif YangYearGanGee[0] in ('戊', '癸'):
                    YangMonthGangee = '丁巳' + '月'
            elif 75 <= SUN00.lon < 105 :
                if YangYearGanGee[0] in ('甲', '己'):
                    YangMonthGangee = '庚午' + '月'
                elif YangYearGanGee[0] in ('乙', '庚'):
                    YangMonthGangee = '壬午' + '月'
                elif YangYearGanGee[0] in ('丙', '辛'):
                    YangMonthGangee = '甲午' + '月'
                elif YangYearGanGee[0] in ('丁', '壬'):
                    YangMonthGangee = '丙午' + '月'
                elif YangYearGanGee[0] in ('戊', '癸'):
                    YangMonthGangee = '戊午' + '月'
            elif 105 <= SUN00.lon < 135 :
                if YangYearGanGee[0] in ('甲', '己'):
                    YangMonthGangee = '辛未' + '月'
                elif YangYearGanGee[0] in ('乙', '庚'):
                    YangMonthGangee = '癸未' + '月'
                elif YangYearGanGee[0] in ('丙', '辛'):
                    YangMonthGangee = '乙未' + '月'
                elif YangYearGanGee[0] in ('丁', '壬'):
                    YangMonthGangee = '丁未' + '月'
                elif YangYearGanGee[0] in ('戊', '癸'):
                    YangMonthGangee = '己未' + '月'
            elif 135 <= SUN00.lon < 165 :
                if YangYearGanGee[0] in ('甲', '己'):
                    YangMonthGangee = '壬申' + '月'
                elif YangYearGanGee[0] in ('乙', '庚'):
                    YangMonthGangee = '甲申' + '月'
                elif YangYearGanGee[0] in ('丙', '辛'):
                    YangMonthGangee = '丙申' + '月'
                elif YangYearGanGee[0] in ('丁', '壬'):
                    YangMonthGangee = '戊申' + '月'
                elif YangYearGanGee[0] in ('戊', '癸'):
                    YangMonthGangee = '庚申' + '月'
            elif 165 <= SUN00.lon < 195 :
                if YangYearGanGee[0] in ('甲', '己'):
                    YangMonthGangee = '癸酉' + '月'
                elif YangYearGanGee[0] in ('乙', '庚'):
                    YangMonthGangee = '乙酉' + '月'
                elif YangYearGanGee[0] in ('丙', '辛'):
                    YangMonthGangee = '丁酉' + '月'
                elif YangYearGanGee[0] in ('丁', '壬'):
                    YangMonthGangee = '己酉' + '月'
                elif YangYearGanGee[0] in ('戊', '癸'):
                    YangMonthGangee = '辛酉' + '月'
            elif 195 <= SUN00.lon < 225 :
                if YangYearGanGee[0] in ('甲', '己'):
                    YangMonthGangee = '甲戌' + '月'
                elif YangYearGanGee[0] in ('乙', '庚'):
                    YangMonthGangee = '丙戌' + '月'
                elif YangYearGanGee[0] in ('丙', '辛'):
                    YangMonthGangee = '戊戌' + '月'
                elif YangYearGanGee[0] in ('丁', '壬'):
                    YangMonthGangee = '庚戌' + '月'
                elif YangYearGanGee[0] in ('戊', '癸'):
                    YangMonthGangee = '壬戌' + '月'
            elif 225 <= SUN00.lon < 255 :
                if YangYearGanGee[0] in ('甲', '己'):
                    YangMonthGangee = '乙亥' + '月'
                elif YangYearGanGee[0] in ('乙', '庚'):
                    YangMonthGangee = '丁亥' + '月'
                elif YangYearGanGee[0] in ('丙', '辛'):
                    YangMonthGangee = '己亥' + '月'
                elif YangYearGanGee[0] in ('丁', '壬'):
                    YangMonthGangee = '辛亥' + '月'
                elif YangYearGanGee[0] in ('戊', '癸'):
                    YangMonthGangee = '癸亥' + '月'
            elif 255 <= SUN00.lon < 285 :
                if YangYearGanGee[0] in ('甲', '己'):
                    YangMonthGangee = '丙子' + '月'
                elif YangYearGanGee[0] in ('乙', '庚'):
                    YangMonthGangee = '戊子' + '月'
                elif YangYearGanGee[0] in ('丙', '辛'):
                    YangMonthGangee = '庚子' + '月'
                elif YangYearGanGee[0] in ('丁', '壬'):
                    YangMonthGangee = '壬子' + '月'
                elif YangYearGanGee[0] in ('戊', '癸'):
                    YangMonthGangee = '甲子' + '月'
            elif 285 <= SUN00.lon < 315 :
                if YangYearGanGee[0] in ('甲', '己'):
                    YangMonthGangee = '丁丑' + '月'
                elif YangYearGanGee[0] in ('乙', '庚'):
                    YangMonthGangee = '己丑' + '月'
                elif YangYearGanGee[0] in ('丙', '辛'):
                    YangMonthGangee = '辛丑' + '月'
                elif YangYearGanGee[0] in ('丁', '壬'):
                    YangMonthGangee = '癸丑' + '月'
                elif YangYearGanGee[0] in ('戊', '癸'):
                    YangMonthGangee = '乙丑' + '月'

            ilGangee00 = calendar_um.getChineseGapJaString()[8:11] # 음력갑자에서 일간지만 추출


            df = pd.DataFrame({'요일' : [of[iday.weekday()]],
                               '양력' : [iday.strftime('%Y-%m-%d')],
                               '음력' : [calendar_um.LunarIsoFormat()],
                               '입춘간지(명리학)': [YangYearGanGee + ' ' + YangMonthGangee + ' ' + ilGangee00],
                               '음력간지(천문연구원)': [calendar_um.getChineseGapJaString()]
                               })
            df2 = pd.concat([df2, df],ignore_index = True) #
            iday = first_day + relativedelta(days=i)  #

        #st.text(YangYearGanGee[0])
        #AgGrid(data=df2, columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,enable_enterprise_modules=False)
        AgGrid(data=df2, columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,enable_enterprise_modules=False)



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


    # tab2
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

