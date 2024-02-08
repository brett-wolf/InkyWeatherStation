from time import strftime
from datetime import datetime
import pytz
from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from WeatherData import WeatherData
from LoggingHandler import LoggingHandler
from ConfigHandler import ConfigHandler
config = ConfigHandler()

class WeatherApp:

    def getsize(font, text):
        _, _, right, bottom = font.getbbox(text)
        return (right, bottom)

    try:
        inky_display = auto(ask_user=True, verbose=True)
    except TypeError:
        logging.error("Inky display not found")
        raise TypeError("You need to update the Inky library to >= v1.1.0")
    
    #try:
    #    inky_display.set_border(inky_display.BLACK)
    #except NotImplementedError:
    #    pass

    # Set scaling for display size
    scale_size = 2.20
    padding = 15

    # Load the fonts
    hanken_bold_font = ImageFont.truetype(HankenGroteskBold, int(10 * scale_size))
    weather_icons_font = ImageFont.truetype("./fonts/weathericons-regular-webfont.ttf", 46)
    weather_icons_font_small = ImageFont.truetype("./fonts/weathericons-regular-webfont.ttf", 20)
    source_code_pro_font = ImageFont.truetype("./fonts/SourceCodePro.ttf", 15)
    source_code_pro_bold_font = ImageFont.truetype("./fonts/SourceCodePro-Bold.ttf", 17)

    # Get data from weather provider
    try:
        print("Calling weather data function")
        print(config.latitude)
        print(config.weather_url)
        data = WeatherData(config.latitude, config.longitude, config.api_key, config.weather_url)
        data.getWeatherData()

    except Exception as exc:
        LoggingHandler.handle_exception("Error in calling the weather API", exc)

    #TODO: After midnight, it goes to the next day. Making the sun show instead of stars after midnight
    # Set the message. If its night time, take the second icon, which is for night
    current_icon = data.currentweather.icon[0]
    if data.currentweather.dateTime > data.currentweather.sunrise and data.currentweather.dateTime > data.currentweather.sunset:
        current_icon = data.currentweather.icon[1]
    
    print("sunrise:" + str(data.currentweather.sunrise))
    print("sunset:" + str(data.currentweather.sunset))
    print("time:" + str(data.currentweather.dateTime))

    print("HourMinute:" + str(data.currentweather.dateTime.time())[0:5])

    current_description = data.currentweather.description
    current_temp = str(data.currentweather.temp) #TODO make a string in handler
    current_feels = str(data.currentweather.tempfeels) #TODO make a string in handler
    current_sunrise = str(data.currentweather.sunrise.time())[0:5]
    current_sunset = str(data.currentweather.sunset.time())[0:5]
    
    # Create a new canvas to draw on
    img = Image.new("P", inky_display.resolution)
    canvas = ImageDraw.Draw(img)

    #TODO If its sunny, show data like Humidity. Wind Speed.
    #If its rainy, show % chance of rain. Cloud coverage etc. 
    #Put this logic in its own method

    #Current weather icon
    canvas.text((10, 5), current_icon, inky_display.BLACK, font=weather_icons_font)

    #Sunrise / Sunset display
    canvas.text((82, 8), "\uf046", inky_display.BLACK, font=weather_icons_font_small)
    canvas.text((82, 30), "\uf047", inky_display.BLACK, font=weather_icons_font_small)
    canvas.text((108, 15), current_sunrise, inky_display.BLACK, font=source_code_pro_font)    
    canvas.text((108, 34), current_sunset, inky_display.BLACK, font=source_code_pro_font)

    #Current weather temp and description
    canvas.text((10, 60), current_description, inky_display.BLACK, font=source_code_pro_bold_font)
    canvas.text((10, 80), "temp:", inky_display.BLACK, font=source_code_pro_font)
    canvas.text((60, 78), current_temp, inky_display.BLACK, font=source_code_pro_bold_font)

    canvas.text((10, 100), "feels like:", inky_display.BLACK, font=source_code_pro_font)
    canvas.text((110, 98), current_feels, inky_display.BLACK, font=source_code_pro_bold_font)

    #canvas.line([(0,120),(0,120)], fill=inky_display.BLACK,width=5, joint="curve")
    #corners=(top_left, top_right, bottom_right, bottom_left)
    canvas.rounded_rectangle((0, 0, 160, 130), 
                            fill=None, 
                            outline=inky_display.BLACK, 
                            width=3, 
                            radius=7, 
                            corners=(False,False,True,False))
    
    #canvas.rounded_rectangle((130, 150, 210, 210), 
    #                        fill=None, 
    #                        outline=inky_display.BLACK, 
    #                        width=3, 
    #                        radius=7, 
    #                        corners=(False,False,True,False))

    canvas.chord((130, 220, 210, 300), start=140, end=40, fill=inky_display.BLACK, width=6)

    #canvas.rectangle([(0,120),(120,0)], fill=inky_display.WHITE, outline=inky_display.BLACK, width=3)
    inky_display.set_image(img)

    #inky_display.getModified()
    inky_display.show()


    exit()