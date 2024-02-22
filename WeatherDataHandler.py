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
        weatherid,
        description,
        pop,
        uvi,
        day_of_week,
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
        self.weather_icon = weatherid
        self.weather_description = description
        self.precipitation_chance = pop
        self.uv_index = uvi
        self.day_of_week = day_of_week


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
        moon_map = {0: {"\XXXXXX"}, 20: {"\XXXXXX"}, 40: {"\XXXXXX"}, 100: {"\XXXXXX"}}
        if moon_percent in moon_map:
            return moon_map[moon_percent]

    def _parse_data(self, jsonobject):
        return_class = []

        for daydata in jsonobject["daily"]:
            day_of_the_week = datetime.fromtimestamp(daydata["dt"]).strftime("%A")
            weather_icon = self._set_weather_icon(daydata["weather"][0]["id"])[0]
            # current_icon = data.currentweather.icon[0]
            # if data.currentweather.dateTime > data.currentweather.sunrise and data.currentweather.dateTime > data.currentweather.sunset:
            #    current_icon = data.currentweather.icon[1]
            if (
                datetime.now() > daydata["sunrise"]
                and datetime.now() > daydata["sunset"]
            ):
                weather_icon = weather_icon[1]

            moon_icon = self._set_moon_icon(daydata["moon_phase"])

            return_class.append(
                WeatherData(
                    daydata["dt"],
                    daydata["sunrise"],
                    daydata["sunset"],
                    moon_icon,
                    daydata["temp"]["min"],
                    daydata["temp"]["max"],
                    daydata["temp"]["day"],
                    daydata["temp"]["morn"],
                    daydata["temp"]["eve"],
                    daydata["temp"]["night"],
                    daydata["humidity"],
                    weather_icon,
                    daydata["weather"][0]["description"],
                    daydata["pop"],
                    daydata["uvi"],
                    day_of_the_week,
                )
            )

        # val.dateTime = datetime.datetime.fromtimestamp(jsonobject["dt"])
        # val.temp = math.ceil(jsonobject["main"]["temp"])
        # val.min = math.ceil(jsonobject["main"]["temp_min"])
        # val.max = math.ceil(jsonobject["main"]["temp_max"])
        # val.tempfeels = math.ceil(jsonobject["main"]["feels_like"])
        # val.description = jsonobject["weather"][0]["description"]
        # val.icon = self._set_weather_icon(jsonobject["weather"][0]["id"]) #TODO we cant assume this will have something?
        # val.humidity = jsonobject["main"]["humidity"]
        # val.windspeed = jsonobject["wind"]["speed"]
        # val.sunrise = datetime.datetime.fromtimestamp(jsonobject["sys"]["sunrise"])
        # val.sunset = datetime.datetime.fromtimestamp(jsonobject["sys"]["sunset"])

        return return_class

    def get_weather_data(self):
        print("In get_weather_data function")
        self.weather_data = self._parse_data(self.weather_data_json)
