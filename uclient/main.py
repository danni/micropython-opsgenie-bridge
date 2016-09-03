import time
import logging
from machine import Pin, PWM

import usocketio.client

logging.basicConfig(level=logging.DEBUG)

blue_led = PWM(Pin(14))
blue_led.freq(60)
green_led = PWM(Pin(12))
green_led.freq(60)
red_led = PWM(Pin(13))
red_led.freq(60)


def set_colour(r, g, b):
    """
    Set the colour as a hex triplet

    Common anode RGB LED, high is off
    """

    red_led.duty((0xff - r) << 2)
    green_led.duty((0xff - g) << 2)
    blue_led.duty((0xff - b) << 2)

set_colour(0, 0, 0)

ack_btn = Pin(5)
ack_btn.init(Pin.IN, Pin.PULL_UP)


def main():
    acknowledge = [False]  # flag to set in the interrupt handler

    with usocketio.client.connect('http://192.168.1.10:5000/') as socketio:

        # register an interrupt handler for the acknowledge button
        def button_interrupt(pin):
            acknowledge[0] = True

        ack_btn.irq(trigger=Pin.IRQ_FALLING,
                    handler=button_interrupt)

        @socketio.on('alert')
        def on_alert(message):
            STATUSES = {
                'green': (0, 0xff, 0),
                'red': (0xff, 0, 0),
                'orange': (0xff, 0x45, 0),
            }
            try:
                set_colour(*STATUSES[message['status']])
            except KeyError:
                print("Unknown colour:", message['status'])

        @socketio.at_interval(1)
        def at_interval():
            if acknowledge[0]:
                socketio.send('acknowledge')
                acknowledge[0] = False

        try:
            set_colour(0, 0, 0xff)
            socketio.run_forever()
        finally:
            set_colour(0, 0, 0)


while True:
    try:
        main()
    except OSError:
        print("Retry in 10")
        time.sleep(10)
