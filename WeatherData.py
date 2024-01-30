import requests, json, datetime

class Values(object):
  pass

class WeatherData(object):
    URL = "https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid={2}&units=imperial"
    
    def __init__(self,latitude,longitude,apikey):
        self._latitude = latitude
        self._longitude = longitude
        self._apikey = apikey
        self.currentweather = None

    def _parse_data(self,jsonobject):
      val = Values()
      val.dateTime = datetime.datetime.fromtimestamp(jsonobject["dt"])
      val.temp = jsonobject["main"]["temp"]
      val.tempfeels = jsonobject["main"]["feels_like"]
      val.description = jsonobject["weather"][0]["description"]
      val.icon = jsonobject["weather"][0]["icon"]
      val.humidity = jsonobject["main"]["humidity"]
      val.windspeed = jsonobject["wind"]["speed"]
      val.sunrise = datetime.datetime.fromtimestamp(jsonobject["sys"]["sunrise"])
      val.sunset = datetime.datetime.fromtimestamp(jsonobject["sys"]["sunset"])

      return val 
    
    def getWeatherData(self):
        print("In weather data function")
        url = WeatherData.URL.format(self._latitude, self._longitude, self._apikey)
        response = requests.get(url)
        data = json.loads(response.text)
        response.close()

        #print(data["weather"][0]["description"])
        #print(data["main"]["temp"])

        self.currentweather = self._parse_data(data)



