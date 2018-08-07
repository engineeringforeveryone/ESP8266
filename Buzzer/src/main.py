# main.py 
# speaker climb

import time

def climb(pwm_obj):
    pwm_obj.duty(50)
    
    
    i = 0
    while i < 1023:
        pwm_obj.freq(i)
        
        if i < 512:
            i += 1
        else:
            i += 2
        
        time.sleep(0.025)

def climb_down(pwm_obj):
    pwm_obj.duty(50)

    i = 1023
    while i > 0:
        pwm_obj.freq(i)
        if i < 512:
            i -= 1
        else:
            i -= 2
            
        time.sleep(0.025)

def heart_rate(pwm_obj, rate=55):
    pwm_obj.duty(50)
    
    for i in range(10):
        pwm_obj.duty(50)
        pwm_obj.freq(960)
        time.sleep(0.1)
        pwm_obj.duty(0)
        time.sleep(60/rate)

def alarm(pwm_obj):
    pwm_obj.duty(50)

    for i in range(2):
        freq = 450

        # climb up
        while freq < 960:
            freq += int(0.05*freq)
            pwm_obj.freq(freq)
            time.sleep(0.025)
        
        # climb down
        while freq > 450:
            freq -= int(0.05*freq)
            pwm_obj.freq(freq)
            time.sleep(0.025)

        

