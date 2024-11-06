# google sheet pandas로 읽어오는 방법

import pandas as pd

# https://docs.google.com/spreadsheets/d/1McH-oBzPZ8ewfyEl605wq-9b3gZHCIIBVbWHEHwNnIs/edit?gid=941998772#gid=941998772
gsheet_url = "https://docs.google.com/spreadsheets/d/1McH-oBzPZ8ewfyEl605wq-9b3gZHCIIBVbWHEHwNnIs/gviz/tq?tqx=out:csv&sheet=ames-spot"

df = pd.read_csv(gsheet_url)
df


import pandas as pd

# https://docs.google.com/spreadsheets/d/1McH-oBzPZ8ewfyEl605wq-9b3gZHCIIBVbWHEHwNnIs/edit?gid=941998772#gid=941998772
gsheet_url = "https://docs.google.com/spreadsheets/d/1McH-oBzPZ8ewfyEl605wq-9b3gZHCIIBVbWHEHwNnIs/gviz/tq?tqx=out:csv&sheet=codebook"

codebook = pd.read_csv(gsheet_url)
codebook
codebook.info()


# !pip install pyyaml
# !conda install jupyter
# ---------------------------------------------------------
import json
geo = json.load(open('bigdata/ia_iowa_zip_codes_geo.min.json', encoding = 'UTF-8'))

geo.keys()
len(geo["features"]) # 935
geo["features"][0].keys()
geo["features"][0]["properties"]['ZCTA5CE10']
geo["features"][1]["properties"]

# 위도, 경도 좌표 출력
coordinate_list = geo["features"][1]["geometry"]["coordinates"][0]
len(coordinate_list) # 1558

import numpy as np
coordinate_array = np.array(coordinate_list)
coordinate_array

# 경도 추출
x = coordinate_array[:, 0]
# 위도 추출
y = coordinate_array[:, 1]

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 8))
plt.plot(x, y, color='blue', linewidth=1)

plt.title('Boundary of ZIP Code Area in Iowa')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)

# 그래프 출력
plt.show()
plt.clf()
# ---------------------------------------------------------
import pandas as pd
import numpy as np

import json
geo = json.load(open('bigdata/ia_iowa_zip_codes_geo.min.json', encoding = 'UTF-8'))

def make_ames(num) : 
    postal_code = geo["features"][num]["properties"]['ZCTA5CE10']
    coordinate_list = geo["features"][num]["geometry"]["coordinates"][0]
    coordinate_array = np.array(coordinate_list)
    x = coordinate_array[:, 0].flatten()
    y = coordinate_array[:, 1].flatten()

    return pd.DataFrame({"postal_code" : postal_code, "x":x, "y":y})

# num의 범위 : 935
# make_ames(0)
# make_ames(934)

result = pd.DataFrame({
    'postal_code' : [],
    'x' : [],
    'y' : []
})


for i in range(len(geo["features"])) : 
    result = pd.concat([result, make_ames(i)], ignore_index=True)

result

import seaborn as sns
sns.scatterplot(data = result, 
                x='x', y='y', 
                hue="postal_code", s=1,
                legend=False)
plt.xlim((-97, -89.5))
plt.ylim((40, 44))
plt.show()
plt.clf()
# ---------------------------------------------------------

# ames랑 waukee 그림 그리기
# ames의 postal codes
# waukee_postal_codes
ames_postal_codes = ['50010', '50011', '50012', '50013', '50014']
waukee_postal_code = ['50003', '50263', '50325']
result['location'] = np.where(result['postal_code'].isin(ames_postal_codes), 'Ames',(
                     np.where(result['postal_code'].isin(waukee_postal_code), 'Waukee','Iowa')
                      ))
result

result[result['location'] == "Ames"]
result[result['location'] == "Waukee"]

import seaborn as sns
sns.scatterplot(data = result, 
                x='x', y='y', 
                hue="location", s=1,
                palette={"Ames":"red", "Iowa":"grey", "Waukee":"blue"}
                )
plt.xlim((-97, -89.5))
plt.ylim((40.2, 43.8))
plt.show()
plt.clf()
plt.close()

# ---------------------------------------------------------


# 시계열 나도 해보자.
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

house_train = pd.read_csv("./data/train.csv")
house_train.info()

house_train = house_train[['YrSold','MoSold', 'SalePrice']]

# 년도별로 group by 해서 Sale_Price의 평균 구하기
group_df = house_train.groupby(['YrSold', 'MoSold'])['SalePrice'].agg('mean').reset_index()

# --------------------------------
# 새로운 'YrMo' 컬럼을 생성하여 시간 축으로 사용
group_df['YrMo'] = group_df['YrSold'].astype(str) + '-' + group_df['MoSold'].astype(str)

# Plotly Express를 사용하여 선 그래프 생성
fig = px.line(group_df, 
              x='YrMo', 
              y='SalePrice', 
              title='월별 평균 SalePrice의 변화 (2006-2010)', 
              labels={'SalePrice':'Average SalePrice', 'YrMo':'Year-Month'})

# x축 레이블 회전 (가독성 향상)
fig.update_xaxes(tickangle=45)

# 그래프 표시
fig.show()
# --------------------------------
# -- 선아 교통수단 ---------------

import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 읽기
transportation = pd.read_csv('data/transportation.csv')

# 2022년 데이터만 필터링
data_2022 = transportation[transportation['Year'] == 2022]

# Group 별로 Commute Means를 집계
grouped_data = data_2022.groupby('Group')['Commute Means'].sum()

# 전체 합계 계산 후 비율로 변환
total_commute = grouped_data.sum()
grouped_data_percentage = (grouped_data / total_commute) * 100

# 파스텔 색상 리스트
colors = plt.cm.Pastel1(range(len(grouped_data_percentage)))

# 원형 그래프 그리기
plt.figure(figsize=(10, 6))  # 그래프의 전체 크기를 조정
plt.pie(grouped_data_percentage, labels=None, autopct='%1.1f%%', startangle=140, colors=colors, textprops={'fontsize': 10}, labeldistance=1.1)

# 라벨을 원 바깥으로 빼고, 라벨과 원을 선으로 연결
plt.legend(grouped_data_percentage.index, title="Commute Types", loc="center left", bbox_to_anchor=(1.0, 0.5), fontsize='small')

plt.title('Commute Means Distribution in 2022', pad=20, fontsize=14)
plt.show()

# ---------------------------------------------------------------------------
import pandas as pd
import numpy as np

import json
geo = json.load(open('bigdata/ia_iowa_zip_codes_geo.min.json', encoding = 'UTF-8'))

def make_ames(num) : 
    postal_code = geo["features"][num]["properties"]['ZCTA5CE10']
    coordinate_list = geo["features"][num]["geometry"]["coordinates"][0]
    coordinate_array = np.array(coordinate_list)
    x = coordinate_array[:, 0].flatten()
    y = coordinate_array[:, 1].flatten()

    return pd.DataFrame({"postal_code" : postal_code, "x":x, "y":y})

# num의 범위 : 935
# make_ames(0)
# make_ames(934)

result = pd.DataFrame({
    'postal_code' : [],
    'x' : [],
    'y' : []
})


for i in range(len(geo["features"])) : 
    result = pd.concat([result, make_ames(i)], ignore_index=True)
    
# ---------------------------------------------------------

# ames랑 waukee 그림 그리기
# ames의 postal codes
# waukee_postal_codes
ames_postal_codes = ['50010', '50011', '50012', '50013', '50014']
waukee_postal_code = ['50003', '50263', '50325']
result['location'] = np.where(result['postal_code'].isin(ames_postal_codes), 'Ames',(
                     np.where(result['postal_code'].isin(waukee_postal_code), 'Waukee','Iowa')
                      ))

import seaborn as sns
import matplotlib.pyplot as plt
sns.scatterplot(data = result, 
                x='x', y='y', 
                hue="location", s=1,
                palette={"Ames":"red", "Iowa":"grey", "Waukee":"blue"}
                )
#---------------------------------------------
result[result['location']=="Ames"]['x'].mean()
result[result['location']=="Ames"]['y'].mean()

result[result['location']=="Waukee"]['x'].mean()
result[result['location']=="Waukee"]['y'].mean()
#---------------------------------------------




#---------------------------------------------
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
plt.title('Iowa Map')
plt.xlabel('경도')
plt.ylabel('위도')
plt.xlim((-97, -89.5))
plt.ylim((40.2, 43.8))
plt.show()
plt.clf()
plt.close()
# ----------------------------------------------

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Ames와 Waukee의 평균 위도, 경도
ames_x_mean = result[result['location'] == "Ames"]['x'].mean()
ames_y_mean = result[result['location'] == "Ames"]['y'].mean()

waukee_x_mean = result[result['location'] == "Waukee"]['x'].mean()
waukee_y_mean = result[result['location'] == "Waukee"]['y'].mean()

# Ames와 Waukee 간의 중간 지점
middle_x = (ames_x_mean + waukee_x_mean) / 2
middle_y = (ames_y_mean + waukee_y_mean) / 2

# 그래프 그리기
sns.scatterplot(data=result, 
                x='x', y='y', 
                hue="location", s=1,
                palette={"Ames":"red", "Iowa":"grey", "Waukee":"blue"}
                )

# 화살표 추가 (Waukee에서 Ames로)
plt.annotate('', xy=(ames_x_mean, ames_y_mean), 
             xytext=(waukee_x_mean, waukee_y_mean),
             arrowprops=dict(facecolor='black', alpha=0.5, shrink=0.05))

# 거리 텍스트 추가 (중간 지점에 50분 표시)
plt.text(middle_x, middle_y, '차량 이동 : 52분', fontsize=12, ha='center')

# 제목 및 라벨 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
plt.title('남Q씨의 이사 경로') 
plt.xlabel('경도')
plt.ylabel('위도')

# 축 범위 조정 (Ames와 Waukee를 확대하여 보기)
plt.xlim((waukee_x_mean - 0.5, ames_x_mean + 0.5))
plt.ylim((waukee_y_mean - 0.5, ames_y_mean + 0.5))

# 레전드 위치 조정 (왼쪽 상단에 고정)
plt.legend(loc='upper left')

# 그래프 표시
plt.show()
plt.clf()
plt.close()

# ----------------------------------------------------
# Waukee랑 Ames시 비교해보자
# 우선 데이터 프레임 만들자
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# 데이터 생성
w_vs_a = pd.DataFrame(
    {"city" : ["Waukee", "Ames"],
     "income" : [106846, 57428],
     "real_estate_price" : [305300, 247500],
     "home_ownership_rate":[70.7, 42],
     "commute_time" : [19.6, 15.8],
     "car" : [2, 2] }
)

# 서브플롯 생성
fig_subplot = make_subplots(
    rows=1, cols=5,
    subplot_titles=("중위 소득($)", "중위 부동산 가격($)", "주택 소유율(%)", "평균 통근 시간(분)", "평균 차량 개수")
)

# 각 서브플롯에 막대 그래프 추가
fig_subplot.add_trace(
    go.Bar(x=w_vs_a['city'], y=w_vs_a['income'], name='Median Income'),
    row=1, col=1
)

fig_subplot.add_trace(
    go.Bar(x=w_vs_a['city'], y=w_vs_a['real_estate_price'], name='Median Real Estate Price'),
    row=1, col=2
)

fig_subplot.add_trace(
    go.Bar(x=w_vs_a['city'], y=w_vs_a['home_ownership_rate'], name='Home Ownership Rate'),
    row=1, col=3
)

fig_subplot.add_trace(
    go.Bar(x=w_vs_a['city'], y=w_vs_a['commute_time'], name='Commute Time'),
    row=1, col=4
)

fig_subplot.add_trace(
    go.Bar(x=w_vs_a['city'], y=w_vs_a['car'], name='Cars'),
    row=1, col=5
)

# 레이아웃 설정
fig_subplot.update_layout(height=600, width=1200, showlegend=False)

# 그래프 표시
fig_subplot.show()

# -------------------------------------------------------------------------
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# 데이터 생성
w_vs_a = pd.DataFrame(
    {"city" : ["Waukee", "Ames"],
     "income" : [106846, 57428],
     "real_estate_price" : [305300, 247500],
     "home_ownership_rate":[70.7, 42],
     "commute_time" : [19.6, 15.8],
     "car" : [2, 2] }
)

# 색상 및 투명도 설정
waukee_color = 'rgba(38, 71, 115, 0.7)'  # Waukee 색상 (남색, 투명도 0.7)
ames_color = 'rgba(255, 255, 153, 0.7)'  # Ames 색상 (
background_color = "#F2F2F2"  
grid_color = 'rgba(128, 128, 128, 0.3)'  # 그리드 색상 (회색, 투명도 0.3)

# 서브플롯 생성
fig_subplot = make_subplots(
    rows=1, cols=5,
    subplot_titles=("중위 소득($)", "중위 부동산 가격($)", "주택 소유율(%)", "평균 통근 시간(분)", "평균 차량 개수")
)

# 각 서브플롯에 막대 그래프 추가
fig_subplot.add_trace(
    go.Bar(x=w_vs_a['city'], y=w_vs_a['income'], 
           marker_color=[waukee_color, ames_color], name='Median Income'),
    row=1, col=1
)

fig_subplot.add_trace(
    go.Bar(x=w_vs_a['city'], y=w_vs_a['real_estate_price'], 
           marker_color=[waukee_color, ames_color], name='Median Real Estate Price'),
    row=1, col=2
)

fig_subplot.add_trace(
    go.Bar(x=w_vs_a['city'], y=w_vs_a['home_ownership_rate'], 
           marker_color=[waukee_color, ames_color], name='Home Ownership Rate'),
    row=1, col=3
)

fig_subplot.add_trace(
    go.Bar(x=w_vs_a['city'], y=w_vs_a['commute_time'], 
           marker_color=[waukee_color, ames_color], name='Commute Time'),
    row=1, col=4
)

fig_subplot.add_trace(
    go.Bar(x=w_vs_a['city'], y=w_vs_a['car'], 
           marker_color=[waukee_color, ames_color], name='Cars'),
    row=1, col=5
)

# 레이아웃 설정
fig_subplot.update_layout(
    height=600, width=1200, showlegend=False,
    plot_bgcolor=background_color,  # 그래프 배경색
    paper_bgcolor=background_color,  # 전체 배경색
    font=dict(color="gray"),  # 폰트 색상
    xaxis=dict(gridcolor=grid_color),  # X축 그리드 색상
    yaxis=dict(gridcolor=grid_color)   # Y축 그리드 색상
)

# 각 서브플롯의 그리드 색상 설정 (모든 서브플롯에 동일하게 적용)
for i in range(1, 6):
    fig_subplot['layout'][f'xaxis{i}']['gridcolor'] = grid_color
    fig_subplot['layout'][f'yaxis{i}']['gridcolor'] = grid_color

# 그래프 표시
fig_subplot.show()
# -----------------------------------------------------------------------
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# 데이터 생성
w_vs_a = pd.DataFrame(
    {"city" : ["Waukee", "Ames"],
     "income" : [106846, 57428],
     "real_estate_price" : [305300, 247500],
     "home_ownership_rate":[70.7, 42],
     "commute_time" : [19.6, 15.8],
     "car" : [2, 2] }
)

# 감소율 계산 함수
def calculate_percentage_decrease(waukee_value, ames_value):
    return ((waukee_value - ames_value) / waukee_value) * 100

# 각 항목에 대한 감소율 계산
income_decrease = calculate_percentage_decrease(w_vs_a['income'][0], w_vs_a['income'][1])
real_estate_price_decrease = calculate_percentage_decrease(w_vs_a['real_estate_price'][0], w_vs_a['real_estate_price'][1])
home_ownership_rate_decrease = calculate_percentage_decrease(w_vs_a['home_ownership_rate'][0], w_vs_a['home_ownership_rate'][1])
commute_time_decrease = calculate_percentage_decrease(w_vs_a['commute_time'][0], w_vs_a['commute_time'][1])
car_decrease = calculate_percentage_decrease(w_vs_a['car'][0], w_vs_a['car'][1])

# 서브플롯 생성
fig_subplot = make_subplots(
    rows=1, cols=5,
    subplot_titles=("중위 소득($)", "중위 부동산 가격($)", "주택 소유율(%)", "평균 통근 시간(분)", "평균 차량 개수")
)

# 색상 및 투명도 설정
waukee_color = 'rgba(38, 71, 115, 0.7)'  # Waukee 색상 (남색, 투명도 0.7)
ames_color = 'rgba(255, 255, 153, 0.7)'  # Ames 색상 (
background_color = "white"
grid_color = 'rgba(128, 128, 128, 0.3)'  # 그리드 색상 (회색, 투명도 0.3)

# 각 서브플롯에 막대 그래프 추가
fig_subplot.add_trace(
    go.Bar(x=w_vs_a['city'], y=w_vs_a['income'], 
           marker_color=[waukee_color, ames_color], name='Median Income'),
    row=1, col=1
)

fig_subplot.add_trace(
    go.Bar(x=w_vs_a['city'], y=w_vs_a['real_estate_price'], 
           marker_color=[waukee_color, ames_color], name='Median Real Estate Price'),
    row=1, col=2
)

fig_subplot.add_trace(
    go.Bar(x=w_vs_a['city'], y=w_vs_a['home_ownership_rate'], 
           marker_color=[waukee_color, ames_color], name='Home Ownership Rate'),
    row=1, col=3
)

fig_subplot.add_trace(
    go.Bar(x=w_vs_a['city'], y=w_vs_a['commute_time'], 
           marker_color=[waukee_color, ames_color], name='Commute Time'),
    row=1, col=4
)

fig_subplot.add_trace(
    go.Bar(x=w_vs_a['city'], y=w_vs_a['car'], 
           marker_color=[waukee_color, ames_color], name='Cars'),
    row=1, col=5
)

# 레이아웃 설정
fig_subplot.update_layout(
    height=600, width=1200, showlegend=False,
    plot_bgcolor=background_color,  # 그래프 배경색
    paper_bgcolor=background_color,  # 전체 배경색
    font=dict(color="gray"),  # 폰트 색상
    xaxis=dict(gridcolor=grid_color),  # X축 그리드 색상
    yaxis=dict(gridcolor=grid_color)   # Y축 그리드 색상
)

# 각 서브플롯의 그리드 색상 설정 (모든 서브플롯에 동일하게 적용)
for i in range(1, 6):
    fig_subplot['layout'][f'xaxis{i}']['gridcolor'] = grid_color
    fig_subplot['layout'][f'yaxis{i}']['gridcolor'] = grid_color

# 각 서브플롯의 X축 레이블에 퍼센트 감소값 추가
fig_subplot.update_xaxes(
    title_text=f"{income_decrease:.1f}% 감소", row=1, col=1
)

fig_subplot.update_xaxes(
    title_text=f"{real_estate_price_decrease:.1f}% 감소", row=1, col=2
)

fig_subplot.update_xaxes(
    title_text=f"{home_ownership_rate_decrease:.1f}% 감소", row=1, col=3
)

fig_subplot.update_xaxes(
    title_text=f"{commute_time_decrease:.1f}% 감소", row=1, col=4
)

fig_subplot.update_xaxes(
    title_text="동일", row=1, col=5
)

fig_subplot.show()

#---------------------------------------

import pandas as pd
import plotly.express as px

# Load the CSV file
race = pd.read_csv('data/race.csv')

# Convert column names to lowercase
race.columns = race.columns.str.lower()

# Map English race names to Korean
race_name_mapping = {
    'White Alone': '백인',
    'Black or African American Alone': '흑인 또는 아프리카계 미국인',
    'American Indian & Alaska Native Alone': '아메리카 인디언 & 알래스카 원주민',
    'Asian Alone': '아시아인',
    'Native Hawaiian & Other Pacific Islander Alone': '하와이 원주민 및 기타 태평양 섬 주민',
    'Some Other Race Alone': '기타 인종',
    'Two or More Races': '두 개 이상의 인종'
}

# Apply the mapping to the race column
race['race'] = race['race'].map(race_name_mapping)

# Filter the dataset to only include necessary columns
race_filtered = race[['year', 'race', 'share']]

# Ensure that the data is complete and continuous by sorting and filling any missing values
race_complete = race_filtered.pivot(index='year', columns='race', values='share').interpolate().reset_index()

# Convert the data back to long format for Plotly
race_long = pd.melt(race_complete, id_vars=['year'], value_vars=race_name_mapping.values(), var_name='race', value_name='share')

# Create an interactive line chart using Plotly
fig = px.line(
    race_long, 
    x='year', 
    y='share', 
    color='race', 
    labels={
        'year': '연도',
        'share': '인구 비율 (%)',
        'race': '인종'
    },
    title='연도별 인종 인구 비율'
)

# Ensure that all points are connected by lines
fig.update_traces(mode='lines+markers')

# Set default visibility for each trace to 'legendonly' so that only one trace is visible initially
fig.for_each_trace(lambda trace: trace.update(visible='legendonly'))

# Optionally, make one trace visible initially, e.g., '아시아인'
fig.update_traces(selector=dict(name='아시아인'), visible=True)

# Update layout to make the plot interactive with the ability to select/deselect races
fig.update_layout(
    xaxis_title='연도',
    yaxis_title='인구 비율 (%)',
    hovermode='closest',
    legend_title_text='인종'
)

# Show the plot
fig.show()

# -------------------------------------------------------
# 매물 선택
# 라이브러리 호출
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 데이터 불러오기
house_data = pd.read_csv('data/house_loc.csv', index_col=0)
house = house_data.copy()
# house는 2930개 열이 있음

# 어떤 변수를 쓸까?
# 1. 우선 한국처럼 모든 Utilities가 AllPub: 모든 공공 유틸리티 (전기, 가스, 수도, 하수) 
# 모두 제공되면 좋겠어 - 2927개 필터링 조건 1
house = house[house['Utilities']=='AllPub']

# 2. 샤워 가능 화장실 1개 이상 & 간이 화장실 1개 이상 
# 샤워 가능 화장실 변수 생성 - FullBath
# house.loc[:, ['Bsmt_Full_Bath', 'Full_Bath']]
house['FullBath'] = house['Bsmt_Full_Bath'] + house['Full_Bath'] 

# 간이 화장실 변수 생성 - HalfBath
# house.loc[:, ['Bsmt_Half_Bath', 'Half_Bath']]
house['HalfBath'] = house['Bsmt_Half_Bath'] + house['Half_Bath'] 

# 화장실 변수 살펴보자능
house.loc[:, ['FullBath', 'HalfBath']]

# 여기서 FullBath>=1, HalfBath>=1인 조건을 걸어보면, 1220개의 행이 나옴
house = house[(house['FullBath'] >= 1) & (house['HalfBath'] >= 1)]

# 3. 차가 2대 이상 있어서, 2대 이상의 차고를 원해, 971개의 행으로 줄여짐
house = house[house['Garage_Cars']>=2]

# 4. Ames시의 겨울은 눈이 오고 섭씨 영하 15도까지 내려가 많이 와서 춥더군. 
#    크리스마스도 보내고 싶어서 난로가 1개이상 있으면 좋겠어, 706개의 행으로 줄어듬
house = house[house['Fireplaces']>=1]

# 5. 난방 품질이 우수하면 좋겠고, 중앙 에어컨 시스템이 있어야해 # 477개 행
house = house[(house['Heating_QC']=='Excellent') & (house['Central_Air']=='Y')]

# 6. 나무로 된 데크를 좀 평균 이상 넓이로 가지고 싶어 # 240개 행
house = house[house['Wood_Deck_SF'] >= house['Wood_Deck_SF'].mean()]

house
