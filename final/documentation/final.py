import os, sys, io
import M5
from M5 import *
from umqtt import *
from hardware import *
from servo import Servo
from machine import ADC, Pin
import time
from time import sleep_ms
from driver.neopixel import NeoPixel

mqtt_client = None
user_name = 'skzmdlp'
mqtt_timer = 0
adc = None
adc_val = None

servo = Servo(pin=7)
button_val = 1
# configure ADC input on pin G2 with 11dB attenuation:
#adc = ADC(Pin(2), atten=ADC.ATTN_11DB)
adc = ADC(Pin(1), atten=ADC.ATTN_11DB)

program_state = "OFF"

def setup():
  global mqtt_client
  global adc
  M5.begin()
  mqtt_client = MQTTClient(
      'testclient',
      'io.adafruit.com',
      port=1883, 
      user=user_name,
      password='aio_Dwed44jkCjaUQDmxvcKXVZZOwCqu',
      keepalive=3000
  )
  mqtt_client.connect(clean_session=True)
  # configure ADC input on pin G8 with 11dB attenuation:
  #adc = ADC(Pin(8), atten=ADC.ATTN_11DB)



def loop():
  global mqtt_client
  global mqtt_timer
  global adc, adc_val
  global button_val
  global program_state
  M5.update()
  adc_val = adc.read()
  # publish when button is pressed:
  print('adc_val =', adc_val)
  if program_state == "OFF":
    if adc_val <= 10:
      mqtt_client.publish(user_name+'/feeds/test-feed', str(button_val), qos=0)
      button_val = 0
      print('0')
      program_state = "ON"
    else:
      servo.move(90)
  if program_state == "ON":
    if adc_val >= 10:
      mqtt_client.publish(user_name+'/feeds/test-feed', str(button_val), qos=0)
      button_val = 1
      print('1')
      program_state = "OFF"
    else:
      servo.move(100)
    #mqtt_client.publish(user_name+'/feeds/test-feed', 'OFF', qos=0)
  # publish every 2.5 seconds:
#   if(time.ticks_ms() > mqtt_timer + 2500):
#     # read 12-bit analog value (0 - 4095 range):
#     adc_val = adc.read()
#     # publisch analog value as a string:
#     mqtt_client.publish(user_name+'/feeds/adc-feed', str(adc_val), qos=0)
#     print('publish data..')
#     # update timer:
#     mqtt_timer = time.ticks_ms()
  time.sleep_ms(100)
      

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
