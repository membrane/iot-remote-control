import time
import sys
import wiringpi

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(27, 0) # sets GPIO 27 to input  
#wiringpi.pinMode(17, 1) # sets GPIO 17 to output 

last = 0
last_high = 0
bits_to_output = 0
ones = 0
zeros = 0
code = ""

def calc_time():
	global last, last_high, bits_to_output, ones, zeros, code
	now = wiringpi.micros()
	diff = now - last
	if (diff > 40000 and diff < 42000):
		sys.stdout.write("\n")
		sys.stdout.write("\n\nwhole signal duration: " + str(now - last) + "")
		sys.stdout.write("  sync duration:" + str(now - last_high) + " ")
		if ones + zeros != 0:
			sys.stdout.write(" sync ones-ration:" + str(ones / (ones + zeros)) + " ")
		sys.stdout.write(" code duration:" + str((last_high - last) / 24) + "\n")
		bits_to_output = 24
		ones = 0
		zeros = 0
		code = ""
	last = now

def compress_string(string):
	compressed = ""; i = 0
	while i < len(string):
		pair = string[i] + string[i + 1]
		if pair == "00":
			compressed += "0"
		elif pair == "11":
			compressed += "1"
		elif pair == "01":
			compressed += "F"
		else:
			compressed = "non valid"
			break
		i += 2
	return compressed

def main():

	receiver = 27; sender = 1; state = 1; i = 0
	global last_high, ones, zeros, bits_to_output, code

	while True:
		wiringpi.delayMicroseconds(25)

		if wiringpi.digitalRead(receiver) == False:

			if (bits_to_output > 0):
				sys.stdout.write("0")
			zeros += 1
			
			if state < 80:
				state += 1
		else:
			if state >= 2 and bits_to_output > 0:
				bits_to_output -= 1
				#sys.stdout.write("\n")
				#sys.stdout.write(str(format(ones / (ones + zeros), '.2f')) + " ")
				#sys.stdout.write(str( (ones + zeros)) + " ")
				
				if ones / (ones + zeros) < 0.5:
					#sys.stdout.write("0")
					code += "0"
				else:
					#sys.stdout.write("1")
					code += "1"

				if bits_to_output == 0:
					sys.stdout.write("   " + code)
					sys.stdout.write("   " + compress_string(code))
				
				#sys.stdout.write(" --\n")
				ones = 0
				zeros = 0

			if state == 80:
				calc_time()
			
			if (bits_to_output > 0):
				sys.stdout.write("1")
			ones += 1
			

			if state >= 2:
				last_high = wiringpi.micros()

			state = 0

		i += 1
		if i == 40:
			sys.stdout.flush()
			i = 0

if __name__ == "__main__":
    main()
