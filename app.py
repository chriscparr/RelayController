'''

Adapted excerpt from Getting Started with Raspberry Pi by Matt Richardson

Modified by Rui Santos
Complete project details: http://randomnerdtutorials.com
                                                                                                                         
'''                                                                                                                      
                                                                                                                         
import RPi.GPIO as GPIO                                                                                                  
from flask import Flask, render_template, request                                                                        
app = Flask(__name__)                                                                                                    

GPIO.setmode(GPIO.BCM)

latches = {
    0 : {'name' : 'Latch0', 'A2' : 'false', 'A1' : 'false', 'A0' : 'false'},
    1 : {'name' : 'Latch1', 'A2' : 'false', 'A1' : 'false', 'A0' : 'true'},
    2 : {'name' : 'Latch2', 'A2' : 'false', 'A1' : 'true', 'A0' : 'false'},
    3 : {'name' : 'Latch3', 'A2' : 'false', 'A1' : 'true', 'A0' : 'true'},
    4 : {'name' : 'Latch4', 'A2' : 'true', 'A1' : 'false', 'A0' : 'false'},
    5 : {'name' : 'Latch5', 'A2' : 'true', 'A1' : 'false', 'A0' : 'true'},
    6 : {'name' : 'Latch6', 'A2' : 'true', 'A1' : 'true', 'A0' : 'false'},
    7 : {'name' : 'Latch7', 'A2' : 'true', 'A1' : 'true', 'A0' : 'true'}    
    }

GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)
GPIO.setup(22, GPIO.OUT)
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
    GPIO.output(17, GPIO.HIGH)
    # Convert the latch from the URL into an integer:
    changeLatch = int(changeLatch)
    # Get the device name for the latch being changed:
    deviceName = latches[changeLatch]['name']
    
    if latches[changeLatch]['A0'] == 'true':
        GPIO.output(23, GPIO.HIGH)
    if latches[changeLatch]['A0'] == 'false':
        GPIO.output(23, GPIO.LOW)
    if latches[changeLatch]['A1'] == 'true':
        GPIO.output(24, GPIO.HIGH)
    if latches[changeLatch]['A1'] == 'false':
        GPIO.output(24, GPIO.LOW)
    if latches[changeLatch]['A0'] == 'true':
        GPIO.output(25, GPIO.HIGH)
    if latches[changeLatch]['A0'] == 'false':
        GPIO.output(25, GPIO.LOW)   
   
    if action == "on":
        GPIO.output(22, GPIO.HIGH)
        GPIO.output(17, GPIO.LOW) #change mode to addressable latch
        # Save the status message to be passed into the template:
        message = "Turned " + deviceName + " on."
    if action == "off":
        GPIO.output(22, GPIO.LOW)
        GPIO.output(17, GPIO.LOW) #change mode to addressable latch
        message = "Turned " + deviceName + " off."
        
    GPIO.output(17, GPIO.HIGH) #change mode to memory to ignore input

    # Along with the latch dictionary, put the message into the template data dictionary:
    templateData = {
        'latches' : latches
        }

    return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
