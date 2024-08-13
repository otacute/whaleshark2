# 남규 :

#!pip install dash dash-core-components dash-html-components plotly pandas
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import folium
import plotly.express as px
import plotly.graph_objects as go



# 대쉬보드 이용해서 시각화하기=============================================================================================

gsheet_url = "https://docs.google.com/spreadsheets/d/1McH-oBzPZ8ewfyEl605wq-9b3gZHCIIBVbWHEHwNnIs/gviz/tq?tqx=out:csv&sheet=ames-spot"

hot_spot= pd.read_csv(gsheet_url)

house = pd.read_csv('data/house_loc.csv')
house.rename(columns={'Unnamed: 0': 'Id'}, inplace=True)

fig = go.Figure(go.Scattermapbox(
  lat = hot_spot['Latitude'], lon = hot_spot['Longitude'],
  mode = 'markers+text',
  marker = dict(symbol = 'marker', size = 15, color = 'blue'),
  text = hot_spot['Spot'], textposition = 'top center'))
  
fig.update_layout(title = dict(text = '에임스 주요시설', x = 0.5),
                  autosize = True, hovermode='closest',
                  mapbox = dict(accesstoken = 'pk.eyJ1IjoibmFtcSIsImEiOiJjbHpub2Q4bzUwc2ozMnBweXd4OW9mbm9mIn0.qc2xzGw9Za-ftKFZkDrCcA',
                                bearing = 0, center = dict(lon = -93.642897, lat = 42.034482),
                                pitch = 0, zoom = 12, style = 'light'))

fig.add_trace(go.Scattermapbox(
    lat=house['Latitude'],
    lon=house['Longitude'],
    mode='markers',
    marker=dict(symbol='circle', size=5, color='red'),
    text=house['Id'].astype(str),
    textposition='top right',
    hovertemplate='<b>House ID: %{text}</b><extra></extra>',
    name='Houses'))

fig.show()


# 나중에 혹시 카테고리별로 아이콘 바꿀때 사용할 코드======================================================================
hot_spot['Category'].unique()

spot_Cultural = hot_spot.query("Category == 'Cultural'")
spot_Education = hot_spot.query("Category == 'Education'")
spot_Leisure = hot_spot.query("Category == 'Leisure'")



fig = go.Figure(go.Scattermapbox(
  lat = spot_Cultural.iloc[:, -2], lon = spot_Cultural.iloc[:, -1],
  mode = 'markers+text',
  marker = dict(symbol = 'star', size = 15, color = 'blue'),
  text = hot_spot['Spot'], textposition = 'top center'))          # Cultureal 표시

fig.add_trace(go.Scattermapbox(
    lat=spot_Education.iloc[:, -2],
    lon=spot_Education.iloc[:, -1],
    mode='markers+text',
    marker=dict(symbol='star', size=15, color='blue'),
    text=hot_spot['Spot'],
    textposition='top center'))

fig.add_trace(go.Scattermapbox(
    lat=spot_Leisure.iloc[:, -2],
    lon=spot_Leisure.iloc[:, -1],
    mode='markers+text',
    marker=dict(symbol='star', size=15, color='blue'),
    text=hot_spot['Spot'],
    textposition='top center'))

fig.add_trace(go.Scattermapbox(
    lat=house['Latitude'],
    lon=house['Longitude'],
    mode='markers',
    marker=dict(symbol='circle', size=5, color='red'),
    text=house['Id'].astype(str),
    textposition='top right',
    hovertemplate='<b>House ID: %{text}</b><extra></extra>',
    name='Houses'))

fig.update_layout(title = dict(text = '에임스 주요시설', x = 0.5),
                  autosize = True, hovermode='closest',
                  mapbox = dict(accesstoken = 'pk.eyJ1IjoibmFtcSIsImEiOiJjbHpub2Q4bzUwc2ozMnBweXd4OW9mbm9mIn0.qc2xzGw9Za-ftKFZkDrCcA',
                                bearing = 0, center = dict(lon = -93.642897, lat = 42.034482),
                                pitch = 0, zoom = 12, style = 'light'))

fig.show()
#===========================================================================================================================

train = pd.read_csv('data/train.csv')
train.info()
train[['Id', 'MoSold', 'YrSold', 'SalePrice']]
df = train.groupby('YrSold', as_index = False) \
          .agg(sale_mean = ('SalePrice', 'mean'))
train['YrSold'].unique()


margins_P = {'t' : 50, 'b' : 25, 'l' : 35, 'r' : 25}

fig = go.Figure(
  data = [
    {'type'   : 'scatter',
     'mode'   : 'markers',
     'x'      : df['YrSold'],
     'y'      : df['sale_mean'],
     'marker' : {'color' : 'red'}
     },
     {'type'   : 'scatter',
      'mode'   : 'lines',
      'x'      : df['YrSold'],
      'y'      : df['sale_mean'],
      'line'   : {'color' : 'blue', 'dash' : 'dash'}
      }
  ],
 layout = {
     'title'  : "연도별 부동산 평균가격",
     'xaxis'  : {'title'    : '연도도',
                 'showgrid' : False},
     'yaxis'  : {'title' : '평균가격격'},
     'margin' : margins_P
     }
)
fig.show()

frames = []
dates = df['YrSold'].unique()

for date in dates:
    frame_data = {
        "data": [
            {
                "type": "scatter",
                "mode": "markers",
                "x": df[df["YrSold"] <= date]["YrSold"],
                "y": df[df["YrSold"] <= date]["sale_mean"],
                "marker": {"color": "red"}
            },
            {
                "type": "scatter",
                "mode": "lines",
                "x": df[df["YrSold"] <= date]["YrSold"],
                "y": df[df["YrSold"] <= date]["sale_mean"],
                "line": {"color": "blue", "dash": "dash"}
            }
        ],
        "name": str(date)
    }
    frames.append(frame_data)

# 애니메이션을 위한 레이아웃 설정


last_date = dates[-1]
max_y = df['sale_mean'].max()
min_y = df['sale_mean'].min()


margins_P = {"l": 25, "r": 25, "t": 50, "b": 50}
layout = {
    "title": "코로나 19 발생현황",
    "xaxis": {"title": "날짜", "showgrid": False, "range": [df["YrSold"].min(), df["YrSold"].max()]},
    "yaxis": {"title": "확진자수", "range": [min_y, max_y]},
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
            "x": df['YrSold'],
            "y": df['sale_mean'],
            "marker": {"color": "red"}
        },
        {
            "type": "scatter",
            "mode": "lines",
           "x": df['YrSold'],
            "y": df['sale_mean'],
            "line": {"color": "blue", "dash": "dash"}
        }
    ],
    layout=layout,
    frames=frames
)

fig.show()

