# main.py 
# speaker climb

import time


def climb(pwm_obj):
    """Ascending frequency sweep from 0 to 1023 Hz.
    Each step occurs every 25 ms

    Arguments:
        pwm_obj {machine.PWM} -- The initialised PWM object that controls the speaker. (machine.PWM(pin))
    """

    # 50% duty cycle for the pwm
    pwm_obj.duty(50)

    i = 0
    while i < 1023:
        pwm_obj.freq(i)
        
        if i < 512:
            i += 1
        else:
            i += 2
        
        time.sleep(0.025)
    
    # silence the speaker
    pwm_obj.duty(0)

def climb_down(pwm_obj):
    """Descending frequency sweet from 1023 to 0 Hz.
    Each step occurs every 25 ms
    
    Arguments:
        pwm_obj {machine.PWM} -- The initialised PWM object that controls the speaker. (machine.PWM(pin))
    """
    
    # 50% duty cycle for the pwm
    pwm_obj.duty(50)

    i = 1023
    while i > 0:
        pwm_obj.freq(i)
        if i < 512:
            i -= 1
        else:
            i -= 2
            
        time.sleep(0.025)

    # silence the speaker
    pwm_obj.duty(0)


def heart_beat(pwm_obj, rate=55):
    """Attempts to simulate a heart beat monitor sound with a specified heart rate.
    
    Arguments:
        pwm_obj {machine.PWM} -- The initialised PWM object that controls the speaker. (machine.PWM(pin))
    
    Keyword Arguments:
        rate {int} -- The rate in beats per minute at which the heart should beat (default: {55})
    """

    # 50% duty cycle for the pwm
    pwm_obj.duty(50)
    
    N_HEARTBEATS = 6
    for _ in range(N_HEARTBEATS):
        pwm_obj.duty(50)
        pwm_obj.freq(960)
        time.sleep(0.1)
        pwm_obj.duty(0)
        time.sleep(60/rate)

    # flatline sound
    pwm_obj.freq(960)
    pwm_obj.duty(50)
    time.sleep(2.5)

    # silence the speaker
    pwm_obj.duty(0)


def alarm(pwm_obj):
    """Simulates an alarm type sound. Repeats 10 times
    
    Arguments:
        pwm_obj {machine.PWM} -- The initialised PWM object that controls the speaker. (machine.PWM(pin))
    """

    pwm_obj.duty(50)

    for i in range(10):
        freq = 450

        # climb up
        while freq < 960:
            freq += int(0.05*freq)
            pwm_obj.freq(freq)
            time.sleep(0.02)
        
        # climb down
        while freq > 450:
            freq -= int(0.05*freq)
            pwm_obj.freq(freq)
            time.sleep(0.02)

    # silence the speaker
    pwm_obj.duty(0)

# function that returns a pwm object on the specified pin
# used for quick debugging and testing of code
def get_pwm(pin=5):
    import machine
    return machine.PWM(machine.Pin(pin, machine.Pin.OUT))
