from pynetwork import Controller, Client
from pynetwork.backend2 import safe_print
import warnings
import inspect
fun_name = lambda: inspect.stack()[1][3]
import time

class RC_client:

    def __init__(self, ip:int, port:int):
        self.ip = ip
        self.port= port
        self.is_connected = False

    def __validate__(self):
        if not self.is_connected or self.controller is None or self.client is None:
            warnings.warn('RC_client will not send this command as host pi is not connected yet')
            return False
        return True

    def connect(self):
        if not self.is_connected:
            self.controller = Controller(gateway_ip=self.ip, port= self.port)
            self.client = self.controller.get_client()
            self.is_connected = True
            self.io_set_mode_bcm()

    def io_set_mode_bcm(self):
        if self.__validate__():
            return self.client.send_subroutine_batch(fun_name())

    def config_digital_io(self, digital_in: [] = [], digital_out: [] = []):
        if self.__validate__():
            return self.client.send_subroutine_batch(fun_name(), arguments=[ digital_in, digital_out])

    def config_digital_output(self, pins):
        self.config_digital_io(digital_out=pins)

    def config_digital_input(self, pins):
        self.config_digital_io(digital_in= pins)

    def digital_out(self, pins=[], states=[]):
        if self.__validate__():
            return self.client.send_subroutine_batch(fun_name(), arguments=[pins, states])

    def digital_in(self, pins=[]):
        if self.__validate__():
            return self.client.send_subroutine_batch(fun_name(), arguments=[pins,])

    def set_digital_pin(self, pin:int, state:bool):
        self.digital_out([pin], [state])

    def read_digital_pin(self, pin:int):
        self.digital_out([pin], [pin])

    def config_pwm(self, pin_info:[]):# format [(pin, name, frequency), ...]
        if self.__validate__():
            for info in pin_info:
                assert( info[0].__class__ is int)
                assert (info[1].__class__ is str)
                assert (info[2].__class__ is int)
            self.config_digital_output([info[0] for info in pin_info])
            return self.client.send_subroutine_batch(fun_name(), arguments=[pin_info, ])

    def config_pwm_pin(self, pin:int, name:str, freq:int):
        self.config_pwm([(
            pin, name, freq
        )])

    def start_pwm(self, name:str, duty_cycle:int):
        if self.__validate__():
            self.client.send_subroutine_batch(fun_name(), arguments=[name, duty_cycle])

    def stop_pwm(self, name:str):
        if self.__validate__():
            self.client.send_subroutine_batch(fun_name(), arguments=[name,])

    def change_pwm(self, name, duty_cycle):
        if self.__validate__():
            self.client.send_subroutine_batch(fun_name(), arguments=[name, duty_cycle])

    def io_cleanup(self):
        if self.__validate__():
            self.client.send_subroutine_batch(fun_name())

    def stop(self, stop_listening= True):
        if stop_listening:
            self.client.close_handler()
            self.controller.close_gateway()
        else:
            self.client.close_handler()

if __name__ =='__main__':

    pi_ip = '192.168.0.106'
    pi_port = 1857
    rc = RC_client(pi_ip, pi_port)
    rc.connect()
    # safe_print('testing digital')
    # rc.config_digital_output([18,])
    # flag = False
    # for i in range(5):
    #     flag = not flag
    #     rc.set_digital_pin(18, flag)
    #     time.sleep(1)

    safe_print('testing pwm')
    rc.config_pwm_pin(18, 'pwm0',50)
    rc.start_pwm('pwm0', 0)

    # for i in range(5):
    #     for j in range(1,100,1):
    #         rc.change_pwm('pwm0', j)
    #         time.sleep(0.02)
    #     time.sleep(0.5)
    #     for j in range(100,0,-1):
    #         rc.change_pwm('pwm0', j)
    #         time.sleep(0.02)
    rc.change_pwm('pwm0', 30)
    time.sleep(2)

    rc.stop_pwm('pwm0')

    rc.io_cleanup()
    rc.stop(stop_listening= False)





