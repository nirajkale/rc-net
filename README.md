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
Then run the ui.py as:
```python
   python3 ui.py
```
Make sure rc_client.py is present in the same directory where ui.py is present.
4. Once the UI is started, you can use UP, DOWN, LEFT, RIGHT arrow keys to control robot.
Also, you can use CTRL + LEFT or CTRL + RIGHT to make hard turns

# Code Walkthough:, RIGH

This repo contains 3 files
 
1. rc_host.py

