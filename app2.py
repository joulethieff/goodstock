from datetime import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

now = datetime.now()
today = date.today()

# 현재시간 출력
print("현재 :" , now)	# 현재 : 2021-01-09 20:07:09.682594

#해당 달의 첫째날 구하기
first_day = today.replace(day=1)
last_day = first_day + relativedelta(months=1) - relativedelta(days=1)

print("금월 1일 : ", first_day)
print("금월 말일 : ", last_day)



