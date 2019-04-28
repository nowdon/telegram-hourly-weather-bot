import telegram
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Read config file
with open('config.json') as f:
    conf = json.load(f)

bot = telegram.Bot(token=conf["bot_token"])

# HTTP request
r = requests.get(conf["url"])

# parse html
bs_obj = BeautifulSoup(r.content, "html.parser")
# find todays hourly forecast
today = bs_obj.find(class_="forecast-point-1h")
hourly_weathers = today.find(class_="weather")

# get current hour
current_hour = datetime.now().hour
i = 1
for weather in hourly_weathers.select('p'):
    if i == current_hour + 1:
        mes = '1時間後の天気は ' + weather.string + ' だぞ\n' + conf["url"]
#        if '雨' in weather.string:
#           mes = 'そろそろ雨が降るかもしれないぞ\n' + conf["url"]
        bot.send_message(chat_id=conf["chat_id"], text=mes)
    i += 1
