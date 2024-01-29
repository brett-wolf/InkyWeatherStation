from time import strftime
from datetime import datetime
import pytz
from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from WeatherData import WeatherData

def getsize(font, text):
    _, _, right, bottom = font.getbbox(text)
    return (right, bottom)

#print the current time
print(strftime("%X %Z"))

#print the current date
print(strftime("%d-%m-%Y"))

#print the current day
print(strftime("%A"))

#print time in London
londonTimeZone = pytz.timezone('Europe/London')
timeInLondon = datetime.now(londonTimeZone)
currentTimeInLondon = timeInLondon.strftime("%X %Z")
print(currentTimeInLondon)

try:
    inky_display = auto(ask_user=True, verbose=True)
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")

try:
    inky_display.set_border(inky_display.BLACK)
except NotImplementedError:
    pass

# Set scaling for display size
scale_size = 2.20
padding = 15

# Create a new canvas to draw on
img = Image.new("P", inky_display.resolution)
draw = ImageDraw.Draw(img)

# Load the fonts
hanken_bold_font = ImageFont.truetype(HankenGroteskBold, int(10 * scale_size))

# Get data from weather provider
try:
    data = WeatherData(37.55589989488259, -77.4800165092538, "6284869d5895baaf5f2537c1e6872fb0")

except:
    print("Error in calling the weather API")
    #return


# Set the message
message = strftime("%X")

# Top and bottom y-coordinates for the white strip
y_top = int(inky_display.height * (0 / 10.0))
y_bottom = y_top + int(inky_display.height * (3.0 / 10.0))

for y in range(0, y_top):
    for x in range(0, inky_display.width):
        img.putpixel((x, y), inky_display.BLACK if inky_display.colour == "black" else inky_display.BLACK)
for y in range(y_top, y_bottom):
    for x in range(0, inky_display.width):
        img.putpixel((x, y), inky_display.WHITE)

for y in range(y_bottom, inky_display.height):
    for x in range(0, inky_display.width):
        img.putpixel((x, y), inky_display.BLACK if inky_display.colour == "black" else inky_display.BLACK)

# Calculate position and draw the message
message_w, message_h = getsize(hanken_bold_font, message)
message_x = int((inky_display.width - message_w) / 2)
message_y = 0 + padding

draw.text((message_x, message_y), message, inky_display.BLACK, font=hanken_bold_font)

inky_display.set_image(img)

#inky_display.getModified()
inky_display.show()


exit()