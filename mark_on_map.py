import pandas as pd
import folium
from geopy.geocoders import Nominatim
from folium.plugins import MarkerCluster
import time
import os

# 设置代理，如果你在需要通过特定代理访问Internet的环境中
os.environ['http_proxy'] = 'http://127.0.0.1:15732'
os.environ['https_proxy'] = 'http://127.0.0.1:15732'

# 读取地名数据
location_df = pd.read_excel("Paradise.xlsx")

# 初始化地图
m = folium.Map(location=[20, 0], zoom_start=2)

# 使用有意义的用户代理名来初始化地理编码器
geolocator = Nominatim(user_agent="willow984@qq.com")  # 使用你的应用名或你的邮箱

# 初始化标记群集
marker_cluster = MarkerCluster().add_to(m)

# 通过地名获取坐标并添加到地图
for index, row in location_df.iterrows():
    try:
        location = geolocator.geocode(row['Location'], timeout=10)
        if location:
            folium.Marker(
                location=[location.latitude, location.longitude],
                popup=f"{row['Location']} ({row['Count']} times)",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(marker_cluster)
        time.sleep(1)  # 延时以遵守Nominatim的请求频率限制
    except Exception as e:
        print(f"Error geocoding {row['Location']}: {e}")

# 保存地图
m.save("Paradise.html")
