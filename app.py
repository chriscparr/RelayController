'''

Adapted excerpt from Getting Started with Raspberry Pi by Matt Richardson

Modified by Rui Santos
Complete project details: http://randomnerdtutorials.com
																														 
'''

#Pin17 = !G
#Pin22 = D
#Pin23 = A0
#Pin24 = A1
#Pin25 = A2                                                                                                                      
																														 
import RPi.GPIO as GPIO                                                                                                  
from flask import Flask, render_template, request                                                                        
app = Flask(__name__)                                                                                                    

GPIO.setmode(GPIO.BCM)

latches = {
	0 : {'name' : 'Down Light', 'A2' : 'false', 'A1' : 'false', 'A0' : 'false'},
	1 : {'name' : 'ScreenL', 'A2' : 'false', 'A1' : 'false', 'A0' : 'true'},
	2 : {'name' : 'Unused', 'A2' : 'false', 'A1' : 'true', 'A0' : 'false'},
	3 : {'name' : 'ScreenR', 'A2' : 'false', 'A1' : 'true', 'A0' : 'true'},
	4 : {'name' : 'Latch4', 'A2' : 'true', 'A1' : 'false', 'A0' : 'false'},
	5 : {'name' : 'Latch5', 'A2' : 'true', 'A1' : 'false', 'A0' : 'true'},
	6 : {'name' : 'Latch6', 'A2' : 'true', 'A1' : 'true', 'A0' : 'false'},
	7 : {'name' : 'Latch7', 'A2' : 'true', 'A1' : 'true', 'A0' : 'true'}
	}

addresses = [
	(False, False, False),
	(True, False, False),
	(False, True, False),
	(True, True, False),
	(False, False, True),
	(True, False, True),
	(False, True, True),
	(True, True, True)
]

GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)
GPIO.setup(22, GPIO.OUT)
#GPIO.output(22, GPIO.HIGH)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)


@app.route("/")
def main():
	# Put the pin dictionary into the template data dictionary:
	templateData = {
		'latches' : latches
	}
	# Pass the template data into the template main.html and return it to the user
	return render_template('main.html', **templateData)


# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changeLatch>/<action>")
def action(changeLatch, action):
	setOutput(17, True) #change mode to memory to ignore input
	# Convert the latch from the URL into an integer:
	changeLatch = int(changeLatch)
	# Get the device name for the latch being changed:
	deviceName = latches[changeLatch]['name']
	
	setAddress(changeLatch)

	setOutput(17, False) #change mode to addressable latch

	if action == "off":
		setOutput(22, False)
		setOutput(22, True)
		message = "Turned " + deviceName + " off."
	if action == "on":
		setOutput(22, False)
		message = "Turned " + deviceName + " on."

	setOutput(17, True) #change mode to memory to ignore input

	# Along with the latch dictionary, put the message into the template data dictionary:
	templateData = {
		'latches' : latches
		}

	return render_template('main.html', **templateData)

def setAddress(latchNumber):
	setOutput(17, True) #change mode to memory to ignore input
	setOutput(23, addresses[latchNumber][0])
	setOutput(24, addresses[latchNumber][1])
	setOutput(25, addresses[latchNumber][2])

def setOutput(pinNumber, isHigh):
	if isHigh == True:
		GPIO.output(pinNumber, GPIO.HIGH)
	if isHigh == False:
		GPIO.output(pinNumber, GPIO.LOW)

if __name__ == "__main__":
	try:
		app.run(host='0.0.0.0', port=80, debug=True)
	except KeyboardInterrupt:
		print "Excecution Cancelled"
	except:
		print "Some other exception occured!"
	finally:
		print "Cleaning up..."
		GPIO.cleanup()
