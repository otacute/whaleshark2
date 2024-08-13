# 수빈 :

# !pip install pandas
# !pip install seaborn
# !pip install folium
# !pip install nbformat
# !pip install --upgrade nbformat
# !pip install pyyaml
# !conda install jupyter

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import folium
import plotly.express as px
import plotly.graph_objects as go


gsheet_url = "https://docs.google.com/spreadsheets/d/1McH-oBzPZ8ewfyEl605wq-9b3gZHCIIBVbWHEHwNnIs/gviz/tq?tqx=out:csv&sheet=ames-spot"
hot_spot= pd.read_csv(gsheet_url)
hot_spot.head()

house_loc = pd.read_csv('C:/Users/USER/Documents/LS빅데이터스쿨/whaleshark/data/house_loc.csv')

house_loc.head()
house_loc_df = house_loc
data_to_plot = house_loc[['Year_Sold', 'Sale_Price']]


# 년도별로 group by 해서 Sale_Price의 평균 구하기
group_df = house_loc_df.groupby('Year_Sold')['Sale_Price'].agg('mean').reset_index()

fig = px.scatter(
    data_to_plot, 
    x='Year_Sold', 
    y='Sale_Price', 
    animation_frame='Year_Sold', 
    animation_group='Sale_Price', 
    range_y=[data_to_plot['Sale_Price'].min(), data_to_plot['Sale_Price'].max()],
    title="Sale Price Trend by Year",
    labels={
        "Year_Sold": "Year Sold",
        "Sale_Price": "Sale Price"
    }
)
fig.show(renderer="browser")
# 그래프 표시
# fig.show()
