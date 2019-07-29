from pynetwork import *
from pynetwork.backend2 import safe_print
import RPi.GPIO as GPIO
import time

class RC_host:

    def __init__(self, port):
        self.pwm_objects = {}
        self.digital_out_pins = []
        self.port= port
        self.gateway = Gateway(port = self.port)
        self.gateway.add_subroutine('config_digital_io', self.configure_digital)
        self.gateway.add_subroutine('config_pwm', self.configure_pwm)
        self.gateway.add_subroutine('digital_out', self.digital_out)
        self.gateway.add_subroutine('digital_in', self.digital_in)
        self.gateway.add_subroutine('start_pwm', self.start_pwm)
        self.gateway.add_subroutine('stop_pwm', self.stop_pwm)
        self.gateway.add_subroutine('change_pwm', self.change_pwm)
        self.gateway.add_subroutine('io_cleanup',GPIO.cleanup)
        self.gateway.add_subroutine('io_set_mode_bcm', self.io_set_mode_bcm)
        # GPIO.setmode(GPIO.BCM)

    def io_set_mode_bcm(self):
        GPIO.setmode(GPIO.BCM)

    def test_host(self):
        safe_print('test success returning 1 as a response')

    def configure_digital(self, digital_in: [] = [], digital_out: [] = []):
        safe_print('Setting digital_in:', digital_in)
        safe_print('Setting digital_out:', digital_out)
        for pin in digital_out:
            GPIO.setup(pin, GPIO.OUT)
        for pin in digital_in:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        r = len(digital_in) + len(digital_out)
        return r

    # batch-data send
    def configure_pwm(self, pins: [] = []):  # format [(pin, name, frequency), ...]
        for pin, name, freq in pins:
            safe_print('setting pwm:', pin, name, freq)
            self.pwm_objects[name] = GPIO.PWM(pin, freq)

    # batch-data send
    def start_pwm(self, name, duty_cycle):
        if name not in self.pwm_objects:
            raise Exception('pwm obj not available')
        self.pwm_objects[name].start(duty_cycle)

    # batch-data send
    def stop_pwm(self, name):
        if name not in self.pwm_objects:
            raise Exception('pwm obj not available')
        self.pwm_objects[name].stop()

    # batch-data send
    def change_pwm(self, name, duty_cycle):
        if name not in self.pwm_objects:
            raise Exception('pwm obj not available')
        self.pwm_objects[name].ChangeDutyCycle(duty_cycle)

    # batch-data-send
    def digital_out(self, pins=[], states=[]):
        safe_print('pins:', pins)
        safe_print('states:', states)
        for pin, state in zip(pins, states):
            GPIO.output(pin, state)
        return len(pins)

    # batch-data-receive
    def digital_in(self, pins=[]):
        result = []
        for pin in pins:
            result.append(GPIO.input(pin))
        return result

    def reset_states(self):
        for item in self.pwm_objects:
            self.stop_pwm(item)
        self.digital_out(self.digital_out_pins, [0 for pin in self.digital_out_pins])
        pwm_objects = {}
        digital_out_pins = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        # Exception handling here
        self.stop()

    def start(self, blocking: bool = True):
        self.reset_states()
        self.gateway.start(blocking= blocking)

    def stop(self):
        self.reset_states()
        if self.gateway.is_running:
            self.gateway.stop()


if __name__ == '__main__':
    with RC_host(port = 1857) as host:
        host.start()

