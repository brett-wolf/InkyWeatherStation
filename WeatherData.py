import requests, json, datetime, math
from ConfigHandler import ConfigHandler
config = ConfigHandler()

class Values(object):
  pass

class WeatherData(object):
    #URL = "https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid={2}&units=imperial"
    
    def __init__(self,latitude,longitude,apikey,weatherurl):
        self._latitude = latitude
        self._longitude = longitude
        self._apikey = apikey
        self._weatherurl = weatherurl
        self.currentweather = None
    
    def _set_weather_icon(self, weatherID):
      weatherMap = {
        200: ("\uf01e","\uf01e"),   #thunderstorm
        201: ("\uf01e","\uf01e"),   #thunderstorm
        202: ("\uf01e","\uf01e"),   #thunderstorm
        210: ("\uf016","\uf016"),   #lightning
        211: ("\uf016","\uf016"),   #lightning
        212: ("\uf016","\uf016"),   #lightning
        221: ("\uf016","\uf016"),   #lightning
        230: ("\uf01e","\uf01e"),   #thunderstorm
        231: ("\uf01e","\uf01e"),   #thunderstorm
        232: ("\uf01e","\uf01e"),   #thunderstorm
        300: ("\uf01c","\uf01c"),   #sprinkle
        301: ("\uf01c","\uf01c"),   #sprinkle
        302: ("\uf019","\uf019"),   #rain
        310: ("\uf017","\uf017"),   #rain-mix
        311: ("\uf019","\uf019"),   #rain
        312: ("\uf019","\uf019"),   #rain
        313: ("\uf01a","\uf01a"),   #showers
        314: ("\uf019","\uf019"),   #rain
        321: ("\uf01c","\uf01c"),   #sprinkle
        500: ("\uf019","\uf019"),   #light rain
        501: ("\uf019","\uf019"),   #moderate rain
        502: ("\uf015","\uf015"),   #heavy intense rain
        503: ("\uf018","\uf018"),   #very heavy rain
        504: ("\uf018","\uf018"),   #extreme rain
        511: ("\uf017","\uf017"),   #freezing rain
        520: ("\uf01c","\uf01c"),   #light intensity showers
        521: ("\uf01a","\uf01a"),   #rain showers
        522: ("\uf015","\uf015"),   #heavy rain showers
        531: ("\uf01d","\uf01d"),   #storm-showers
        600: ("\uf01b","\uf01b"),   #light snow
        601: ("\uf01b","\uf01b"),   #snow
        602: ("\uf064","\uf064"),   #heavy snow
        611: ("\uf0b5","\uf0b5"),   #sleet
        612: ("\uf017","\uf017"),   #light shower sleet
        612: ("\uf017","\uf017"),   #shower sleet
        615: ("\uf017","\uf017"),   #light rain and snow
        616: ("\uf017","\uf017"),   #rain and snow
        620: ("\uf01b","\uf01b"),   #light shower snow
        621: ("\uf01b","\uf01b"),   #shower snow
        622: ("\uf064","\uf064"),   #heavy shower snow
        701: ("\uf014","\uf014"),   #mist
        711: ("\uf062","\uf062"),   #smoke
        721: ("\uf063","\uf063"),   #haze
        731: ("\uf063","\uf063"),   #dust
        741: ("\uf021","\uf021"),   #fog
        751: ("\uf063","\uf063"),   #sand
        761: ("\uf063","\uf063"),   #dust
        762: ("\uf063","\uf063"),   #dust
        771: ("\uf014","\uf014"),   #squalls
        781: ("\uf056","\uf056"),   #tornado
        800: ("\uf00d","\uf077"),   #sunny !  alternative: f02e: moon, f077: stars
        801: ("\uf041","\uf041"),   #cloud
        802: ("\uf00c","\uf083"),   #clouds  25-50% !
        803: ("\uf002","\uf031"),   #clouds  51-84% !
        804: ("\uf013","\uf013"),   #clouds  85-100%
        900: ("\uf056","\uf056"),   #tornado
        901: ("\uf01d","\uf01d"),   #storm-showers
        902: ("\uf073","\uf073"),   #hurricane
        903: ("\uf076","\uf076"),   #snowflake-cold
        904: ("\uf055","\uf055"),   #hot
        905: ("\uf011","\uf011"),   #windy
        906: ("\uf015","\uf015"),   #hail
        957: ("\uf050" "\uf050")    #strong-wind
      }

      if weatherID in weatherMap:
        return weatherMap[weatherID]
      #TODO: If not - return some default

    def _parse_data(self,jsonobject):
      val = Values()
      val.dateTime = datetime.datetime.fromtimestamp(jsonobject["dt"])
      val.temp = math.ceil(jsonobject["main"]["temp"])
      val.tempfeels = math.ceil(jsonobject["main"]["feels_like"])
      val.description = jsonobject["weather"][0]["description"]
      val.icon = self._set_weather_icon(jsonobject["weather"][0]["id"]) #TODO we cant assume this will have something?
      val.humidity = jsonobject["main"]["humidity"]
      val.windspeed = jsonobject["wind"]["speed"]
      val.sunrise = datetime.datetime.fromtimestamp(jsonobject["sys"]["sunrise"])
      val.sunset = datetime.datetime.fromtimestamp(jsonobject["sys"]["sunset"])

      return val 
    
    def getWeatherData(self):
        print("In weather data function")
        url = self._weatherurl.format(self._latitude, self._longitude, self._apikey)
        response = requests.get(url)
        data = json.loads(response.text)
        response.close()

        #print(data["weather"][0]["description"])
        #print(data["main"]["temp"])

        self.currentweather = self._parse_data(data)
    
    



