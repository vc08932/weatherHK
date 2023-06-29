import json
import requests
import datetime
import sys

forecast_icon = {
  "50":"陽光充沛",
  "51":"間有陽光",
  "52":"短暫陽光",
  "53":"間有陽光幾陣驟雨",
  "54":"短暫陽光有驟雨",
  "60":"多雲",
  "61":"密雲",
  "62":"微雨",
  "63":"雨",
  "64":"大雨",
  "65":"雷暴",
  "80":"大風",
  "81":"乾燥",
  "82":"潮濕",
  "83":"霧",
  "84":"薄霧",
  "85":"煙霞",
  "90":"熱",
  "91":"暖",
  "92":"涼",
  "93":"冷"
}

def get_data():
  res = requests.get("https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=tc")
  data=json.loads(res.text)
  return data

def dateprocess(str):
  year = str[0:4]
  month = str[4:6]
  day = str[6:9]
  return year,month,day

def weather_info(date,full=0):
  data = get_data()

  if full == 0:
    print("天氣概況：",data['generalSituation'],"\n")

  weather_forecast = data["weatherForecast"][date]

  year = int(dateprocess(weather_forecast["forecastDate"])[0])
  month = int(dateprocess(weather_forecast["forecastDate"])[1])
  day = int(dateprocess(weather_forecast["forecastDate"])[2])
  
  a=weather_forecast["ForecastIcon"]
  print(f'{year} 年 {month} 月 {day} 日 ({weather_forecast["week"]})')
  print(f'風：{weather_forecast["forecastWind"]}')
  print(f'天氣：{weather_forecast["forecastWeather"]}  ({forecast_icon[str(weather_forecast["ForecastIcon"])]})')
  print(f'最高溫度：{weather_forecast["forecastMaxtemp"]["value"]}°C')
  print(f'最低溫度：{weather_forecast["forecastMintemp"]["value"]}°C')
  print(f'相對濕度：{weather_forecast["forecastMinrh"]["value"]}% - {weather_forecast["forecastMaxrh"]["value"]}% ')
  print(f'降雨概率：{weather_forecast["PSR"]}')
  print("-"*20,"\n")

def all_info():
  for i in range(0,9):
    weather_info(i,i)

while True:
  print("""
  [0]: 退出程序;\n
  [1]: 獲取 9 天全部天氣預報；\n
  [2]: 獲取九天内指定日期的天氣預報；\n
  提示：只需輸入數字部分。
  """)
  try:
    command = int(input("指令："))

  except:
    continue
  print()
  

  if command == 0:
    sys.exit()
  elif command == 1:
    all_info()
  elif command == 2:
    try:
      date = int(input("第幾天："))

      while date <= 0 or date > 9:
        print("請輸入 1-9\n")
        date = int(input("第幾天："))

    except:
      print("請輸入 1-9\n")
      continue

    weather_info(date-1)

  else:
    print("請按指令輸入。")
    continue
