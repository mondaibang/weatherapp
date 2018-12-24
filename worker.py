import requests
import psycopg2
import psycopg2.extras
from datetime import datetime
import logging

#from pykeys import api_token
#from keys import db_password
#from keyword import api_token


def fetch_data():
    url = 'http://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=36f78c92ac189594799aaa1b22f0953d'
    data = requests.get(url).json()
    print(" print out: ",data['name'])

    location = data['name']
    weather = "Partly Cloudy"
    wind_str = 'speed: ' + str(data['wind']['speed'])
    temp = data['main']['temp']
    humidity = data['main']['humidity']
    precip = "0.00 in (0 mm)"
    icon_url = "http://icons-ak.wxug.com/i/c/k/partlycloudy.gif"
    observation_time = 'Last Updated on June 27, 5:27 PM PDT'
    #open db
    try:
        conn = psycopg2.connect(dbname='weather',user='postgres',host='localhost',password='123456')
        print('Opened DB successfully')
    except:
        print(datetime.now(), "Unable to connect to the database")
        logging.exception('Unable to open the database')
        return
    else:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # write to db
    cur.execute("""INSERT INTO station_reading(location,weather,wind_str,temp,humidity,precip,icon_url,observation_time)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s) """,(location, weather, wind_str,temp,humidity,precip,icon_url,observation_time))
    
    conn.commit()
    cur.close()
    conn.close()

    print('Data written', datetime.now())

fetch_data()
