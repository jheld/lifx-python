#!/usr/bin/env python3

import lifx
import argparse

MENU_CHOICE_QUIT = 0
MENU_CHOICE_CHANGE_POWER_STATE = 1


def startUp():
    parser = argparse.ArgumentParser(description='Basic interactivity with a set of lights.')
    parser.add_argument('-l','--bulb-label',
                        help='bulb label(s) to perform against; sub/lazy match',
                        type=str,
                        nargs='+',
                        required=False)
    args = parser.parse_args()
    allArgs = args.bulb_label
    return allArgs

def userMenu():
    print('\n------')
    print('To quit: {q}'.format(q=MENU_CHOICE_QUIT))
    print('To change power state: {power_state}'.format(power_state=MENU_CHOICE_CHANGE_POWER_STATE))
    choice = input('Choice: ')
    try:
        choice = int(choice)
    except ValueError:
        print('Please enter a value.')
        choice = userMenu()
    print('------\n')
    return choice

def powerStateDriver(light):
    print('Adjust for light w/label: {label}'.format(label=light.bulb_label))
    print('Power State\n------------')
    print('1/on')
    print('0/off')
    desiredPowerState = input('> ')
    skipSettingPower = False
    if len(desiredPowerState):
        try:
            if int(desiredPowerState):
                desiredPowerState = True
            else:
                desiredPowerState = False
        except ValueError:
            if 'on' in desiredPowerState.lower():
                desiredPowerState = True
            elif 'off' in desiredPowerState.lower():
                desiredPowerState = False
            else:
                print('Skipping this light\'s power state management.')
                skipSettingPower = True
        if desiredPowerState != light.power and not skipSettingPower:
            light.set_power(desiredPowerState)
    else:
        print('Skipping this light\'s power state management.')

def driver(lightLabels):
    choice = userMenu()
    if choice == MENU_CHOICE_QUIT:
        quit
    else:
        lights = lifx.get_lights()
        for light in lights:
            if lightLabels:
                for lightLabel in lightLabels:
                    if lightLabel in light.bulb_label:
                        if choice == MENU_CHOICE_CHANGE_POWER_STATE:
                            powerStateDriver(light)
            else:
                if choice == MENU_CHOICE_CHANGE_POWER_STATE:
                    powerStateDriver(light)
        driver(lightLabels)
if __name__ == '__main__':
    lightLabels = startUp()
    driver(lightLabels)
