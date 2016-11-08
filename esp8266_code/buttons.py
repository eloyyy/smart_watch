# Button configurations
import time
import shared
from machine import PWM, Pin

# Debounce function
def wait_pin_change(pin):

    cur_value = pin.value()
    active = 0
    while active < 80:
        if pin.value() == cur_value:
            active += 1
        else:
            active = 0
            break
        time.sleep(0.001)
    return active

    # Define interrupts
def incrementB(p=0):

    # global B
    # global buttonB
    # active = wait_pin_change(buttonB)
    # if active >= 20:
    shared.B = shared.B+1



def incrementA(p=0):
    # global isHour
    # global A
    # global buttonA
    # active = wait_pin_change(buttonA)
    # if active >= 20:
    if shared.isHour:       
        if shared.A < 23:
            shared.A = shared.A+1
        else:
            shared.A = 0
    else:
        if shared.A < 59:
            shared.A = shared.A+1
        else:
            shared.A = 0      


def decrementA(p=0):
    # global buttonC
    # global isHour
    # global A
    # active = wait_pin_change(buttonC)
    # if active >= 20:
    if shared.isHour:       
        if shared.A > 0:
            shared.A = shared.A-1
        else:
            shared.A = 23
    else:
        if shared.A > 0:
            shared.A = shared.A-1
        else:
            shared.A = 59 

def alarm(current_time, alarm_var, display):
    if current_time['minute'] == alarm_var['minute'] and current_time['hour'] == alarm_var['hour'] and shared.isAlarm:
        display.fill(0)
        display.text('ALARM', 10, 10)
        display.show()
        for i in range(1, 800):
            pwm_piezo = PWM(Pin(15), freq=i, duty=512) 
            time.sleep(0.001)
        time.sleep(3)
        PWM(Pin(15), 0, 0)
        shared.isAlarm = False
        hour_alarm = None
        minutes_alarm = None
    display.fill(0)

def set_time(buttonA, buttonB, buttonC, display, alarm):
    while shared.B==0:
        display.text('Set up hour?', 10, 10)
        display.show()
        time.sleep(2)
    hour = 0
    shared.isHour = True

    while shared.B == 1:
        display.fill(0)
        display.show()
        time.sleep(0.5)    
        display.text('Hour = ' + str(hour), 10, 10)
        hour = shared.A
        display.show()
        time.sleep(0.5)

    shared.A = 0
    minutes = 0
    while shared.B == 2:
        shared.isHour = False
        display.fill(0)
        display.show()
        time.sleep(0.5)
        display.text('Minutes = ' + str(minutes), 10, 10)

        minutes = shared.A
        display.show()
        time.sleep(0.5)

    if not alarm:
        shared.A = 0
        seconds = 0
        while shared.B == 3:
            shared.isHour = False
            display.fill(0)
            display.show()
            time.sleep(0.5)
            display.text('Seconds = ' + str(seconds), 10, 10)
            seconds = shared.A
            display.show()
            time.sleep(0.5)
    else:
        seconds = None

    display.fill(0)
    res = dict()
    res['hour'] = hour
    res['minutes'] = minutes
    res['seconds'] = seconds
    return(res)
