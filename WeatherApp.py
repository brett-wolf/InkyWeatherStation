import requests, json
from time import strftime
from datetime import datetime
import pytz
from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw
from WeatherDataHandler import WeatherDataHandler
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
    except TypeError as exc:
        LoggingHandler.handle_exception("Inky display not found", exc)
        raise TypeError("You need to update the Inky library to >= v1.1.0")

    # Set display visibility
    current_weather_display = True
    tomorrow_weather_display = False
    todo_list_display = True
    calendar_events_display = False

    #TODO Change these font locations to a variable in config
    # Load the fonts
    weather_icons_font = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/weathericons-regular-webfont.ttf",40,)
    weather_icons_font_moon = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/weathericons-regular-webfont.ttf",46,)
    weather_icons_font_moon_small = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/weathericons-regular-webfont.ttf",30,)
    weather_icons_font_small = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/weathericons-regular-webfont.ttf",30,)
    weather_icons_font_smaller = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/weathericons-regular-webfont.ttf",20,)
    weather_icons_font_week_smaller = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/weathericons-regular-webfont.ttf",25,)
    source_code_pro_font_small = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/SourceCodePro.ttf", 10)
    source_code_pro_font = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/SourceCodePro.ttf", 15)
    source_code_pro_bold_font = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/SourceCodePro-Bold.ttf", 17)
    source_code_pro_bold_font_large = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/SourceCodePro-Bold.ttf", 35)

    roboto_condensed_light = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/RobotoCondensed-Light.ttf", 15)
    roboto_condensed_light_small = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/RobotoCondensed-Light.ttf", 10)
    roboto_condensed_medium = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/RobotoCondensed-Medium.ttf", 15)
    roboto_condensed_bold = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/RobotoCondensed-Bold.ttf", 15)
    roboto_condensed_semibold = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/RobotoCondensed-SemiBold.ttf", 15)
    roboto_condensed_regular = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/RobotoCondensed-Regular.ttf", 15)
    roboto_condensed_bold_large = ImageFont.truetype("/home/evolmonster/InkyWeatherStation/fonts/RobotoCondensed-Bold.ttf", 35)

    # Get data from weather provider
    try:
        print("Calling weather data function")

        url = config.weather_url.format(
            config.latitude, config.longitude, config.weather_api_key
        )
        response = requests.get(url)
        data = response.json()

        response.close()

        weather_data_response = WeatherDataHandler(data)
        weather_data = weather_data_response.weather_data

    except Exception as exc:
        LoggingHandler.handle_exception("Error in calling the weather API", exc)

    # Get Data from ToDo provider
    try:
        print("calling todo data function")
        tododata = ToDoData(config.todoist_api_key, config.todoist_project)
        tododata.GetTodoList()
        # print(tododata.todolist.tasks)
    except Exception as exc:
        LoggingHandler.handle_exception("Error in calling the todo API", exc)

    # Get Data from google calendar provider
    if calendar_events_display:
        try:
            print("Calling google calendar data function")
            calendardata = GoogleCalendarData()
            calendardata.GetCalendarData()
        except Exception as exc:
            LoggingHandler.handle_exception(
                "Error in calling the google calendar API", exc
            )

    # TODO Check if we have weather and TODO data. If not, no need to update the screen
    # Eventually we want to store the data locally, and reload it with an error picture somewhere on screen so I know it didnt update

    # Create a new canvas to draw on
    img = Image.new("P", inky_display.resolution)
    canvas = ImageDraw.Draw(img)
    canvas_height = inky_display.height  # 300
    canvas_width = inky_display.width  # 400

    #try:
    #    inky_display.set_border(inky_display.BLACK)
    #except NotImplementedError:
    #    pass

    # Draw out the boxes on screen
    # canvas.line([(0,canvas_height / 2),(canvas_width,canvas_height / 2)], fill=inky_display.BLACK,width=3)
    canvas.line([(canvas_width / 2.5, 0), (canvas_width / 2.5, canvas_height)], fill=inky_display.BLACK, width=2,)
    canvas.line([(0, 95), (160,95)], fill=inky_display.BLACK, width=2,)
    canvas.line([(0, 115), (160,115)], fill=inky_display.BLACK, width=2,)
    #canvas.line([(0, 95), (0,115)], fill=inky_display.BLACK, width=2,)
    # canvas.line([(canvas_width / 1.43,0),(canvas_width /1.43,canvas_height / 2)], fill=inky_display.BLACK,width=2)
    # canvas.line([(canvas_width / 2.5,canvas_height/4),(canvas_width,canvas_height / 4)], fill=inky_display.BLACK,width=2)
    # canvas.line([(55, canvas_height / 2),(55,canvas_height / 2.25)], fill=inky_display.BLACK,width=1)

    # canvas.rounded_rectangle((0, 0, 160, 150),
    #                    fill=None,
    #                    outline=inky_display.BLACK,
    #                    width=3,
    #                    radius=7,
    #                    corners=(False,False,True,False))

    # TODO: After midnight, it goes to the next day. Making the sun show instead of stars after midnight
    # Set the message. If its night time, take the second icon, which is for night

    if current_weather_display:
        weather_count = 0
        weather_icon_placement = [[0,0], [0,117], [0,162], [0,207], [0,252]]
        moon_icon_placement = [[0,0], [130,115], [130,160], [130,205], [130,250]]
        day_of_week_placement = [[0,0], [34,128], [34,173], [34,218], [34,263]]
        low_icon_placement = [[0,0], [60,118], [60,163], [60,208], [60,253]]
        high_icon_placement = [[0,0], [95,118], [95,163], [95,208], [95,253]]

        # Loop through each day of weather
        for weather in weather_data:

            #draw the current date weather at the top of the section
            #TODO Perhaps check the dates here instead of using 0. So if its today, use this data.
            if weather_count == 0:
                canvas.text((0, 0), weather.weather_icon, inky_display.BLACK, font=weather_icons_font)
                canvas.text((120, -10), weather.moon_phase, inky_display.BLACK, font=weather_icons_font_moon)
                canvas.text((60,-5), weather.precipitation_icon, inky_display.BLACK, font=weather_icons_font_smaller)
                canvas.text((75, 0), weather.precipitation_chance, inky_display.BLACK, font=roboto_condensed_light)            
                canvas.text((62,15), weather.wind_icon, inky_display.BLACK, font=weather_icons_font_smaller)
                canvas.text((75, 23), weather.wind_speed, inky_display.BLACK, font=roboto_condensed_light)
                
                wind_mph_x = 85
                if len(weather.wind_speed) == 2:
                    wind_mph_x = 92
                canvas.text((wind_mph_x, 26), "mph", inky_display.BLACK, font=roboto_condensed_light_small)

                degree_x = 98
                temp_x = 60
                if len(weather.temp) > 2:
                    degree_x = 105
                    temp_x = 50
                canvas.text((temp_x, 45), weather.temp, inky_display.BLACK, font=roboto_condensed_bold_large)
                canvas.text((degree_x, 42), weather.degree_icon, inky_display.BLACK, font=weather_icons_font_small)
                #TODO move all these magic icons into variables on the class
                canvas.text((0, 40), "\uf044", inky_display.BLACK, font=weather_icons_font_small)
                canvas.text((145, 40), "\uf058", inky_display.BLACK, font=weather_icons_font_small)
                canvas.text((15, 53), weather.min_temp, inky_display.BLACK, font=roboto_condensed_light)
                canvas.text((30, 43), weather.degree_icon, inky_display.BLACK, font=weather_icons_font_small)

                max_temp_x = 123
                if len(weather.max_temp) > 2:
                    max_temp_x = 112
                canvas.text((max_temp_x, 53), weather.max_temp, inky_display.BLACK, font=roboto_condensed_light)
                canvas.text((max_temp_x + 15, 43), weather.degree_icon, inky_display.BLACK, font=weather_icons_font_small)
                canvas.text((0, 75), "\uf046", inky_display.BLACK, font=weather_icons_font_smaller)
                canvas.text((135, 75), "\uf047", inky_display.BLACK, font=weather_icons_font_smaller)

                canvas.text((26, 78), weather.morning_temp, inky_display.BLACK, font=roboto_condensed_light)
                canvas.text((43, 68), weather.degree_icon, inky_display.BLACK, font=weather_icons_font_small)
                canvas.text((115, 78), weather.night_temp, inky_display.BLACK, font=roboto_condensed_light)
                canvas.text((130, 68), weather.degree_icon, inky_display.BLACK, font=weather_icons_font_small)

                canvas.text((0, 97), weather.sunrise, inky_display.BLACK, font=roboto_condensed_light)                
                canvas.text((127, 97), weather.sunset, inky_display.BLACK, font=roboto_condensed_light)

                canvas.text((55, 97), weather.date_of_week, inky_display.BLACK, font=roboto_condensed_bold)

            elif weather_count >0:
                canvas.text((weather_icon_placement[weather_count][0], weather_icon_placement[weather_count][1]), weather.weather_icon, inky_display.BLACK, font=weather_icons_font_week_smaller)
                canvas.text((moon_icon_placement[weather_count][0], moon_icon_placement[weather_count][1]), weather.moon_phase, inky_display.BLACK, font=weather_icons_font_moon_small)
                canvas.text((day_of_week_placement[weather_count][0], day_of_week_placement[weather_count][1]), weather.day_of_week, inky_display.BLACK, font=roboto_condensed_light)

                canvas.text((low_icon_placement[weather_count][0], low_icon_placement[weather_count][1]), "\uf044", inky_display.BLACK, font=weather_icons_font_week_smaller)
                canvas.text((high_icon_placement[weather_count][0], high_icon_placement[weather_count][1]), "\uf058", inky_display.BLACK, font=weather_icons_font_week_smaller)
                canvas.text((low_icon_placement[weather_count][0] + 10, low_icon_placement[weather_count][1] + 10), weather.min_temp, inky_display.BLACK, font=roboto_condensed_light)
                canvas.text((high_icon_placement[weather_count][0] + 10, high_icon_placement[weather_count][1] + 10), weather.max_temp, inky_display.BLACK, font=roboto_condensed_light)
                canvas.text((low_icon_placement[weather_count][0] + 25, low_icon_placement[weather_count][1] + 2), weather.degree_icon, inky_display.BLACK, font=weather_icons_font_week_smaller)
                canvas.text((high_icon_placement[weather_count][0] + 25, high_icon_placement[weather_count][1] + 2), weather.degree_icon, inky_display.BLACK, font=weather_icons_font_week_smaller)
                

            weather_count += 1


        # Sunrise / Sunset display
        #canvas.text((18, 108), "\uf046", inky_display.BLACK, font=weather_icons_font_small)
        #canvas.text((73, 108), "\uf047", inky_display.BLACK, font=weather_icons_font_small)
        #canvas.text((5, 130), current_sunrise, inky_display.BLACK, font=roboto_condensed_light)
        #canvas.text((60, 130), current_sunset, inky_display.BLACK, font=roboto_condensed_light)

        # Current weather temp and description
        #canvas.text((5, 5), str(data.currentweather.dateTime.strftime("%A %d %b")).lower(), inky_display.BLACK, font=roboto_condensed_bold)
        # TODO If the current temp is >= 100 then make the text smaller and re-align to the left a bit
        #canvas.text((82, 17), current_temp, inky_display.BLACK, font=roboto_condensed_bold_large)
        #canvas.text((82, 55), current_min_temp, inky_display.BLACK, font=roboto_condensed_light)
        #canvas.text((100, 55), current_max_temp, inky_display.BLACK, font=roboto_condensed_light)

        #canvas.arc((70, 8, 130, 70), start=140, end=40, fill=inky_display.BLACK, width=4)

    if todo_list_display:

        # Add the TODO list data to canvas
        canvas.text((170, 5), "todo:", inky_display.BLACK, font=roboto_condensed_bold)
        todoline = 23
        right_todo_line = 170
        tododotleft = 176
        tododotright = 181
        todo_text_left = 180
        todo_dot_left = 5

        task_count = 0
        for task in tododata.todolist.tasks:
            # if task_count > 10:
            #    todo_text_left = 170
            #    todo_dot_left = 165

            # if task_count == 6:
            #    todoline = right_todo_line

            # canvas.ellipse((todo_dot_left, tododotleft, 10, tododotright), fill=inky_display.BLACK, width=4)
            canvas.text((todo_text_left - 10, todoline -5),"\uf042",inky_display.BLACK,font=weather_icons_font_small)
            canvas.text((todo_text_left, todoline),task,inky_display.BLACK,font=roboto_condensed_light)
            todoline += 20
            tododotleft += 20
            tododotright += 20
            task_count += 1
            # if task_count > 6:
            #    right_todo_line += 20

    if calendar_events_display:
        # Add the calendar data to canvas
        calendarline = 170
        for event in calendardata.eventlist.events:
            # canvas.text((180, calendarline), event.summary, inky_display.BLACK, font=source_code_pro_font)
            # TODO Maybe draw box around the calendar events with the time/date at the top and multiline text below
            # limit the number or boxes we can show depending on how many boxes we can fit

            # canvas.multiline_text((180, calendarline), event.summary, inky_display.BLACK, font=roboto_condensed_light, spacing=10)
            calendarline += 20
            # print(event.summary)
            # print(event.date)
            # print(event.time)

    # Update the Inky display with canvas data
    inky_display.set_image(img)
    inky_display.show()

    # Write date and time to log file to signify last run
    LoggingHandler.log_run_complete()


if __name__ == "__main__":
    main()
