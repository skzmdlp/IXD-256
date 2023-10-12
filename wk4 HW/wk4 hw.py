# change RGB LED colors with digital input and time using state logic
# 4 states are implemented as shown:
# 'START'  -> turns on RGB green
# 'OPEN'   -> pulsate RGB blue
# 'CLOSED' -> fade in RGB yellow if digital input is closed
# 'FINISH' -> fade in RGB red 5 seconds after 'CLOSED' state
#             fade out RGB to black after 2 seconds

import os, sys, io
import M5
from M5 import *
from hardware import *
import time
# import NeoPixel module:
from driver.neopixel import NeoPixel

# global variable for neopixel strip:
np = None

rainbow = [
  (126 , 1 , 0),(114 , 13 , 0),(102 , 25 , 0),(90 , 37 , 0),(78 , 49 , 0),(66 , 61 , 0),(54 , 73 , 0),(42 , 85 , 0),
  (30 , 97 , 0),(18 , 109 , 0),(6 , 121 , 0),(0 , 122 , 5),(0 , 110 , 17),(0 , 98 , 29),(0 , 86 , 41),(0 , 74 , 53),
  (0 , 62 , 65),(0 , 50 , 77),(0 , 38 , 89),(0 , 26 , 101),(0 , 14 , 113),(0 , 2 , 125),(9 , 0 , 118),(21 , 0 , 106),
  (33 , 0 , 94),(45 , 0 , 82),(57 , 0 , 70),(69 , 0 , 58),(81 , 0 , 46),(93 , 0 , 34),(105 , 0 , 22),(117 , 0 , 10)]

rgb = None
state = 'START'
state_timer = 0

def setup():
  global rgb, input_pin, state, state_timer, np, rainbow
  M5.begin()
  
  global np
  # initialize neopixel strip on pin G2 with 16 pixels:
  np = NeoPixel(pin=Pin(2), n=30)
  
  # custom RGB setting using pin G35 (M5 AtomS3 built-in LED):
  rgb = RGB(io=2, n=30, type="SK6812")
  
  # custom RGB setting using pin G2 (M5 AtomS3 bottom connector) and 10 LEDs:
  #rgb = RGB(io=2, n=30, type="SK6812")
  
  # initialize pin G41 (M5 AtomS3 built-in button) as input:
  #input_pin = Pin(41)
  
  # initialize pin G39 (M5 PortABC Extension red connector) as input:
  input_pin = Pin(39, Pin.IN, Pin.PULL_UP)
  
  # turn on RGB green and wait 2 seconds:

def loop():
  global state, state_timer, np, rainbow
  M5.update()
  if (state == 'START'):
    print('start with RGB green..')
    rgb.fill_color(get_color(0, 255, 0))
    time.sleep(2)  
    check_input()
      
  if (state == 'OPEN'):
    print('rainbow..')
    # fade in RGB blue:
    # cycle the list of rainbow colors:
    rainbow = rainbow[-1:] + rainbow[:-1]
    for i in range(30):
    # set pixel i to color i of rainbow:
      np[i] = rainbow[i]
    # update neopixel strip:
    np.write()
    time.sleep_ms(50)
    check_input()
    
  elif (state == 'CLOSED'):
    # if less than 1 seconds passed since change to 'CLOSED':
    if(time.ticks_ms() < state_timer + 1000):
      check_input()
      print('fade in yellow..')
      for i in range(100):
        rgb.fill_color(get_color(i, i, 0))
        time.sleep_ms(20)
    # if more than 3 seconds passed since change to 'CLOSED':
    elif(time.ticks_ms() > state_timer + 3000):
      check_input()
      state = 'FINISH'
      print('change to', state)
      # save current time in milliseconds:
      state_timer = time.ticks_ms()
      
  elif (state == 'FINISH'):
    print('fade from yellow to red..')
    for i in range(100):
      rgb.fill_color(get_color(100, 100-i, 0))
      time.sleep_ms(20)
      check_input()
      
    # if 2 seconds passed since change to 'FINISH':
    if(time.ticks_ms() > state_timer + 200):
      for i in range(100):#1
        rgb.fill_color(get_color(100-i, 0, 0))
      for i in range(100):
        rgb.fill_color(get_color(i, 0, 0))
      for i in range(100):#2
        rgb.fill_color(get_color(100-i, 0, 0))
      for i in range(100):
        rgb.fill_color(get_color(i, 0, 0))
      for i in range(100):#3
        rgb.fill_color(get_color(100-i, 0, 0))
      for i in range(100):
        rgb.fill_color(get_color(i, 0, 0))
      for i in range(100):
        rgb.fill_color(get_color(i, 0, 0))
      time.sleep_ms(20)
      print('fade from red to green..') 
      for i in range(100):
        rgb.fill_color(get_color(100-i, i, 0))
        time.sleep_ms(20)
      time.sleep(1)
      state = 'START'
      check_input()

# check input pin and change state to 'OPEN' or 'CLOSED'
def check_input():
  global state, state_timer
  if (input_pin.value() == 0):
    if(state != 'FINISH'):
      print('change to CLOSED')
    state = 'FINISH'
    time.sleep_ms(20)
    # save current time in milliseconds:
    state_timer = time.ticks_ms()
  else:
    if(state != 'OPEN'):
      print('change to OPEN')
    state = 'OPEN'
    time.sleep_ms(20)
    
    
# convert separate r, g, b values to one rgb_color value:  
def get_color(r, g, b):
  rgb_color = (r << 16) | (g << 8) | b
  return rgb_color

if __name__ == '__main__':
  try:
    setup()
    while True:
      loop()
  except (Exception, KeyboardInterrupt) as e:
    try:
      from utility import print_error_msg
      print_error_msg(e)
    except ImportError:
      print("please update to latest firmware")


