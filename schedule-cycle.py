#!/usr/bin/env python3

import lifx
import argparse

import time
import sys
import threading

isDone = False

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

def timeCycleDriver(lightsCycle,minutes):
    global isDone
    if not isDone:
        print('{light} will go on, now for {time} minute(s); the rest in cycle will go off'.format(light=lightsCycle[0].bulb_label,time=minutes))
        lightsCycle[0].set_power(True)
        for light in lightsCycle[1:]:
            light.set_power(False)
        lightsCycle.append(lightsCycle[0])
        lightsCycle.remove(lightsCycle[0])
        timer = threading.Timer(minutes*60,timeCycleDriver,args=[lightsCycle,minutes])
        timer.start()

def driver(lightsInCycle,timeToCycle,cycleSpeed):
    timer = threading.Timer(timeToCycle*60,done,args=[lightsInCycle])
    timer.start()
    timeCycleDriver(lightsInCycle,cycleSpeed)

def done(lights):
    global isDone
    isDone = True
    for light in lights:
        light.set_power(False)
    sys.exit()
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
    driver(lightsToUseBasedOnLabels,timeToCycle,cycleSpeed)
