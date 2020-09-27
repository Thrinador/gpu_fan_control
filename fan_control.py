# Simple gpu fan control script based loosly off of
# https://github.com/vandabbin/nvidia-fan-control-linux

import os
import time

# How long to wait in seconds before setting the gpu fan speed again.
sleepTime = 3

minTemp = 44
minFanSpeed = 35
maxTemp = 80
maxFanSpeed = 100

fanCurveSlope = 1.8
fanCurveYAxis = -44

# Enable maunal fan control for the gpus
def startUp():
    os.popen('nvidia-settings -a "GPUFanControlState=1"').read()


# Returns the current gpu temp.
def getGPUTemp():
    return int(
        os.popen("nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader").read()
    )


# Given gpu temp, return the percent speed the fans should be spinning at
def getFanSpeed(temp):
    if temp < minTemp:
        return minFanSpeed
    if temp > maxTemp:
        return maxFanSpeed
    # Make a linear line between the two extremes.
    newFanSpeed = round(fanCurveSlope * temp + fanCurveYAxis)
    if newFanSpeed > 100:
        return 100
    if newFanSpeed < 0:
        return 0
    return newFanSpeed


# Given a fan speed set the GPU to run at that speed.
def setFanSpeed(speed):
    os.popen('nvidia-settings -a "GPUTargetFanSpeed=%d"' % speed).read()


startUp()
while True:
    setFanSpeed(getFanSpeed(getGPUTemp()))
    time.sleep(sleepTime)
