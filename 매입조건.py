# 매물 선택
# 라이브러리 호출
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 데이터 불러오기
house_data = pd.read_csv('data/house_loc.csv', index_col=0)
house = house_data.copy()

# 어떤 변수를 쓸까?
# 1. 우선 한국처럼 모든 Utilities가 AllPub: 모든 공공 유틸리티 (전기, 가스, 수도, 하수) 모두 제공되면 좋겠어
house['Utilities'].value_counts()
# 모든 집이 이미 모든 공공 유틸리티를 제공하고 있었어

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

# house['Heating_QC'].value_counts()
# house.columns
# ------------------------
