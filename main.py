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

def get_data(datatype):
  res = requests.get(f"https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType={datatype}&lang=tc")
  data=json.loads(res.text)
  return data

def dateprocess(str,dash=False):
  if dash == False:
    year = str[0:4]
    month = str[4:6]
    day = str[6:9]
    time = 0

  elif dash == True:
    year = str[0:4]
    month = str[5:7]
    day = str[8:10]
    time = str[11:16]
  
  return year,month,day,time

def weather_report_info():
  data = get_data("rhrread")
  print(data)
  start_time = dateprocess(data["rainfall"]["startTime"],True)
  end_time = dateprocess(data["rainfall"]["endTime"],True)

  # 特別天氣提示
  if data["specialWxTips"] != "":
    for i in range(len(data["specialWxTips"])):
      print(f'特別天氣提示：{data["specialWxTips"][i]}\n')
  
  # 熱帶氣旋位置
  if data["tcmessage"] != "":
    for i in range(len(data["tcmessage"])):
      print(f'熱帶氣旋位置:{data["tcmessage"][i]}\n')


  # 溫度
  print("溫度：")
  for i in range(26):
    print(f'\t{data["temperature"]["data"][i]["place"]}：{data["temperature"]["data"][i]["value"]}°C')

  print("-"*20,"\n")

  # 濕度
  print(f'濕度：{data["humidity"]["data"][0]["value"]}%\n')

  # 雨量
  if start_time[2] == dateprocess(str(datetime.date.today()),True)[2]: # 判斷是否同一天
    print(f"雨量（時間：{start_time[3]} - {end_time[3]}）：")
  
  elif start_time[1] == dateprocess(str(datetime.date.today()),True)[1]: # 判斷是否同一月
    print(f"雨量（時間：{start_time[2]} 日 {start_time[3]} - {end_time[2]} 日 {end_time[3]}）：")

  elif start_time[0] == dateprocess(str(datetime.date.today()),True)[0]: # 判斷是否同一年
    print(f"雨量（時間：{start_time[1]} 月 {start_time[2]} 日 {start_time[3]} - {end_time[1]} 月 {end_time[2]} 日 {end_time[3]}）：")

  else: # 跨年
    print(f"雨量（時間：{start_time[1]} 年 {start_time[1]} 月 {start_time[2]} 日 {start_time[3]} - {end_time[1]} 年 {end_time[1]} 月 {end_time[2]} 日 {end_time[3]}）：")

  for k in range(0,18):
      if data["rainfall"]["data"][k]["main"] == "FALSE" and data["rainfall"]["data"][k]["max"] != 0 :
        print(f'\t{data["rainfall"]["data"][k]["place"]}：{data["rainfall"]["data"][k]["min"]}mm - {data["rainfall"]["data"][k]["max"]}mm')
      else:
        print(f'\t{data["rainfall"]["data"][k]["place"]}：無雨')
  print("-"*20,"\n")


  # 警告信息
  if data["warningMessage"] != "": # 判斷是否爲空字串
    for i in range(len(data["warningMessage"])):
      print(f'警告信息：{data["warningMessage"][i]}')
    print()





  #for i in ("warningMessage","icon","iconUpdateTime","lightning","uvindex","temperature","tcmessage","mintempFrom00To09","rainfallFrom00To12","rainfallLastMonth","rainfallJanuaryToLastMonth","humidity","updateTime"):
    
    
  update_time = dateprocess(data["updateTime"],True)
  print(f"更新時間：{update_time[0]} 年 {update_time[1]} 月 {update_time[2]} 日 {update_time[3]}")




def weather_forecast_info(date,full=0):
  data = get_data("fnd")

  if full == 0:
    print("天氣概況：",data['generalSituation'],"\n")

  weather_forecast = data["weatherForecast"][date]
  
  # 轉換時間戳
  year = int(dateprocess(weather_forecast["forecastDate"])[0])
  month = int(dateprocess(weather_forecast["forecastDate"])[1])
  day = int(dateprocess(weather_forecast["forecastDate"])[2])
  
  
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
    weather_forecast_info(i,i)

# while True:
#   print("""
#   [0]: 退出程序;\n
#   [1]: 獲取 9 天全部天氣預報；\n
#   [2]: 獲取九天内指定日期的天氣預報；\n
#   提示：只需輸入數字部分。
#   """)
#   try:
#     command = int(input("指令："))

#   except:
#     continue
#   print()
  

#   if command == 0:
#     sys.exit()
#   elif command == 1:
#     all_info()
#   elif command == 2:
#     try:
#       date = int(input("第幾天："))

#       while date <= 0 or date > 9:
#         print("請輸入 1-9\n")
#         date = int(input("第幾天："))

#     except:
#       print("請輸入 1-9\n")
#       continue

#     weather_forecast_info(date-1)

  
#   else:
#     print("請按指令輸入。")
#     continue

weather_report_info()
