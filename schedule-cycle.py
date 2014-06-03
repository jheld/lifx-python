#!/usr/bin/env python3

import lifx

import argparse
import time
import sys
import os
import threading

class ScheduleCycle():
    def __init__(self):
        super().__init__()
        self.configuration = {}
    def addConfiguration(self, lights, time, speed):
        bulbLabels = []
        for light in lights:
            bulbLabels.append(light.bulb_label)
        bulbLabels = sorted(bulbLabels)
        bulbLabels = str(bulbLabels)
        configuration = None
        if not bulbLabels in self.configuration.keys():
            self.configuration[bulbLabels] = {}
            self.configuration[bulbLabels]['lights'] = lights
            self.configuration[bulbLabels]['speed'] = speed
            self.configuration[bulbLabels]['time'] = time
            self.configuration[bulbLabels]['isDone'] = False
            configuration = bulbLabels
        return configuration
    def timeCycleDriver(self,key):
        lights = []
        if key in self.configuration.keys():
            lights = self.configuration[key]['lights']
        if lights and len(lights) > 1:
            if not self.configuration[key]['isDone']:
                speed = self.configuration[key]['speed']
                minutes = float(abs(speed))
                print('unixTime: {utime}-->{light} will go on, now for {time} minute(s); the rest in cycle will go off'.format(utime=time.time(),light=lights[0].bulb_label,time=minutes))
                lights[0].set_power(True)
                for light in lights[1:]:
                    light.set_power(False)
                with open('cycle_report.txt', 'a') as myfile:
                    myfile.write('light {lighton} is now on at unixTime: {utime}\n'.format(lighton=lights[0].bulb_label,utime=time.time()))
                lights.append(lights[0])
                lights.remove(lights[0])
                self.configuration[key]['lights'] = lights
                timer = threading.Timer(minutes*60,self.timeCycleDriver,args=[key])
                timer.start()
            else:
                for light in lights:
                    light.set_power(False)
                self.configuration.pop(key)
    def driver(self,lightsInCycle,timeToCycle,cycleSpeed):
        key = self.addConfiguration(lightsInCycle,timeToCycle,cycleSpeed)
        if key:
            callDoneInSeconds = self.configuration[key]['time']
            timer = threading.Timer(callDoneInSeconds*60,self.done,args=[key])
            timer.start()
            self.timeCycleDriver(key)

    def done(self,key):
        self.configuration[key]['isDone'] = True
        self.timeCycleDriver(key)
    
def startUp():
    parser = argparse.ArgumentParser(description='Simple lights on/off cycling through a list of bulbs.')
    parser.add_argument('-l','--label-bulb',
                        help='bulb label(s) to perform against; sub/lazy match',
                        type=str,
                        nargs='+',
                        required=False)
    parser.add_argument('-t','--time-run',
                        help='amount of time in minutes to run cycle script',
                        type=float,
                        nargs=1,
                        required=False)
    parser.add_argument('-s','--speed-cycle',
                        help='amount of time in minutes between switch cycle per bulb',
                        type=float,
                        nargs=1)
    args = parser.parse_args()
    return vars(args)

if __name__ == '__main__':
    lightLabels = []
    timeToCycle = cycleSpeed = None
    rtnArgs = startUp()
    lightsToUseBasedOnLabels = []
    if rtnArgs.get('label_bulb'):
        lightLabels = rtnArgs['label_bulb']
        lights = lifx.get_lights()
        lightLabelsToUseBasedOnLabels = []
        for light in lights:
            for lightLabel in lightLabels:
                if lightLabel in light.bulb_label:
                    lightsToUseBasedOnLabels.append(light)
                    lightLabelsToUseBasedOnLabels.append(light.bulb_label)
        if len(lightsToUseBasedOnLabels) < 2:
            print('Not at least 2 lights for cycle script to run. Use different labels')
            sys.exit(0)
        else:
            lightLabels = lightLabelsToUseBasedOnLabels
    else:
        while not lightLabels or len(lightLabels) < 2:
            lights = lifx.get_lights()
            print('\n/---------------/')
            labelsAskedInLoop = []
            for light in lights:
                if len(lightLabels):
                    for lightLabel in lightLabels:
                        if light.bulb_label not in labelsAskedInLoop:
                            labelsAskedInLoop.append(light.bulb_label)
                            # only add in distinct, non-added light labels
                            if lightLabel not in light.bulb_label:
                                userChoice  = input('Use {light_label} in cycle: '.format(light_label=light.bulb_label))
                                if (userChoice.isdigit() and int(userChoice) == 1) or userChoice.lower() == 'yes' or userChoice.lower() == 'y':
                                    lightLabels.append(light.bulb_label)
                                    lightsToUseBasedOnLabels.append(light)
                        else:
                            continue
                else:
                    userChoice  = input('Use {light_label} in cycle: '.format(light_label=light.bulb_label))
                    if userChoice and (userChoice.isdigit() and int(userChoice) == 1) or userChoice.lower() == 'yes' or userChoice.lower() == 'y':
                        lightLabels.append(light.bulb_label)
                        lightsToUseBasedOnLabels.append(light)
            if len(lightLabels) == 1:
                print('There have to be at least two bulbs for the cycle execution.')  
            print('/---------------/\n')
    if rtnArgs.get('time_run') and len(rtnArgs['time_run']):
        timeToCycle = rtnArgs['time_run'][0]
    else:
        while not timeToCycle:
            userChoice = input('Minutes for script run: ')
            try:
                userChoice = abs(float(userChoice))
                timeToCycle = userChoice
            except ValueError:
                print('Invalid minutes to run script for. Try again')
    if rtnArgs.get('speed_cycle') and len(rtnArgs['speed_cycle']):
        cycleSpeed = rtnArgs['speed_cycle'][0]
    else:
        while not cycleSpeed:
            userChoice = input('Minutes for each cycle: ')
            try:
                userChoice = abs(float(userChoice))
                cycleSpeed = userChoice
            except ValueError:
                print('Invalid minutes for each cycle. Try again')
    scheduleCycle = ScheduleCycle()
    scheduleCycle.driver(lightsToUseBasedOnLabels,timeToCycle,cycleSpeed)
