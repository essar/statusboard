import board.statusboard as sb
import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


# Define routes

# Static status endpoint for testing the server is up
@app.route('/status', methods=['GET'])
def status():
    return {'status': 'API running'}


# Get LED states
@app.route('/leds', methods=['GET'])
def get_leds():
    return {'leds': sb.get_leds()}


@app.route('/leds/<pin>', methods=['GET'])
def get_led(pin):
    try:
        leds = sb.get_leds()

        led_key = int(pin)
        return {'pin': led_key, 'state': leds[led_key]}

    except KeyError:
        # Key not in range
        return not_found()
    except ValueError:
        # Pin not numeric
        return not_found()


# Error handlers
@app.errorhandler(404)
def not_found():
    return {'status': 404, 'message': 'Not found'}, 404


@app.errorhandler(500)
def internal_error(error):
    return {'status': 500, 'message': error.description}, 500


# Start the server
app.run()
