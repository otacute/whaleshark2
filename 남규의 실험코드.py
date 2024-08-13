#===================================================================================================================================================
spot_image = ['https://lh3.googleusercontent.com/p/AF1QipNIeO-1wG3PNNjN1iK_ZXasKnTQORErtmOhvRgS=s680-w680-h510',
              'https://lh3.googleusercontent.com/p/AF1QipPDMW-e0ala8_n82T1jX6HG_JWWflfIDSxd6Exy=s680-w680-h510',
              'https://amescsd.org/app/uploads/sites/8/2022/04/Sawyer-Main-Image-scaled-e1649709450394-3000x1000-c-default.jpg',
              'https://lh5.googleusercontent.com/p/AF1QipPhBH-d9SM-8PHt0cfuyRO8VszsLiLwNyeACx0=w540-h312-n-k-no',
              'https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Hilton_Coliseum_Inside_View.jpg/250px-Hilton_Coliseum_Inside_View.jpg',
              'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQxQewscpasg669ypQmNvqdoBqBA0jgiyp8w&sg',
              'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSYuMQzhyB9qyl8eP1LRuEIJxdcVAEQ42T4lQHaWJpZD16aZGQ8qXJKqXfCEA&s',
              'https://lh3.googleusercontent.com/p/AF1QipNKRtVDRmvx3OtNnix6GgYkVe6a-eD_0qM1x9dI=s680-w680-h510',
              'https://lh3.googleusercontent.com/p/AF1QipPIW7KoRYYBPXsU3lXCP_LwPOUw5pOFftLeqLWd=s680-w680-h510',
              'https://lh3.googleusercontent.com/p/AF1QipNmY43hWQw_BVhT1AF9zzaeYuPCCkThavee8px3=s680-w680-h510',
              'https://lh3.googleusercontent.com/p/AF1QipMqzpEh8vwJsxiRNvgiZgAozwe4yVJ5PBipAsRZ=s1360-w1360-h1020',
              'https://lh3.googleusercontent.com/p/AF1QipPjZiW8ejuvi7pvr8_Augg0Rb5j7LEchpNKo6Kh=s1360-w1360-h1020',
              'https://www.amestrib.com/gcdn/authoring/authoring-images/2024/02/26/NATR/72747516007-226-ams-building-photos-1.jpg?width=660&height=364&fit=crop&format=pjpg&auto=webp'
              ]

hot_spot_add = hot_spot
hot_spot_add['image'] = spot_image 

fig = go.Figure(go.Scattermapbox(
  lat = hot_spot['Latitude'], lon = hot_spot['Longitude'],
  mode = 'markers+text',
  marker = dict(symbol = 'marker', size = 15, color = 'blue'),
  text = hot_spot['Spot'], textposition = 'top center', customdata = hot_spot_add['image'],
  hovertemplate = '<b>%{text}</b><br><img src="%{customdata}" height="100"><extra></extra>'))
  
fig.update_layout(title = dict(text = '에임스 주요시설', x = 0.5),
                  autosize = True, hovermode='closest',
                  mapbox = dict(accesstoken = 'pk.eyJ1IjoibmFtcSIsImEiOiJjbHpub2Q4bzUwc2ozMnBweXd4OW9mbm9mIn0.qc2xzGw9Za-ftKFZkDrCcA',
                                bearing = 0, center = dict(lon = -93.642897, lat = 42.034482),
                                pitch = 0, zoom = 10, style = 'light'))
fig.show()

## 실험일지
## plotly에 folium으로 만든 지도처럼 이미지를 넣으려고 했으나 실패했다.
## 아무래도 Scattermapbox에서 사용자 정의 아이콘 사용해야하는것 같다.
#===================================================================================================================================================






# 집위치 데이터 표시=============================================================
house = pd.read_csv('data/house_loc.csv')
house.rename(columns={'Unnamed: 0': 'Id'}, inplace=True)

house_loc = house.iloc[:, -2:]
map_sig = folium.Map(location = [42.034482, -93.642897],
                     zoom_start = 10,
                     tiles = 'cartodbpositron')

for i in range(2930):
  folium.Circle([house_loc.iloc[i,1], house_loc.iloc[i,0]],
                radius = 5, popup = str(i)).add_to(map_sig)
map_sig.save('map_ames.html')
#================================================================================









# 주요시설 위치 데이터 표시======================================================
spot_loc = hot_spot.iloc[:,2:]

for i in range(12):
  folium.Marker([spot_loc.iloc[i,0], spot_loc.iloc[i,1]], popup = str(hot_spot['Spot'][i]),
                 icon=folium.Icon(color='red', icon='info-sign')).add_to(map_sig)
map_sig.save('map_ames.html')
#================================================================================








#===========================================================================================================================
# Ames Public Library
image_url = "https://lh3.googleusercontent.com/p/AF1QipNIeO-1wG3PNNjN1iK_ZXasKnTQORErtmOhvRgS=s680-w680-h510"
popup_html = f"""
<div>
    <img src="{image_url}" alt="Spot Image" style="width: 300px; height: auto;"/>
    <p>Ames Public Library</p>
</div>
"""
folium.Marker([spot_loc.iloc[0,0], spot_loc.iloc[0,1]], popup = folium.Popup(popup_html, max_width=300),
               icon=folium.Icon(color='red', icon='info-sign')).add_to(map_sig)
map_sig.save('map_ames.html')

# Mitchel
image_url = "https://lh3.googleusercontent.com/p/AF1QipPDMW-e0ala8_n82T1jX6HG_JWWflfIDSxd6Exy=s680-w680-h510"
popup_html = f"""
<div>
    <img src="{image_url}" alt="Spot Image" style="width: 300px; height: auto;"/>
    <p>Mitchel</p>
</div>
"""
folium.Marker([spot_loc.iloc[1,0], spot_loc.iloc[1,1]], popup = folium.Popup(popup_html, max_width=300),
               icon=folium.Icon(color='red', icon='info-sign')).add_to(map_sig)
map_sig.save('map_ames.html')

# Sawyer
image_url = "https://amescsd.org/app/uploads/sites/8/2022/04/Sawyer-Main-Image-scaled-e1649709450394-3000x1000-c-default.jpg"
popup_html = f"""
<div>
    <img src="{image_url}" alt="Spot Image" style="width: 300px; height: auto;"/>
    <p>Sawyer</p>
</div>
"""
folium.Marker([spot_loc.iloc[2,0], spot_loc.iloc[2,1]], popup = folium.Popup(popup_html, max_width=300),
               icon=folium.Icon(color='red', icon='info-sign')).add_to(map_sig)
map_sig.save('map_ames.html')

# Reiman Gardens
image_url = "https://lh5.googleusercontent.com/p/AF1QipPhBH-d9SM-8PHt0cfuyRO8VszsLiLwNyeACx0=w540-h312-n-k-no"
popup_html = f"""
<div>
    <img src="{image_url}" alt="Spot Image" style="width: 300px; height: auto;"/>
    <p>Reiman Gardens</p>
</div>
"""
folium.Marker([spot_loc.iloc[3,0], spot_loc.iloc[3,1]], popup = folium.Popup(popup_html, max_width=300),
               icon=folium.Icon(color='red', icon='info-sign')).add_to(map_sig)
map_sig.save('map_ames.html')

# Hilton Coliseum
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Hilton_Coliseum_Inside_View.jpg/250px-Hilton_Coliseum_Inside_View.jpg"
popup_html = f"""
<div>
    <img src="{image_url}" alt="Spot Image" style="width: 300px; height: auto;"/>
    <p>Hilton Coliseum</p>
</div>
"""
folium.Marker([spot_loc.iloc[4,0], spot_loc.iloc[4,1]], popup = folium.Popup(popup_html, max_width=300),
               icon=folium.Icon(color='red', icon='info-sign')).add_to(map_sig)
map_sig.save('map_ames.html')

# Stephens Auditorium
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQxQewscpasg669ypQmNvqdoBqBA0jgiyp8w&sg"
popup_html = f"""
<div>
    <img src="{image_url}" alt="Spot Image" style="width: 300px; height: auto;"/>
    <p>Stephens Auditorium</p>
</div>
"""
folium.Marker([spot_loc.iloc[5,0], spot_loc.iloc[5,1]], popup = folium.Popup(popup_html, max_width=300),
               icon=folium.Icon(color='red', icon='info-sign')).add_to(map_sig)
map_sig.save('map_ames.html')

# Farm House Museum
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSYuMQzhyB9qyl8eP1LRuEIJxdcVAEQ42T4lQHaWJpZD16aZGQ8qXJKqXfCEA&s"
popup_html = f"""
<div>
    <img src="{image_url}" alt="Spot Image" style="width: 300px; height: auto;"/>
    <p>Farm House Museum</p>
</div>
"""
folium.Marker([spot_loc.iloc[6,0], spot_loc.iloc[6,1]], popup = folium.Popup(popup_html, max_width=300),
               icon=folium.Icon(color='red', icon='info-sign')).add_to(map_sig)
map_sig.save('map_ames.html')


# Iowa State University
image_url = "https://lh3.googleusercontent.com/p/AF1QipNKRtVDRmvx3OtNnix6GgYkVe6a-eD_0qM1x9dI=s680-w680-h510"
popup_html = f"""
<div>
    <img src="{image_url}" alt="Spot Image" style="width: 300px; height: auto;"/>
    <p>Iowa State University</p>
</div>
"""
folium.Marker([spot_loc.iloc[7,0], spot_loc.iloc[7,1]], popup = folium.Popup(popup_html, max_width=300),
               icon=folium.Icon(color='red', icon='info-sign')).add_to(map_sig)
map_sig.save('map_ames.html')

# Furman Aquatic Center
image_url = "https://lh3.googleusercontent.com/p/AF1QipPIW7KoRYYBPXsU3lXCP_LwPOUw5pOFftLeqLWd=s680-w680-h510"
popup_html = f"""
<div>
    <img src="{image_url}" alt="Spot Image" style="width: 300px; height: auto;"/>
    <p>Furman Aquatic Center</p>
</div>
"""
folium.Marker([spot_loc.iloc[8,0], spot_loc.iloc[8,1]], popup = folium.Popup(popup_html, max_width=300),
               icon=folium.Icon(color='red', icon='info-sign')).add_to(map_sig)
map_sig.save('map_ames.html')


# Tom Evans Plaza
image_url = "https://lh3.googleusercontent.com/p/AF1QipNmY43hWQw_BVhT1AF9zzaeYuPCCkThavee8px3=s680-w680-h510"
popup_html = f"""
<div>
    <img src="{image_url}" alt="Spot Image" style="width: 300px; height: auto;"/>
    <p>Tom Evans Plaza</p>
</div>
"""
folium.Marker([spot_loc.iloc[9,0], spot_loc.iloc[9,1]], popup = folium.Popup(popup_html, max_width=300),
               icon=folium.Icon(color='red', icon='info-sign')).add_to(map_sig)
map_sig.save('map_ames.html')


# Octagon Center For the Arts
image_url = "https://lh3.googleusercontent.com/p/AF1QipMqzpEh8vwJsxiRNvgiZgAozwe4yVJ5PBipAsRZ=s1360-w1360-h1020"
popup_html = f"""
<div>
    <img src="{image_url}" alt="Spot Image" style="width: 300px; height: auto;"/>
    <p>Octagon Center For the Arts</p>
</div>
"""
folium.Marker([spot_loc.iloc[10,0], spot_loc.iloc[10,1]], popup = folium.Popup(popup_html, max_width=300),
               icon=folium.Icon(color='red', icon='info-sign')).add_to(map_sig)
map_sig.save('map_ames.html')


# Ames High School
image_url = "https://lh3.googleusercontent.com/p/AF1QipPjZiW8ejuvi7pvr8_Augg0Rb5j7LEchpNKo6Kh=s1360-w1360-h1020"
popup_html = f"""
<div>
    <img src="{image_url}" alt="Spot Image" style="width: 300px; height: auto;"/>
    <p>Ames High School</p>
</div>
"""
folium.Marker([spot_loc.iloc[11,0], spot_loc.iloc[11,1]], popup = folium.Popup(popup_html, max_width=300),
               icon=folium.Icon(color='red', icon='info-sign')).add_to(map_sig)
map_sig.save('map_ames.html')


# Ames Middle School
image_url = "https://www.amestrib.com/gcdn/authoring/authoring-images/2024/02/26/NATR/72747516007-226-ams-building-photos-1.jpg?width=660&height=364&fit=crop&format=pjpg&auto=webp"
popup_html = f"""
<div>
    <img src="{image_url}" alt="Spot Image" style="width: 300px; height: auto;"/>
    <p>Ames Middle School</p>
</div>
"""
folium.Marker([spot_loc.iloc[12,0], spot_loc.iloc[12,1]], popup = folium.Popup(popup_html, max_width=300),
               icon=folium.Icon(color='red', icon='info-sign')).add_to(map_sig)
map_sig.save('map_ames.html')
#===========================================================================================================================
