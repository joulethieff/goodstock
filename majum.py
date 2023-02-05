import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
import tkinter as Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


###### 기본 GUI를 만듬 ####

root = Tk.Tk() #추가

## 최초 윈도우의 크기
window_width = 1600            # 창의 좌우 크기
window_height = 900           # 창의 높이 크기
window_pos_x = 160            # 창의 x방향 위치
window_pos_y = 30            # 창의 y방향 위치

# 창의 타이틀
root.title("마점")

# tk의 크기, 가로크기 세로크기 화면x좌표 화면 y좌표
root.geometry("{}x{}+{}+{}".format(window_width,window_height,window_pos_x,window_pos_y))
# 창의 크기조절은 안됨
root.resizable(False,False)
#창의 아이콘을 설정함
#root.iconphoto(False,tkinter.PhotoImage(file="test.png"))

# 프레임 위젯 생성
frame1 = Tk.LabelFrame(width = 600, height = 600, relief="solid",bd=1,bg="white",text="360 심운차트")
frame2 = Tk.LabelFrame(width = 200, height = 80, relief="solid",bd=1,bg="white",text="해석")

# 프레임 위젯 배치
frame1.place(x=00,y=0)
frame2.place(x=600,y=0)


# 입력정보 라벨 프레임 생성 배치
lf=Tk.LabelFrame(root,text='기본정보',bg='white')
lf.place(x=1280,y=0,width=300,height=100)

l1=Tk.Label(lf,text='이름')
l1.place(x=10,y=5,)

e1=Tk.Entry(lf,width=30)
e1.place(x=50,y=5)



# 사용할 폰트를 지정한다.
# 한글 표현이 안되어서 한글폰트를 지정한다.
matplotlib.font_manager._load_fontmanager(try_read_cache=False)
fm.get_fontconfig_fonts()
#font_location = 'C:/Windows/Fonts/NanumGothic.ttf'
#font_location = 'C:/Windows/Fonts/gulim.ttc' #굴림체로 한다.
font_location = 'C:/Windows/Fonts/wt004.ttf' #
#font_location = 'C:/Windows/Fonts/wt004.ttf' #굴림체로 한다.
font_name = fm.FontProperties(fname=font_location).get_name()
matplotlib.rc('font', family=font_name,size=16)

fpath00 = 'C:/Windows/Fonts/wt004.ttf'
fontprop = fm.FontProperties(fname=fpath00, size=14)


## 지반 데이터 준비
#labels = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']  ## 라벨
jiban_labels = ['午', '未', '申', '酉','戌','亥','子','丑','寅','卯','辰','巳'] # 지반의 표시
jiban_ratio = [30,30,30,30,30,30,30,30,30,30,30,30]  ## 360도에서 차지하는 비율
jiban_explode = (0,0,0,0,0,0,0,0,0,0,0,0)          # 파이에서 튀어나오게 하는 부분
jiban_color = ['white','white','white','white','white','white','white','white','white','white','white','white']

## 천반 데이터 준비
#labels = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']  ## 라벨
cheonban_labels = ['午', '未', '申', '酉','戌','亥','子','丑','寅','卯','辰','巳'] # 지반의 표시
cheonban_ratio = [30,30,30,30,30,30,30,30,30,30,30,30]  ## 360도에서 차지하는 비율
cheonban_explode = (0,0,0,0,0,0,0,0,0,0,0,0)          # 파이에서 튀어나오게 하는 부분
cheonban_color = ['white','white','white','white','white','white','white','white','white','white','white','white']



#################
fig = plt.figure(figsize=(5, 5))  ## 캔버스 생성
fig.set_facecolor('#FFFF80')  ## 캔버스 배경색

ax = fig.add_subplot()       ## 프레임 생성

jiban_pie = ax.pie(jiban_ratio,  ## 파이차트 출력
             startangle=0,  ## 시작점을 90도(degree)로 지정
             explode=jiban_explode,
             counterclock=True,  ## 시계 방향으로 그린다.
             #autopct=lambda p: '{:.2f}%'.format(p),  ## 퍼센티지 출력
             radius= 1.0,
             labels=jiban_labels,
             wedgeprops={ 'linewidth' : 1 , 'edgecolor' : 'black','width' : 0.2}, # 파이차트의 선 두께 색상을 정함
             #wedgeprops=dict(width=0.2)  ## 중간의 반지름 0.5만큼 구멍을 뚫어준다.
             colors = jiban_color,
             textprops={'fontsize': 16, 'ha':'center','va':'center'},
             labeldistance=1.15,
             )


#for t in jiban_pie:
#    t.set_horizontalalignment('center')

cheonban_pie = ax.pie(cheonban_ratio,  ## 파이차트 출력
             startangle=0,  ## 시작점을 90도(degree)로 지정
             explode=cheonban_explode,
             counterclock=True,  ## 시계 방향으로 그린다.
             #autopct=lambda p: '{:.2f}%'.format(p),  ## 퍼센티지 출력
             radius= 0.8,
             labels=cheonban_labels,
             wedgeprops={ 'linewidth' : 1 , 'edgecolor' : 'black','width' : 0.2}, # 파이차트의 선 두께 색상을 정함
             colors = cheonban_color,
             #labeldistance=0.85,
             textprops={'fontsize': 10, 'ha':'center','va':'center'},
             #textprops={'fontsize': 10,'horizontalalignment' : 'center', 'verticalalignment' :'top'},
             labeldistance=0.86 # 바깥쪽으로 치우친 라벨을 안쪽으로
             )




# 가운데에 원형 CIRCLE을 만들어준다.
centre_circle = plt.Circle((0,0), 0.25, fc='white')
fig= plt.gcf()
fig.gca().add_artist(centre_circle) # adding the centre circle


###### matlib의 파이차트를 tkinter에 추가함 ####

#canvas = FigureCanvasTkAgg(fig, master=root) #
canvas = FigureCanvasTkAgg(fig, master=frame1) # 파이차트를 프레임에 배치
canvas.get_tk_widget().grid(column=0,row=1) #


# 일반적으로 matplot을 그리는데 필요하지만
# tkinter에 그리는데는 필요하지 않음.
#plt.show()


Tk.mainloop()