from subprocess import call
import time
import requests, json
import urllib.request as urllib2

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import sys


# D.H: Basic components
def turn_on_all_led_on_with_given_color(pixels, R, G, B):
    # Function: Turn on 60 LEDs with the given color value
    # Arguments: R, G, B (0~255 for each color Red, Green, Blue)

    # write the given color on LEDs
    pixels.fill((R, G, B))

    # update
    pixels.show()


def turn_off_led(pixels):
    # Function: Turn off 60 LEDs with the given color value
    # pixels: reference of led instance

    # turn off all LEDs
    pixels.fill((0, 0, 0))

    # update
    pixels.show()


def blinking_led(pixels, R, G, B, number_of_blinking, seconds_led_on, seconds_led_off):
    # For the number of blinking, turn on and off all the leds with the given (R, G, B => Red, Green, Blue)
    # pixels: reference of led instance

    # turn off all LEDs
    turn_off_led(pixels)

    # for the given repeat number,
    for _ in range(number_of_blinking):
        # write the given color on LEDs
        turn_on_all_led_on_with_given_color(pixels, R, G, B)
        # wait a moment
        time.sleep(seconds_led_on)

        # turn off all LEDs
        turn_off_led(pixels)
        # wait a moment
        time.sleep(seconds_led_off)


def led_flow_on_clock_wise(pixels, number_of_leds, R, G, B, seconds_wait):
    # One led cell flows in clock-wise
    # pixels: reference of led instance

    # turn off all LEDs
    turn_off_led(pixels)

    # start from power source side
    for index_led in range(number_of_leds):
        # turn off previous LED cell
        if index_led > 0:
            pixels[index_led - 1] = (0, 0, 0)

        # write color on current LED cell
        pixels[index_led] = (R, G, B)
        # update neopixel
        pixels.show()

        # wait a moment
        time.sleep(seconds_wait)


def even_and_odd_led(pixels, number_of_leds, R, G, B, is_odd_on, is_even_on):
    # control odd and even number of LEDs separately

    # turn off all LEDs
    turn_off_led(pixels)

    # start from power source side
    for index_led in range(number_of_leds):
        # even number of led
        if index_led % 2 == 0:
            if is_even_on is True:
                pixels[index_led] = (R, G, B)
        # odd number of led
        else:
            if is_odd_on is True:
                pixels[index_led] = (R, G, B)

    # update neopixel
    pixels.show()


# J.W: Call this function inside his loop
def wake_up_led(pixels):
    # turn off all LEDs
    turn_off_led(pixels)

    # One led cell flows in clock-wise
    led_flow_on_clock_wise(pixels, 60, 255, 255, 255, 0.005)

    # signals to represent that it's preparing activation
    blinking_led(pixels, 255, 255, 255, 2, 0.3, 0.1)

    # listen right away
    turn_on_all_led_on_with_given_color(pixels, 255, 255, 255)


def fail_speech_recognition_led(pixels):
    # turn off all LEDs
    turn_off_led(pixels)

    # signals to represent wrong speech input
    blinking_led(pixels, 255, 0, 0, 2, 0.6, 0.2)


def listening_mode_led(pixels):
    # turn off all LEDs
    turn_off_led(pixels)

    # notice that it's listening: white LEDs
    turn_on_all_led_on_with_given_color(pixels, 255, 255, 255)


def processing_1(pixels):
    # turn off all LEDs
    turn_off_led(pixels)

    # One led cell flows in clock-wise
    for _ in range(4):
        led_flow_on_clock_wise(pixels, 60, 255, 35, 214, 0.015)

    # signals to represent that it's preparing activation
    blinking_led(pixels, 255, 35, 214, 2, 0.4, 0.1)

    # turn off all LEDs
    turn_off_led(pixels)


def processing_2(pixels):
    # turn off all LEDs
    turn_off_led(pixels)

    for _ in range(8):
        # One led cell flows in clock-wise
        even_and_odd_led(pixels, 60, 255, 35, 214, True, False)
        time.sleep(0.4)

        # One led cell flows in clock-wise
        even_and_odd_led(pixels, 60, 255, 35, 214, False, True)
        time.sleep(0.4)

    # turn off all LEDs
    turn_off_led(pixels)


def sleep(pixels):
    # turn off all LEDs
    turn_off_led(pixels)


def main():
    # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
    # NeoPixels must be connected to "D10(o: issue), D12(o), D18(x) or D21(x)" to work.
    # board.Dx -> GPIO x (number)
    pixel_pin = board.D12
    # The number of NeoPixels
    number_of_leds = 60
    # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
    # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
    # Dreami: RGB
    pixels = neopixel.NeoPixel(pixel_pin, number_of_leds, brightness=1, auto_write=False,
                               pixel_order=neopixel.GRB)
    # start from turn off all LEDs
    turn_off_led(pixels)
    time.sleep(0.1)

    # server-connection configuration
    session = requests.Session()
    session.trust_env = False
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    get_url = 'http://125.181.80.84:3000/getLED'


    while True:
        res = session.post(url=get_url, headers=headers)
        led_status = res.json()['blink']
        print(led_status)
        if led_status == 0:
            time.sleep(0.1)
        if led_status == 1:
            wake_up_led(pixels)
        if led_status == 2:
            listening_mode_led(pixels)
        if led_status == 3:
            fail_speech_recognition_led(pixels)
        if led_status == 4:
            processing_2(pixels)
        if led_status == 5:
            sleep(pixels)

if __name__ == "__main__":
    main()
