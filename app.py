# Your df that contains "Time" column
import streamlit as st
import pandas as pd
import datetime

df = pd.DataFrame({"Time":[1, 2, 3, 4]})


st.header('문수보리 택일')

#start_date = st.date_input('Enter start date', value=datetime.datetime(2019,7,6))
#start_time = st.time_input('Enter start time', datetime.time(8, 45))

daate = st.text_input('Movie title', '2023/01/01')
tiime2 = st.text_input('Movie title', '2023/01/01')

"""
start = "00:00"
end = "23:59"
times = []
start = now = datetime.datetime.strptime(start, "%H:%M")
end = datetime.datetime.strptime(end, "%H:%M")

while now != end:
    times.append(str(now.strftime("%H:%M")))
    now += datetime.timedelta(minutes=1)

times.append(end.strftime("%H:%M"))
"""




# start_datetime = datetime.datetime.combine(start_date, start_time)
# df["DateTime"] = [start_datetime + datetime.timedelta(seconds=time) for time in df["Time"]]
# df["DateTime"] = [date.strftime("%d/%m/%Y %H:%M:%S") for date in df["DateTime"]]


#df = df.drop(columns=["Time"])
#st.dataframe(df)