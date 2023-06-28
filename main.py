import json
import requests
import calendar
import datetime


def dateprocess(str):
  year = str[0:4]
  month = str[4:6]
  day = str[6:9]
  return year,month,day


res = requests.get("https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=tc")
data=json.loads(res.text)

print("天氣概況：",data['generalSituation'],"\n")
for i in range(0,9):
  year = int(dateprocess(data["weatherForecast"][i]["forecastDate"])[0])
  month = int(dateprocess(data["weatherForecast"][i]["forecastDate"])[1])
  day = int(dateprocess(data["weatherForecast"][i]["forecastDate"])[2])

  print(f'{year} 年 {month} 月 {day} 日 ({datetime.date(year,month,day).strftime( "%A")[:3]})')
  print(f'風：{data["weatherForecast"][i]["forecastWind"]}')
  print(f'天氣：{data["weatherForecast"][i]["forecastWeather"]}')
  print(f'最高溫度：{data["weatherForecast"][i]["forecastMaxtemp"]["value"]}°C')
  print(f'最低溫度：{data["weatherForecast"][i]["forecastMintemp"]["value"]}°C')
  print(f'相對濕度：{data["weatherForecast"][i]["forecastMinrh"]["value"]}% - {data["weatherForecast"][i]["forecastMaxrh"]["value"]}% ')
  print("-"*20,"\n")
