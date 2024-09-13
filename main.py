from time import sleep
import requests
import schedule
import os

# seting time
send_time = '07:00'

def send(msg):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + os.getenv("token")}
    payload = {'message': msg}
    requests.post(url, headers=headers, params=payload)

def main():
    send(f"{send_time}の時間の天気をお知らせするよ")
    new_get_weather()
    schedule.every().days.at(send_time).do(new_get_weather)
    while True:
        schedule.run_pending()
        sleep(1)

def new_get_weather():
    api = "http://api.openweathermap.org/data/2.5/weather"

    params = {
        'q': "地域名を入力", # 地域名
        'appid': "key", # APIキー
        'units': 'metric', # 温度単位（摂氏）
        'lang': 'ja' # 言語（日本語）
    }

    # APIリクエスト
    res = requests.get(api, params=params)

    # レスポンスが成功したか確認
    if res.status_code == 200:
        data = res.json()

        # 天気情報の抽出
        location_name = data['name']
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']

        msg =f"< {location_name}の天気予報 >\n\n> 天気\n・{weather_description}\n\n> 気温\n・{temperature}°C\n\n> 湿度\n・{humidity}%\n\n> 気圧\n・{pressure} hPa\n\n> 風速\n・{wind_speed} m/s"
        send(msg)
    else:
        print("天気情報を取得できませんでした。")

if __name__ == "__main__":
    main()