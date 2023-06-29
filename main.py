import json
import requests
import datetime
import sys

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

  year = int(dateprocess(data["weatherForecast"][date]["forecastDate"])[0])
  month = int(dateprocess(data["weatherForecast"][date]["forecastDate"])[1])
  day = int(dateprocess(data["weatherForecast"][date]["forecastDate"])[2])

  print(f'{year} 年 {month} 月 {day} 日 ({datetime.date(year,month,day).strftime( "%A")[:3]})')
  print(f'風：{data["weatherForecast"][date]["forecastWind"]}')
  print(f'天氣：{data["weatherForecast"][date]["forecastWeather"]}')
  print(f'最高溫度：{data["weatherForecast"][date]["forecastMaxtemp"]["value"]}°C')
  print(f'最低溫度：{data["weatherForecast"][date]["forecastMintemp"]["value"]}°C')
  print(f'相對濕度：{data["weatherForecast"][date]["forecastMinrh"]["value"]}% - {data["weatherForecast"][date]["forecastMaxrh"]["value"]}% ')
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
