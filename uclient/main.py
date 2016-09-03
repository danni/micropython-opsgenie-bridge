import time
import logging
import machine

import usocketio.client

logging.basicConfig(level=logging.DEBUG)


def main():
    ready_led = machine.Pin(12)
    ready_led.init(machine.Pin.OUT)

    alert_led = machine.Pin(13)
    alert_led.init(machine.Pin.OUT)

    ack_btn = machine.Pin(14)
    ack_btn.init(machine.Pin.IN, machine.Pin.PULL_UP)
    acknowledge = [False]  # flag to set in the interrupt handler

    with usocketio.client.connect('http://192.168.1.10:5000/') as socketio:

        # register an interrupt handler for the acknowledge button
        def button_interrupt(pin):
            acknowledge[0] = True

        ack_btn.irq(trigger=machine.Pin.IRQ_FALLING,
                    handler=button_interrupt)

        @socketio.on('alert')
        def on_alert(message):
            print("alert", message)
            pin13.high()
            time.sleep(0.3)
            pin13.low()

        @socketio.at_interval(1)
        def at_interval():
            if acknowledge[0]:
                socketio.send('acknowledge')
                acknowledge[0] = False

        try:
            ready_led.high()
            socketio.run_forever()
        finally:
            ready_led.low()

main()
