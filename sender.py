
# A on 		000000000000010101010001	Oliver
# A off 	000000000000010101010100
# B on 		000000000001000101010001	Kitchen
# B off 	000000000001000101010100
# C on 		000000000001010001010001	Thomas
# C off 	000000000001010001010100
# D on 		000000000001010100010001	Tobias
# D off 	000000000001010100010100

import sys
import time
import wiringpi

wiringpi.wiringPiSetupGpio()  
wiringpi.pinMode(17, 1) # sets GPIO 17 to output


sender = 17 # orange cabel
code_duration = 1275
sync_duration = 10400
code = ""


def send_sync():
	wiringpi.digitalWrite(sender, 1)
	wiringpi.delayMicroseconds(400)
	wiringpi.digitalWrite(sender, 0)
	wiringpi.delayMicroseconds(10000)


def send_digit(digit):
	if digit == "0":
		wiringpi.digitalWrite(sender, 1)
		wiringpi.delayMicroseconds(int(code_duration * 0.25))
		wiringpi.digitalWrite(sender, 0)
		wiringpi.delayMicroseconds(int(code_duration * 0.75))
	else:
		wiringpi.digitalWrite(sender, 1)
		wiringpi.delayMicroseconds(int(code_duration * 0.75))
		wiringpi.digitalWrite(sender, 0)
		wiringpi.delayMicroseconds(int(code_duration * 0.25))

def send_signal(code):
	send_sync()
	for c in code:
		send_digit(c)


def send_code(code):
	for i in range(0, 4):
		send_signal(code)

def main(code):
	send_code(code)

if __name__ == "__main__":
	for single_code in sys.argv[1:]: main(single_code) if (len(sys.argv) > 2) else main(sys.argv[1])

