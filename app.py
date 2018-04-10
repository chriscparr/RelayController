#Pin17 = !G
#Pin22 = D
#Pin23 = A0
#Pin24 = A1
#Pin25 = A2

import os
import hmac
import RPi.GPIO as GPIO
import flask_sijax
from hashlib import sha1
from flask import Flask, g, render_template, abort, request, session
from werkzeug.security import safe_str_cmp

path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')

app = Flask(__name__)
app.secret_key = os.urandom(128)
app.config['SIJAX_STATIC_PATH'] = path
app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'
flask_sijax.Sijax(app)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

latches = {
	0 : {'name' : 'All'},
	1 : {'name' : 'ScreenL'},
	2 : {'name' : 'Unused'},
	3 : {'name' : 'ScreenR'},
	4 : {'name' : 'Down Light'}
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
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)


@flask_sijax.route(app, '/')
def main():

	def setLatch(obj_response, latchNum, action):
		if latchNum == 0:
			for key in latches[1:]:
				applyLatchAction(key, action)
		else:
			applyLatchAction(latchNum, action)

	if g.sijax.is_sijax_request:
		# Sijax request detected - let Sijax handle it
		g.sijax.register_callback('setLatch', setLatch)
		return g.sijax.process_request()

	# Put the pin dictionary into the template data dictionary:
	templateData = {
		'latches' : latches
	}
	# Regular (non-Sijax request) - render the page template
	return render_template('main.html', **templateData)

def setAddress(latchNumber):
	setOutput(17, True) #change mode to memory to ignore input
	setOutput(23, addresses[latchNumber][0])
	setOutput(24, addresses[latchNumber][1])
	setOutput(25, addresses[latchNumber][2])

def applyLatchAction(latchNum, action):
	setOutput(17, True) #change mode to memory to ignore input
	setAddress(latchNum)
	setOutput(17, False) #change mode to addressable latch
	if action == "off":
		setOutput(22, False)
		setOutput(22, True)
		#obj_response.alert("Turning latch %s off." % (latchNum))
	if action == "on":
		setOutput(22, False)
		#obj_response.alert("Turning latch %s on." % (latchNum))
	setOutput(17, True) #change mode to memory to ignore input

def setOutput(pinNumber, isHigh):
	if isHigh == True:
		GPIO.output(pinNumber, GPIO.HIGH)
	if isHigh == False:
		GPIO.output(pinNumber, GPIO.LOW)

@app.template_global('csrf_token')
def csrf_token():
    """
    Generate a token string from bytes arrays. The token in the session is user
    specific.
    """
    if "_csrf_token" not in session:
        session["_csrf_token"] = os.urandom(128)
    
    return hmac.new(app.secret_key, session["_csrf_token"], digestmod=sha1).hexdigest()

@app.before_request
def check_csrf_token():
    """Checks that token is correct, aborting if not"""
    if request.method in ("GET",): # not exhaustive list
        return
    token = request.form.get("csrf_token")
    if token is None:
        app.logger.warning("Expected CSRF Token: not present")
        abort(400)
    if not safe_str_cmp(token, csrf_token()):
        app.logger.warning("CSRF Token incorrect")
        abort(400)



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
