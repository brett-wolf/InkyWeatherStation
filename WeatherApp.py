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
from GoogleCalendarData import GoogleCalendarData
config = ConfigHandler()

def getsize(font, text):
    _, _, right, bottom = font.getbbox(text)
    return (right, bottom)

def main():

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
    weather_icons_font = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/weathericons-regular-webfont.ttf", 46)
    weather_icons_font_small = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/weathericons-regular-webfont.ttf", 20)
    source_code_pro_font_small = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/SourceCodePro.ttf", 10)
    source_code_pro_font = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/SourceCodePro.ttf", 15)
    source_code_pro_bold_font = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/SourceCodePro-Bold.ttf", 17)
    source_code_pro_bold_font_large = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/SourceCodePro-Bold.ttf", 35)

    roboto_condensed_light = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/RobotoCondensed-Light.ttf", 15)
    roboto_condensed_medium = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/RobotoCondensed-Medium.ttf", 15)
    roboto_condensed_bold = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/RobotoCondensed-Bold.ttf", 15)
    roboto_condensed_semibold = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/RobotoCondensed-SemiBold.ttf", 15)
    roboto_condensed_regular = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/RobotoCondensed-Regular.ttf", 15)
    roboto_condensed_bold_large = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/RobotoCondensed-Bold.ttf", 35)
    # Get data from weather provider
    try:
        print("Calling weather data function")
        print(config.latitude)
        print(config.weather_url)
        data = WeatherData(config.latitude, config.longitude, config.api_key, config.weather_url)
        data.getWeatherData()

    except Exception as exc:
        LoggingHandler.handle_exception("Error in calling the weather API", exc)
    
    #Get Data from ToDo provider
    try:
        print("calling todo data function")
        tododata = ToDoData(config.todoist_key, config.todoist_project)
        tododata.GetTodoList()
        #print(tododata.todolist.tasks)
    except Exception as exc:
        LoggingHandler.handle_exception("Error in calling the todo API", exc) 

    #Get Data from google calendar provider
    try:
        print("Calling google calendar data function")
        calendardata = GoogleCalendarData()
        calendardata.GetCalendarData()
    except Exception as exc:
        LoggingHandler.handle_exception("Error in calling the google calendar API", exc)

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
    canvas.text((5, 130), current_sunrise, inky_display.BLACK, font=roboto_condensed_light)    
    canvas.text((60, 130), current_sunset, inky_display.BLACK, font=roboto_condensed_light)

    #Current weather temp and description
    #canvas.text((10, 80), current_description, inky_display.BLACK, font=source_code_pro_bold_font)
    canvas.text((10, 80), str(data.currentweather.dateTime.strftime('%A %d %b')).lower(), inky_display.BLACK, font=roboto_condensed_bold)
    #TODO If the current temp is >= 100 then make the text smaller and re-align to the left a bit
    canvas.text((100, 17), current_temp, inky_display.BLACK, font=roboto_condensed_bold_large)
    canvas.text((95, 55), current_min_temp, inky_display.BLACK, font=roboto_condensed_light)
    canvas.text((124, 55), current_max_temp, inky_display.BLACK, font=roboto_condensed_light)

    #canvas.text((10, 150), "feels like:", inky_display.BLACK, font=source_code_pro_font)
    #canvas.text((110, 158), current_feels, inky_display.BLACK, font=source_code_pro_bold_font)

    #canvas.line([(0,120),(0,120)], fill=inky_display.BLACK,width=5, joint="curve")
    #corners=(top_left, top_right, bottom_right, bottom_left)

    
    #10, 80, 80, 140
    #(Left starting point of circle, top point of the arc, Right end of arc, bottom line of arc)
    canvas.arc((85, 8, 150, 70), start=140, end=40, fill=inky_display.BLACK, width=4)

    #canvas.ellipse((85, 8, 150, 70), fill=inky_display.RED, width=4)

    #canvas.rectangle([(0,120),(120,0)], fill=inky_display.WHITE, outline=inky_display.BLACK, width=3)

    #Add the TODO list data to canvas
    canvas.text((12, 150), "todo:", inky_display.BLACK, font=roboto_condensed_bold)
    todoline = 170
    right_todo_line = 170
    tododotleft = 176
    tododotright = 181
    todo_text_left = 15
    todo_dot_left = 5

    task_count = 0
    for task in tododata.todolist.tasks:
        if task_count > 5:
            todo_text_left = 170
            todo_dot_left = 165
        
        if task_count == 6:
            todoline = right_todo_line
        
        #canvas.ellipse((todo_dot_left, tododotleft, 10, tododotright), fill=inky_display.BLACK, width=4)
        canvas.text((todo_text_left, todoline), task, inky_display.BLACK, font=roboto_condensed_light)
        todoline += 20
        tododotleft += 20
        tododotright += 20
        task_count += 1
        if task_count > 6:
            right_todo_line += 20
        
    #Add the calendar data to canvas
    calendarline = 170
    for event in calendardata.eventlist.events:
        #canvas.text((180, calendarline), event.summary, inky_display.BLACK, font=source_code_pro_font)
        #TODO Maybe draw box around the calendar events with the time/date at the top and multiline text below
        #limit the number or boxes we can show depending on how many boxes we can fit
        

        #canvas.multiline_text((180, calendarline), event.summary, inky_display.BLACK, font=roboto_condensed_light, spacing=10)
        calendarline += 20
        #print(event.summary)
        #print(event.date)
        #print(event.time)

    #Update the Inky display with canvas data
    inky_display.set_image(img)
    inky_display.show()

    #Write date and time to log file to signify last run
    LoggingHandler.log_run_complete()


if __name__ == "__main__":
  main()