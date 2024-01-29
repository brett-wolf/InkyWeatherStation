import requests, json, datetime

class Values(object):
  pass

class WeatherData(object):
    URL = "https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid={2}&units=imperial"
    #LAT HOME : 37.55589989488259
    #LON HOME : -77.4800165092538
    #API KEY  : 6284869d5895baaf5f2537c1e6872fb0
    
    def __init__(self,latitude,longitude,apikey):
        self._latitude = latitude
        self._longitude = longitude
        self._apikey = apikey

    
    def getWeatherData(self):
        url = WeatherData.URL.format(self._latitude, self._longitude, self._apikey)

        response = requests.get(url)
        data = json.loads(response.text)
        response.close()
