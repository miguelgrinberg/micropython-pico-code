import machine
import time

LED_PIN = 'WL_GPIO0'
BUTTON_PIN = 2  # GP2 pin

def blink():
    led = machine.Pin(LED_PIN, machine.Pin.OUT)
    button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    while True:
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)
    led.off()

blink()
