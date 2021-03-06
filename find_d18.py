# import RPi.GPIO as GPIO
# import board
# import time
#
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
#
# # pin = board.D18
#
# GPIO.setup(18, GPIO.OUT)
# GPIO.output(18, GPIO.HIGH)
# while True:
#     print(board.D18)
#     time.sleep(1)

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D12

# The number of NeoPixels
num_pixels = 30

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=True,
                           pixel_order=ORDER)

while True:
    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((255, 0, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    #pixels.fill((255, 0, 0, 0))
    pixels.show()
    time.sleep(2)

    print('ing')
    pixels.fill((0,0,0))
    pixels.show()
    time.sleep(2)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    #pixels.fill((0, 255, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 255, 0, 0))
    #pixels.show()
    #time.sleep(1)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((255, 255, 255))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 0, 255, 0))
    pixels.show()
    time.sleep(2)

    #rainbow_cycle(0.001)    # rainbow cycle with 1ms delay per step



