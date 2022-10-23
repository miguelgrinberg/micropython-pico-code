import machine
import network
import sys
import time
import urequests as requests
import config

def connect_wifi():
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to WiFi...')
        sta_if.active(True)
        sta_if.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        while not sta_if.isconnected():
            time.sleep(1)
    print('Network config:', sta_if.ifconfig())

def call_webhook():
    print('Invoking webhook')
    response = requests.post(config.WEBHOOK_URL,
                             json={'value1': config.BUTTON_ID})
    if response is not None and response.status_code < 400:
        print('Webhook invoked')
    else:
        print('Webhook failed')
        raise RuntimeError('Webhook failed')

def show_error():
    led = machine.Pin(config.LED_PIN, machine.Pin.OUT)
    for i in range(3):
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)

def is_debug():
    debug = machine.Pin(config.DEBUG_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    return debug.value() == 0

def run():
    debug = is_debug()
    try:
        if not debug:
            connect_wifi()
            call_webhook()
        else:
            print('Debug mode detected. Skipping network calls and sleep.')
    except Exception as exc:
        sys.print_exception(exc)
        show_error()
    if not debug:
        machine.deepsleep()

run()
