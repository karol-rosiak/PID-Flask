import sqlite3
import requests
def weatherCounter():
    conn = sqlite3.connect('baza.db')
    c = conn.cursor()
    tab = c.execute('SELECT * FROM lokalizacja ORDER BY rowid DESC LIMIT 1').fetchone()
    conn.close()
    lat = str(tab[0])
    lng = str(tab[1])
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=" + lat + "&lon=" + lng + "&exclude=current,minutely,hourly&lang=pl&appid=a874452b76f1cc6022316d344c4ac034"
    r = requests.get(url)
    daily = r.json()["daily"]
    counter = 0
    for weather in daily:
        if weather['weather'][0]['main']=="Rain":
            counter+=1

    return counter


print(weatherCounter())