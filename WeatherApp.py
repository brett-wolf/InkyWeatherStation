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
from ToDoData import ToDoData
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
    
    # Set scaling for display size
    scale_size = 2.20
    padding = 15

    # Load the fonts
    hanken_bold_font = ImageFont.truetype(HankenGroteskBold, int(10 * scale_size))
    weather_icons_font = ImageFont.truetype("./fonts/weathericons-regular-webfont.ttf", 46)
    weather_icons_font_small = ImageFont.truetype("./fonts/weathericons-regular-webfont.ttf", 20)
    source_code_pro_font = ImageFont.truetype("./fonts/SourceCodePro.ttf", 15)
    source_code_pro_bold_font = ImageFont.truetype("./fonts/SourceCodePro-Bold.ttf", 17)
    source_code_pro_bold_font_large = ImageFont.truetype("./fonts/SourceCodePro-Bold.ttf", 35)

    # Get data from weather provider
    try:
        print("Calling weather data function")
        print(config.latitude)
        print(config.weather_url)
        data = WeatherData(config.latitude, config.longitude, config.api_key, config.weather_url)
        data.getWeatherData()

    except Exception as exc:
        LoggingHandler.handle_exception("Error in calling the weather API", exc)
    
    try:
        print("calling todo api")
        tododata = ToDoData(config.todoist_key, config.todoist_project)
        tododata.GetTodoList()
        print(tododata.todolist.tasks)
    except Exception as exc:
        LoggingHandler.handle_exception("Error in calling the todo API", exc) 

    #TODO Check if we have weather and TODO data. If not, no need to update the screen
    #Eventually we want to store the data locally, and reload it with an error picture somewhere on screen so I know it didnt update

    # Create a new canvas to draw on
    img = Image.new("P", inky_display.resolution)
    canvas = ImageDraw.Draw(img)
    canvas_height = inky_display.height #300
    canvas_width = inky_display.width #400

    try:
        inky_display.set_border(inky_display.BLACK)
    except NotImplementedError:
        pass

    #Draw out the boxes on screen
    canvas.line([(0,canvas_height / 2),(canvas_width,canvas_height / 2)], fill=inky_display.BLACK,width=3)
    canvas.line([(canvas_width / 2.5,0),(canvas_width / 2.5,canvas_height / 2)], fill=inky_display.BLACK,width=3)
    canvas.line([(canvas_width / 1.43,0),(canvas_width /1.43,canvas_height / 2)], fill=inky_display.BLACK,width=2)
    canvas.line([(canvas_width / 2.5,canvas_height/4),(canvas_width,canvas_height / 4)], fill=inky_display.BLACK,width=2)

    canvas.line([(55, canvas_height / 2),(55,canvas_height / 2.25)], fill=inky_display.BLACK,width=1)

    #canvas.rounded_rectangle((0, 0, 160, 150), 
    #                    fill=None, 
    #                    outline=inky_display.BLACK, 
    #                    width=3, 
    #                    radius=7, 
    #                    corners=(False,False,True,False))

    #TODO: After midnight, it goes to the next day. Making the sun show instead of stars after midnight
    # Set the message. If its night time, take the second icon, which is for night
    current_icon = data.currentweather.icon[0]
    if data.currentweather.dateTime > data.currentweather.sunrise and data.currentweather.dateTime > data.currentweather.sunset:
        current_icon = data.currentweather.icon[1]

    current_description = data.currentweather.description
    current_temp = str(data.currentweather.temp) #TODO make a string in handler
    current_max_temp = str(data.currentweather.max) #TODO make a string in handler
    current_min_temp = str(data.currentweather.min) #TODO make a string in handler
    current_feels = str(data.currentweather.tempfeels) #TODO make a string in handler
    current_sunrise = str(data.currentweather.sunrise.time())[0:5]
    current_sunset = str(data.currentweather.sunset.time())[0:5]    


    #TODO If its sunny, show data like Humidity. Wind Speed.
    #If its rainy, show % chance of rain. Cloud coverage etc. 
    #Put this logic in its own method

    #Current weather icon
    canvas.text((10, 5), current_icon, inky_display.BLACK, font=weather_icons_font)

    #Sunrise / Sunset display
    canvas.text((18, 108), "\uf046", inky_display.BLACK, font=weather_icons_font_small)
    canvas.text((73, 108), "\uf047", inky_display.BLACK, font=weather_icons_font_small)
    canvas.text((5, 130), current_sunrise, inky_display.BLACK, font=source_code_pro_font)    
    canvas.text((60, 130), current_sunset, inky_display.BLACK, font=source_code_pro_font)

    #Current weather temp and description
    #canvas.text((10, 80), current_description, inky_display.BLACK, font=source_code_pro_bold_font)
    canvas.text((10, 80), str(data.currentweather.dateTime.strftime('%A %d %b')).lower(), inky_display.BLACK, font=source_code_pro_bold_font)
    #canvas.text((10, 130), "temp:", inky_display.BLACK, font=source_code_pro_font)
    canvas.text((97, 18), current_temp, inky_display.BLACK, font=source_code_pro_bold_font_large)
    canvas.text((95, 55), current_min_temp, inky_display.BLACK, font=source_code_pro_font)
    canvas.text((122, 55), current_max_temp, inky_display.BLACK, font=source_code_pro_font)

    #canvas.text((10, 150), "feels like:", inky_display.BLACK, font=source_code_pro_font)
    #canvas.text((110, 158), current_feels, inky_display.BLACK, font=source_code_pro_bold_font)

    #canvas.line([(0,120),(0,120)], fill=inky_display.BLACK,width=5, joint="curve")
    #corners=(top_left, top_right, bottom_right, bottom_left)

    
    #10, 80, 80, 140
    #(Left starting point of circle, top point of the arc, Right end of arc, bottom line of arc)
    canvas.arc((85, 8, 150, 70), start=140, end=40, fill=inky_display.BLACK, width=4)

    #canvas.ellipse((85, 8, 150, 70), fill=inky_display.RED, width=4)

    #canvas.rectangle([(0,120),(120,0)], fill=inky_display.WHITE, outline=inky_display.BLACK, width=3)

    #TODO: High, trying a loop for tasks
    todoline = 180
    for task in tododata.todolist:
        print(task)
        canvas.text((15, todoline), task, inky_display.BLACK, font=source_code_pro_font)
        todoline + 20

    inky_display.set_image(img)

    #inky_display.getModified()
    inky_display.show()


    exit()