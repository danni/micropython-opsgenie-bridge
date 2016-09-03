import time
import logging
import machine

import usocketio.client

logging.basicConfig(level=logging.DEBUG)


def main():
    pin13 = machine.Pin(13)
    pin13.init(machine.Pin.OUT)

    pin12 = machine.Pin(12)
    pin12.init(machine.Pin.OUT)

    with usocketio.client.connect('http://192.168.1.10:5000/') as socketio:
        @socketio.on('message')
        def on_message(self, message):
            print("message", message)

        @socketio.on('alert')
        def on_alert(self, message):
            print("alert", message)
            pin13.high()
            time.sleep(0.3)
            pin13.low()

        try:
            pin12.high()
            socketio.run_forever()
        finally:
            pin12.low()

main()
