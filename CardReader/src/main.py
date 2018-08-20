# auth.py

# main.py 
# speaker climb

import time
import mfrc522
import machine
from os import uname

# plays the "access granted" sound
def access_granted(pwm_obj):
    pwm_obj.duty(50)

    freq_hi = 600
    freq_lo = 515
    pwm_obj.freq(freq_hi)
    time.sleep(0.1)

    pwm_obj.duty(0)
    time.sleep(0.4)

    pwm_obj.duty(50)

    pwm_obj.freq(freq_lo)
    time.sleep(0.1)
    pwm_obj.freq(freq_hi)
    time.sleep(0.2)

    pwm_obj.duty(0)

# plays the "access denied sound"
def access_denied(pwm_obj):

    pwm_obj.duty(50)

    freq_hi = 600
    freq_lo = 515
    pwm_obj.freq(freq_hi)
    time.sleep(0.1)
    pwm_obj.duty(0)
    time.sleep(0.2)

    pwm_obj.duty(50)
    for i in range(8):
        pwm_obj.freq(freq_lo)
        freq_lo -= 20
        time.sleep(0.12)

    time.sleep(0.6)
    pwm_obj.duty(0)

# function that returns a pwm object on the specified pin
# used for quick debugging and testing of code
def get_pwm(pin=5):
	return machine.PWM(machine.Pin(pin, machine.Pin.OUT))


# based on wendler's rc522 library for micropython
# https://github.com/wendlers/micropython-mfrc522
# specifically from examples/read.py
# checks uid
def access_loop():

	# hard coded uid match
	match = 'a5e82c22'

	if uname()[0] == 'WiPy':
		rdr = mfrc522.MFRC522("GP14", "GP16", "GP15", "GP22", "GP17")
	elif uname()[0] == 'esp8266':
		rdr = mfrc522.MFRC522(14, 13, 12, 4, 15)
	else:
		raise RuntimeError("Unsupported platform")

	print("")
	print("Access")
	print("")

	try:
		while True:

			(stat, tag_type) = rdr.request(rdr.REQIDL)

			if stat == rdr.OK:

				(stat, raw_uid) = rdr.anticoll()



				if stat == rdr.OK:

					uid = "%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])

					print("Card detected")
					print("  - tag type: 0x%02x" % tag_type)
					# print("  - uid	 : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
					# print("")

					if uid == match:
						print('Access granted.')
						access_granted(machine.PWM(machine.Pin(5, machine.Pin.OUT)))
						print()
					else:
						print('Access denied.')
						access_denied(machine.PWM(machine.Pin(5, machine.Pin.OUT)))
						print()

                    

					# if rdr.select_tag(raw_uid) == rdr.OK:

					# 	key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
					# 	# key = [0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]

					# 	if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
					# 		print("Address 8 data: %s" % rdr.read(8))
					# 		rdr.stop_crypto1()
					# 	else:
					# 		print("Authentication error")
					# else:
					# 	print("Failed to select tag")

	except KeyboardInterrupt:
		print("Bye")