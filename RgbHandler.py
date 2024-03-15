from rgbmatrix5x5 import RGBMatrix5x5
import time

class RgbHandler(object):
    def cycle_rgb():
        rgbmatrix5x5 = RGBMatrix5x5()
        rgbmatrix5x5.set_clear_on_exit()
        rgbmatrix5x5.set_brightness(1.0)

        stripes = [
            (0,5),
            (5,10),
            (10,15),
            (15,20),
            (20,25)
        ]

        i = 0
        while i < 5:
            for stripe in stripes:
                rgbmatrix5x5.set_multiple_pixels(list(range(stripe[0], stripe[1])), (255,255,0))
                rgbmatrix5x5.show()
                time.sleep(0.5)

            rgbmatrix5x5.set_all(0,0,0)
            i += 1