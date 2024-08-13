# 선아: 
# !pip install dash dash-core-components dash-html-components plotly pandas
# !pip install folium
# 선아 :
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import folium
import plotly.graph_objects as go
import os

cwd = os.getcwd()  # 현재 작업 디렉토리 확인
print("Current working directory:", cwd)

# 경로 변경
os.chdir('C:\\Users\\USER\\Documents\\LS빅데이터스쿨\\whaleshark\\')

# 변경된 작업 디렉토리 확인
print("New working directory:", os.getcwd())


margins_P = {'t' : 50, 'b' : 25, 'l' : 35, 'r' : 25}

#년도와 월별 평균 집 가격구하기
house = pd.read_csv('./data/house_loc.csv')
train = pd.read_csv('./data/train.csv')

train['YrMoSold'] = train['YrSold'].astype(str) + "-" + train["MoSold"].astype(str)
df= train.groupby(['YrSold', 'MoSold'], as_index=False).agg(YrMo_mean = ('SalePrice', 'mean'))
df['YrMoSold'] = pd.to_datetime(df['YrSold'].astype(str) + "-" + df['MoSold'].astype(str))

frames = []
dates = df['YrMoSold'].sort_values().unique()

for date in dates:
    frame_data = {
        "data": [
            {
                "type": "scatter",
                "mode": "markers",
                "x": df[df["YrMoSold"] <= date]["YrMoSold"],
                "y": df[df["YrMoSold"] <= date]["YrMo_mean"],
                "marker": {"color": "red"}
            },
            {
                "type": "scatter",
                "mode": "lines",
                "x": df[df["YrMoSold"] <= date]["YrMoSold"],
                "y": df[df["YrMoSold"] <= date]["YrMo_mean"],
                "line": {"color": "blue", "dash": "dash"}
            }
        ],
        "name": str(date)
    }
    frames.append(frame_data)

# 애니메이션을 위한 레이아웃 설정


last_date = dates[-1]
max_y = df['YrMo_mean'].max()
min_y = df['YrMo_mean'].min()


margins_P = {"l": 25, "r": 25, "t": 50, "b": 50}
layout = {
    "title": "년도별 SalePrice 변화",
    "xaxis": {"title": "날짜", "showgrid": False, "range": [df["YrMoSold"].min(), df["YrMoSold"].max()]},
    "yaxis": {"title": "가격", "range": [min_y, max_y]},
    "margin": margins_P,
    "updatemenus": [{
        "type": "buttons",
        "showactive": False,
        "buttons": [{
            "label": "Play",
            "method": "animate",
            "args": [None, {"frame": {"duration": 300, "redraw": True}, "fromcurrent": True}]
        }, {
            "label": "Pause",
            "method": "animate",
            "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}]
        }]
    }]
}

# Figure 생성
fig = go.Figure(
    data=[
        {
            "type": "scatter",
            "mode": "markers",
            "x": df['YrMoSold'],
            "y": df['YrMo_mean'],
            "marker": {"color": "red"}
        },
        {
            "type": "scatter",
            "mode": "lines",
           "x": df['YrMoSold'],
            "y": df['YrMo_mean'],
            "line": {"color": "blue", "dash": "dash"}
        }
    ],
    layout=layout,
    frames=frames
)

fig.show()

