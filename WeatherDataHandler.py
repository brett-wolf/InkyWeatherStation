import requests, json, datetime, math
from datetime import datetime


class WeatherData:
    def __init__(
        self,
        dt,
        sunrise,
        sunset,
        moon_phase,
        min,
        max,
        day,
        morn,
        eve,
        night,
        humidity,
        humidity_icon,
        weatherid,
        description,
        pop,
        precipitation_icon,
        uvi,
        uv_icon,
        day_of_week,
        wind_speed,
        wind_icon,
        cloud_percent,
        cloud_icon,
        degree_icon
    ):
        self.datetime = dt
        self.sunrise = sunrise
        self.sunset = sunset
        self.moon_phase = moon_phase
        self.min_temp = min
        self.max_temp = max
        self.temp = day
        self.morning_temp = morn
        self.evening_temp = eve
        self.night_temp = night
        self.humidity = humidity
        self.humidity_icon = humidity_icon
        self.weather_icon = weatherid
        self.weather_description = description
        self.precipitation_chance = pop
        self.precipitation_icon = precipitation_icon
        self.uv_index = uvi
        self.uv_icon = uv_icon
        self.day_of_week = day_of_week
        self.wind_speed = wind_speed
        self.wind_icon = wind_icon
        self.cloud_percent = cloud_percent
        self.cloud_icon = cloud_icon
        self.degree_icon = degree_icon

class WeatherDataHandler(object):

    def __init__(self, weather_data_json):
        self.weather_data_json = weather_data_json
        self.weather_data = None
        self.get_weather_data()

    def _set_weather_icon(self, weatherID):
        weatherMap = {
            200: ("\uf01e", "\uf01e"),  # thunderstorm
            201: ("\uf01e", "\uf01e"),  # thunderstorm
            202: ("\uf01e", "\uf01e"),  # thunderstorm
            210: ("\uf016", "\uf016"),  # lightning
            211: ("\uf016", "\uf016"),  # lightning
            212: ("\uf016", "\uf016"),  # lightning
            221: ("\uf016", "\uf016"),  # lightning
            230: ("\uf01e", "\uf01e"),  # thunderstorm
            231: ("\uf01e", "\uf01e"),  # thunderstorm
            232: ("\uf01e", "\uf01e"),  # thunderstorm
            300: ("\uf01c", "\uf01c"),  # sprinkle
            301: ("\uf01c", "\uf01c"),  # sprinkle
            302: ("\uf019", "\uf019"),  # rain
            310: ("\uf017", "\uf017"),  # rain-mix
            311: ("\uf019", "\uf019"),  # rain
            312: ("\uf019", "\uf019"),  # rain
            313: ("\uf01a", "\uf01a"),  # showers
            314: ("\uf019", "\uf019"),  # rain
            321: ("\uf01c", "\uf01c"),  # sprinkle
            500: ("\uf019", "\uf019"),  # light rain
            501: ("\uf019", "\uf019"),  # moderate rain
            502: ("\uf015", "\uf015"),  # heavy intense rain
            503: ("\uf018", "\uf018"),  # very heavy rain
            504: ("\uf018", "\uf018"),  # extreme rain
            511: ("\uf017", "\uf017"),  # freezing rain
            520: ("\uf01c", "\uf01c"),  # light intensity showers
            521: ("\uf01a", "\uf01a"),  # rain showers
            522: ("\uf015", "\uf015"),  # heavy rain showers
            531: ("\uf01d", "\uf01d"),  # storm-showers
            600: ("\uf01b", "\uf01b"),  # light snow
            601: ("\uf01b", "\uf01b"),  # snow
            602: ("\uf064", "\uf064"),  # heavy snow
            611: ("\uf0b5", "\uf0b5"),  # sleet
            612: ("\uf017", "\uf017"),  # light shower sleet
            615: ("\uf017", "\uf017"),  # light rain and snow
            616: ("\uf017", "\uf017"),  # rain and snow
            620: ("\uf01b", "\uf01b"),  # light shower snow
            621: ("\uf01b", "\uf01b"),  # shower snow
            622: ("\uf064", "\uf064"),  # heavy shower snow
            701: ("\uf014", "\uf014"),  # mist
            711: ("\uf062", "\uf062"),  # smoke
            721: ("\uf063", "\uf063"),  # haze
            731: ("\uf063", "\uf063"),  # dust
            741: ("\uf021", "\uf021"),  # fog
            751: ("\uf063", "\uf063"),  # sand
            761: ("\uf063", "\uf063"),  # dust
            762: ("\uf063", "\uf063"),  # dust
            771: ("\uf014", "\uf014"),  # squalls
            781: ("\uf056", "\uf056"),  # tornado
            800: ("\uf00d", "\uf077"),  # sunny !  alternative: f02e: moon, f077: stars
            801: ("\uf041", "\uf041"),  # cloud
            802: ("\uf00c", "\uf083"),  # clouds  25-50% !
            803: ("\uf002", "\uf031"),  # clouds  51-84% !
            804: ("\uf013", "\uf013"),  # clouds  85-100%
            900: ("\uf056", "\uf056"),  # tornado
            901: ("\uf01d", "\uf01d"),  # storm-showers
            902: ("\uf073", "\uf073"),  # hurricane
            903: ("\uf076", "\uf076"),  # snowflake-cold
            904: ("\uf055", "\uf055"),  # hot
            905: ("\uf011", "\uf011"),  # windy
            906: ("\uf015", "\uf015"),  # hail
            957: ("\uf050" "\uf050"),  # strong-wind
        }


        if weatherID in weatherMap:
            return weatherMap[weatherID]
        # TODO: If not - return some default

    def _set_moon_icon(self, moon_percent):
        if moon_percent == 0 or moon_percent == 1:        #0 = New Moon
          return "\uf0eb"
        
        elif moon_percent > 0 and moon_percent < 0.05:    #0 - 0.24 = Waxing cresent
          return "\uf0d0"
        elif moon_percent >= 0.05 and moon_percent < 0.1:
          return "\uf0d2"
        elif moon_percent >= 0.1 and moon_percent < 0.15:
          return "\uf0d3"
        elif moon_percent >= 0.15 and moon_percent < 0.2:
          return "\uf0d4"
        elif moon_percent >= 0.2 and moon_percent < 0.25:
          return "\uf0d5"

        elif moon_percent == 0.25:                        #0.25 = First quarter moon (half moon)
          return "\uf0d6"
        
        elif moon_percent > 0.25 and moon_percent < 0.3:  #0.26 - 0.5 = Waxing gibbous
          return "\uf0d7"
        elif moon_percent >= 0.3 and moon_percent < 0.35:
          return "\uf0d8"
        elif moon_percent >= 0.35 and moon_percent < 0.4:
          return "\uf0d9"
        elif moon_percent >= 0.4 and moon_percent < 0.45:
          return "\uf0da"
        elif moon_percent >= 0.45 and moon_percent < 0.5:
          return "\uf0db"

        elif moon_percent == 0.5:                         #0.5 = Full Moon
          return "\uf0dd"
        
        elif moon_percent > 0.5 and moon_percent <= 0.55: #0.6 - 0.74 = Waning gibbous
          return "\uf0de"
        elif moon_percent >= 0.55 and moon_percent < 0.6:
          return "\uf0df"
        elif moon_percent >= 0.6 and moon_percent < 0.65:
          return "\uf0e1"
        elif moon_percent >= 0.65 and moon_percent < 0.7:
          return "\uf0e2"
        elif moon_percent >= 0.7 and moon_percent < 0.75:
          return "\uf0e3"

        elif moon_percent == 0.75:                        #0.75 = Last/Third quarter moon
          return "\uf0e4"

        elif moon_percent > 0.75 and moon_percent < 0.8:    #0.76 - 0.99 = Waning cresent
          return "\uf0e6"
        elif moon_percent >= 0.8 and moon_percent < 0.85:
          return "\uf0e7"
        elif moon_percent >= 0.85 and moon_percent < 0.9:
          return "\uf0e8"
        elif moon_percent >= 0.9 and moon_percent < 0.95:
          return "\uf0e9"
        elif moon_percent >= 0.95 and moon_percent < 1:
          return "\uf0ea"

        else:
          return "\uf070"

    def _date_ordinal(self, n):
      return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))

    def _parse_data(self, jsonobject):
        return_class = []
        days_count = 0
        for daydata in jsonobject["daily"]:
            if days_count == 5: #stop when we have 5 days of weather
              break
            day = int(datetime.fromtimestamp(daydata["dt"]).strftime("%-d"))
            date_ord = self._date_ordinal(day)
            day_of_the_week = "{} {}".format(datetime.fromtimestamp(daydata["dt"]).strftime("%a"), date_ord)
            moon_icon = self._set_moon_icon(daydata["moon_phase"])
            weather_icon_array = self._set_weather_icon(daydata["weather"][0]["id"])
            humidity_icon = "\uf07a"
            precipitation_percentage_icon = "\uf078"
            uv_icon = "\uf052"
            wind_icon = "\uf0cc"
            cloud_icon = "\uf083" #cloud with sun
            degree_icon = "\uf042"
            weather_icon = weather_icon_array[0]  
            precipitation = str(int(daydata["pop"] * 100))
            wind_speed = str(int(daydata["wind_speed"]))

            if (
                datetime.now() > datetime.fromtimestamp(daydata["sunrise"])
                and datetime.now() > datetime.fromtimestamp(daydata["sunset"])
            ):

                weather_icon = weather_icon_array[1]
                cloud_icon = "\uf081" #cloud with moon

            return_class.append(
                WeatherData(
                    daydata["dt"],
                    str(datetime.fromtimestamp(daydata["sunrise"]).strftime("%H:%M")),
                    str(datetime.fromtimestamp(daydata["sunset"]).strftime("%H:%M")),
                    moon_icon,
                    str(int(math.ceil(daydata["temp"]["min"]))),
                    str(int(math.ceil(daydata["temp"]["max"]))),
                    str(int(math.ceil(daydata["temp"]["day"]))),
                    str(int(math.ceil(daydata["temp"]["morn"]))),
                    str(int(math.ceil(daydata["temp"]["eve"]))),
                    str(int(math.ceil(daydata["temp"]["night"]))),
                    daydata["humidity"],
                    humidity_icon,
                    weather_icon,
                    daydata["weather"][0]["description"],
                    precipitation + "%",
                    precipitation_percentage_icon,
                    daydata["uvi"],
                    uv_icon,
                    day_of_the_week,
                    wind_speed,
                    wind_icon,
                    daydata["clouds"],
                    cloud_icon,
                    degree_icon
                )
            )
            days_count += 1

        return return_class

    def get_weather_data(self):
        print("In get_weather_data function")

        self.weather_data = self._parse_data(self.weather_data_json)
