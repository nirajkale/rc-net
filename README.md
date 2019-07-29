# rc-net
## A use-case for pynetwork for raspberry pi based projects (Roboitics &amp; IOT)

This use case is based on pynetwork package ( https://github.com/nirajkale/pynetwork), which meant to handle your network workloads
by allowing you to stream your data to & from your python subroutines over the network.
For more information on pynetwork, head over to github page, make sure to get some basic info on the same before continuing on this
thread.

## Abstract

With packge like RPi, IO programming on raspberry pi has becomes a breeze as opposed to doing IO programming on hard-core 
microcontrollers like AVR-18 or something. But integrating it with a RC comm protocol has always been a painful part of any
robotics/IOT project. This is my attempt at simplyifying using pynetwork.

## Reasons for using pynetwork:

<img src="https://user-images.githubusercontent.com/40765055/62054690-bcae5d80-b237-11e9-8455-40e1b57487cf.png" /></p>

1. Quickly convert your local IO program to a wireless one by simply adding pynetwork in between the calls to your IO python
   functions.
2. Instead of reading/writing data to your python functions in batches, convert them to a generator functions & stream
   the data to your client asynchronously (no need poll these functions, just add callbacks) 
3. Parallize your network workload by spawning multiple clients from controller (check Github page for pynetwork for more     info)
4. Control Pi from multiple devices

# Project Hardware Setup:
You'll need below components to get started:
1. Raspberry Pi Zero ( or any other Pi board of your choice)
2. L293D based motor driver
You can either create one from scratch or buy one like this (https://www.amazon.in/L293D-Motor-Driver-Module-board/dp/B07FZ2GQ19/ref=sr_1_16?crid=2BMX8VDUE3AE&keywords=motor+driver&qid=1564410575&s=industrial&sprefix=motor+%2Cindustrial%2C506&sr=1-16 )
3. motors of your choice, a chasis & a battery as the motor requirement
4. Raspberry Pi camera (Optional)
BTW, make sure you buy appropriate cable for this camera, as cable type changes depending on which raspberry pi version you have.
5. A small powerbank for raspberry pi (or can use the same battery which you are using for motors)
6. Once you all the parts, connect your motor driver to raspberry pi
For more details check out this tutorial (https://www.instructables.com/id/DC-Motor-Control-With-Raspberry-Pi-and-L293D/)
Test if you are able to control these motors using Pi
7.Make sure to note down the pins you are using to connect with motor driver
In my case i used pins: 9, 10 (for left motor) 17, 27 (for right motor)
8. Connect your camera to raspberry pi

# Project Software Setup:

1. Install pyentwork on your laptop & raspberry pi:
```python
   pip install pynetwork
```
2. Copy rc_host.py on yotheur raspberry pi. You can either use scp or use tools like Filezilla (https://filezilla-project.org/download.php). Once the file is copied, ssh into your raspberry pi
```python
   ssh pi@YOUR-PI-IP-ADDRESS
```
Then navigate to the directory where rc_host.py is installed & start the host as below:
```python
   python3 rc_host.py
```
3. On your laptop, install pygame ( Required for UI)
```python
   pip install pygame
```
If you have used any other pins other than the onces mentioned in hardware setup, make sure change the code in ui.py
Also, make sure to update variable in rc_client.py file with ip address of your pi as below
```python
   pi_ip = 'YOUR.PI.IP.ADDRESS'
```
Then run the ui.py as:
```python
   python3 ui.py
```
Make sure rc_client.py is present in the same directory where ui.py is present.
4. Once the UI is started, you can use UP, DOWN, LEFT, RIGHT arrow keys to control robot.
Also, you can use CTRL + LEFT or CTRL + RIGHT to make hard turns

5. For live camera feed:
Open another ssh terminal for your pi & enter 

raspivid -t 999999 -h 450 -w 600 -fps 25 -hf -vf -b 2000000 -o - | gst-launch-1.0 -v fdsrc ! h264parse !  rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host=192.168.0.105 port=5000

& on your laptop, open another terminal & enter:

gst-launch-1.0 -v tcpclientsrc host=192.168.0.105 port=5000  ! gdpdepay !  rtph264depay ! avdec_h264 ! videoconvert ! autovideosink sync=false

Additionally, there are many android apps available which allow you to receive this stream via Gsftreamer:
for e.g. RaspberryPi Camera Viewer(Gstreamer)

Make sure to install gstreamer on both the devices. For more details checkout:
https://platypus-boats.readthedocs.io/en/latest/source/rpi/video/video-streaming-gstreamer.html 

# Code Walkthough:

This repo contains 3 files
 
1. rc_host.py
This is the python script that runs on the pi. it has a class RC_host which registers many GPIO functions 
from RPI library for IO programming.
for example, one of the functions being registered is 'digital_out', whcih allows, caller to set output of multiple digital pins of PI
```python
def __init__():
   self.gateway.add_subroutine('digital_out', self.digital_out)

# batch-data-send
def digital_out(self, pins=[], states=[]):
   safe_print('pins:', pins)
   safe_print('states:', states)
   for pin, state in zip(pins, states):
      GPIO.output(pin, state)
   return len(pinsavod
   
```
Once a function/ subroutine is registered with host, you can all the same function from client with same set of arguments. 
For more details checkout https://github.com/nirajkale/pynetwork

2. rc_client.py
This a layer that i have added on top of pynetwork controller to simplify my calls to the host from the UI. It is responsible to connect to the host & send data batches to appropriate functions when called.
For now i have added methods, to write to digital & pwm pins. i'll added more functionality to stream data from sensor (Live!) from a Ultrasonic sensor to the UI in few 1-2 days.

3. UI.py
A simple ( & ugly) UI built using pygame, to read arrow keystrokes from your keybaord & call appropriate 
function from rc_client.py Before launching UI, make sure to configure the IP address of your pi in the code.
Furthermore, your robot may not behave in sync with the keys that you are pressing. (For e.g. robot may go to right 
when you pressing the right key) To avoid this issue you need to configure a state dictionary in UI.py

```python
state_mapping= {
    'off':          [False,False,False,False],
    'forward':      [False,True,False,True],
    'backward':     [True,False,True,False],
    'hard-left':    [True,False,False,True],
    'hard-right':   [False,True,True,False],
    'left':         [False,False,False,True],
    'right':        [False,True,False,False],
}
```
Each boolean value in above array represent ON/OFF condition on pi's IO. In one array, first two values
are for one motor (or a pair of motors depending on design of your robot) & second two represent second motor.
In my case i used: 9, 10 (for left motor) 17, 27 (for right motor)
Setting values like (False,True) or (True, False) changes the direction of that motor.
In order to get the configuration right, you might have to do a bit trial & error. (It's still easy as this config is on 
client side (on your laptop) & no on ur pi, so that you don't have to replace your file again & again)


## Future work:

1. Adding a feature to read values from ultrasonic sensors mounted on my robot & gets it's value live stream on UI
2. replace mannually controlled UI with a Convolutional neural network that can see the live feed & control the robot.

If anyone is intrested in collaborating for the future work, contact me on nirajkale30@gmail.com or raise a pull request on 
either pynetwork or rc-net

happy coding!!
