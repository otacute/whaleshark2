# google sheet pandas로 읽어오는 방법

import pandas as pd

# https://docs.google.com/spreadsheets/d/1McH-oBzPZ8ewfyEl605wq-9b3gZHCIIBVbWHEHwNnIs/edit?gid=941998772#gid=941998772
gsheet_url = "https://docs.google.com/spreadsheets/d/1McH-oBzPZ8ewfyEl605wq-9b3gZHCIIBVbWHEHwNnIs/gviz/tq?tqx=out:csv&sheet=ames-spot"

df = pd.read_csv(gsheet_url)
df

!pip install pyyaml
!conda install jupyter
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
make_ames(0)
make_ames(934)

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

# ames만 그림 그리기
# ames의 postal codes
ames_postal_codes = ['50010', '50011', '50012', '50013', '50014']
result['location'] = np.where(result['postal_code'].isin(ames_postal_codes), 'Ames', 'Iowa')
result

result[result['location'] == "Ames"]

import seaborn as sns
sns.scatterplot(data = result, 
                x='x', y='y', 
                hue="location", s=1,
                palette={"Ames":"red", "Iowa":"grey"}
                )
plt.xlim((-97, -89.5))
plt.ylim((40.2, 43.8))
plt.show()
plt.clf()

# ---------------------------------------------------------

