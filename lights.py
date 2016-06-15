import subprocess
import socket
import paho.mqtt.client as mqtt

code_dict = {	"lights/kitchen": 	{"on": "000000000001000101010001", "off": "000000000001000101010100"},
				"lights/room-middle":	{"on": "000000000000010101010001", "off": "000000000000010101010100"},
				"lights/thomas":	{"on": "000000000001010001010001", "off": "000000000001010001010100"},
				"lights/room-left":	{"on": "000000000001010100010001", "off": "000000000001010100010100"}
			}

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("lights/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	topic = str(msg.topic)
	payload = msg.payload.decode(encoding='UTF-8')
	send_multiple_codes(payload) if (topic == "lights/all") else send_code(topic, payload)

def send_code(topic, payload):
	if payload == "on" or "off":
		try:
			subprocess.Popen("python sender.py " + code_dict[topic][payload], shell = True)
		except KeyError:
			pass

def send_multiple_codes(payload):
	subprocess.Popen(["python", "sender.py"] + get_multiple_codes("off"))

def get_multiple_codes(payload):
	codes = []
	for value in code_dict.values():
		codes.append(value[payload])
	return codes

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(socket.gethostbyname(socket.gethostname()), 1883, 60)
client.loop_forever()
