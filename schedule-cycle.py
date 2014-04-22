#!/usr/bin/env python3

import lifx
import argparse

import time
import sys
import threading

MENU_CHOICE_QUIT = 0
MENU_CHOICE_CHANGE_TIME_CYCLE = 1

isDone = False

def startUp():
    parser = argparse.ArgumentParser(description='Basic interactivity with a set of lights.')
    parser.add_argument('-l','--bulb-label',
                        help='bulb label(s) to perform against; sub/lazy match',
                        type=str,
                        nargs='+',
                        required=False)
    parser.add_argument('-t','--time-cycle',
                        help='amount of time in minutes to run cycle script',
                        type=float,
                        nargs=1,
                        required=False)
    parser.add_argument('-s','--cycle-speed',
                        help='amount of time in minutes between switch cycle per bulb',
                        type=float,
                        nargs=1)
    args = parser.parse_args()
    allArgs = args.bulb_label,args.time_cycle,args.cycle_speed
    return allArgs

def userMenu(timeCycle,cycleSpeed):
    print('\n------')
    print('To quit: {q}'.format(q=MENU_CHOICE_QUIT))
    if not timeCycle:
        print('To set time cycle script: {power_state}'.format(power_state=MENU_CHOICE_CHANGE_TIME_CYCLE))
    choice = input('> ')
    try:
        choice = int(choice)
    except ValueError:
        print('Please enter a value.')
        choice = userMenu()
    print('------\n')
    return choice

def timeCycleDriver(lightsCycle,minutes):
    if not isDone:
        print('{light} will go on, now for {time} minute(s); the rest in cycle will go off'.format(light=lightsCycle[0].bulb_label,time=minutes))
        for light in lightsCycle[1:]:
            light.set_power(False)
        lightsCycle[0].set_power(True)
        lightsCycle.append(lightsCycle[0])
        lightsCycle.remove(lightsCycle[0])
        timer = threading.Timer(minutes*60,timeCycleDriver,args=[lightsCycle,minutes])
        timer.start()

def driver(lightLabels,timeToCycle,cycleSpeed):
    choice = MENU_CHOICE_CHANGE_TIME_CYCLE
    if not lightLabels or not timeToCycle or not cycleSpeed:
        choice = userMenu()
    if choice == MENU_CHOICE_QUIT:
        quit
    else:
        lights = lifx.get_lights()
        lightsInCycle = []
        for light in lights:
            if lightLabels:
                for lightLabel in lightLabels:
                    if lightLabel in light.bulb_label:
                        if choice == MENU_CHOICE_CHANGE_TIME_CYCLE:
                            lightsInCycle.append(light)
            else:
                if choice == MENU_CHOICE_CHANGE_TIME_CYCLE:
                    lightsInCycle.append(light)
        timer = threading.Timer(timeToCycle*60,done,args=[lightsInCycle])
        timer.start()
        print(timer.isAlive())
        timeCycleDriver(lightsInCycle,cycleSpeed)

def done(lights):
    global isDone
    isDone = True
    for light in lights:
        light.set_power(False)
    sys.exit()
if __name__ == '__main__':
    lightLabels = timeToCycle = cycleSpeed = None
    rtnVal = startUp()
    if len(rtnVal):
        lightLabels = rtnVal[0]
        if len(rtnVal) > 1:
            timeToCycle = rtnVal[1][0]
            if len(rtnVal) > 2:
                cycleSpeed = rtnVal[2][0]
    
    driver(lightLabels,timeToCycle,cycleSpeed)
