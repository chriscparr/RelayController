import os
import hmac
import RPi.GPIO as GPIO
from hashlib import sha1
from flask import Flask, g, render_template, request, session
import flask_sijax

path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')

app = Flask(__name__)
app.config['SIJAX_STATIC_PATH'] = path
app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'
flask_sijax.Sijax(app)

@flask_sijax.route(app, '/')
def main():
    # Every Sijax handler function (like this one) receives at least
    # one parameter automatically, much like Python passes `self`
    # to object methods.
    # The `obj_response` parameter is the function's way of talking
    # back to the browser
    def say_hi(obj_response):
        obj_response.alert('Hi there!')

    if g.sijax.is_sijax_request:
        # Sijax request detected - let Sijax handle it
        g.sijax.register_callback('say_hi', say_hi)
        return g.sijax.process_request()

    # Regular (non-Sijax request) - render the page template
    return render_template('test_main.html')

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
	app.run(host='0.0.0.0', port=80, debug=True)

