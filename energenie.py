import RPi.GPIO as GPIO
import time

all_sockets = 0b0011
socket1 = 0b0111
socket2 = 0b0110
socket3 = 0b0101
socket4 = 0b0100
turn_on = 0b1000

D3 = 13
D2 = 16
D1 = 15
D0 = 11

ask = 18
modulate = 22
ready = False


def _set_gpio():
    global ready
    if not ready:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        for pin in D3, D2, D1, D0, ask, modulate:
            GPIO.setup(pin, GPIO.OUT)
        GPIO.output(modulate, False)   # disable modulator
        GPIO.output(ask, False)        # basic ASK
        for pin in D3, D2, D1, D0:
            GPIO.output(pin, False)    # Start at all zeros
        ready = True


def _transmit(code):
    if not ready:
        _set_gpio()
    GPIO.output(D3, bool(code & 0B1000))
    GPIO.output(D2, bool(code & 0B0100))
    GPIO.output(D1, bool(code & 0B0010))
    GPIO.output(D0, bool(code & 0B0001))
    time.sleep(0.1)
    GPIO.output(modulate, True)
    time.sleep(0.25)
    GPIO.output(modulate, False)


def _encode(number):
    if number == 1:
        code = socket1
    elif number == 2:
        code = socket2
    elif number == 3:
        code = socket3
    elif number == 4:
        code = socket4
    else:
        print('We only support sockets 1 to 4')
        return 0
    return code


def program_socket(number):
    print('Setting up socket', number)
    input('Press green button on chosen socket for 5+ seconds')
    on(number)
    off(number)


def on(socket):
    if socket == 'all':
        _transmit(all_sockets | turn_on)
    else:
        _transmit(_encode(socket) | turn_on)


def off(socket):
    if socket == 'all':
        _transmit(all_sockets)
    else:
        _transmit(_encode(socket))

