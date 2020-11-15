import board.statusboard as sb
import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


# Define routes

# Static status endpoint for testing the server is up
@app.route('/status', methods=['GET'])
def status():
    return {'status': 'API running', 'args': sb.cmdargs}


# Run board self-test
@app.route('/test', methods=['POST'])
def test():
    return {'result': sb.test()}


# Get LED states
@app.route('/leds', methods=['GET'])
def get_leds():
    return {'leds': sb.get_leds()}


# Set LED states
@app.route('/leds', methods=['PUT'])
def set_all_leds():
    try:
        leds = flask.request.get_json()['leds']
        sb.set_leds({int(k): leds[k] for k in leds.keys()})
        return get_leds()
    except KeyError as error:
        return bad_request(error)


# Set LED states
@app.route('/leds', methods=['PATCH'])
def set_leds():
    try:
        leds = flask.request.get_json()['leds']
        sb.set_leds({int(k): leds[k] for k in leds.keys()}, merge=True)
        return get_leds()
    except KeyError as error:
        return bad_request(error)


@app.route('/leds/<pin>', methods=['GET'])
def get_led(pin):
    try:
        leds = sb.get_leds()
        led_key = int(pin)
        return {'pin': led_key, 'state': leds[led_key]}
    except (KeyError, ValueError):
        # Pin not found
        return not_found()


@app.route('/leds/<pin>', methods=['PUT'])
def set_led(pin):
    try:
        pin_key = int(pin)
        if pin_key not in sb.led_map:
            raise KeyError
    except (KeyError, ValueError):
        # Key not found or invalid
        return not_found()

    try:
        state = flask.request.get_json()['state']
        state_value = int(state)
        if state_value >= 1:
            sb.enable_leds(sb.led_map[pin_key])
        elif state_value == 0:
            sb.disable_leds(sb.led_map[pin_key])
        else:
            return bad_request()

        return get_led(pin)
    except (KeyError, ValueError) as error:
        # Key not in range
        return bad_request(error)


# Reset board
@app.route('/leds/reset', methods=['POST'])
def reset():
    sb.reset()
    return get_leds()


# Error handlers
@app.errorhandler(400)
def bad_request(error=None):
    app.logger.debug(error)
    return {'status': 400, 'message': 'Bad request'}, 400


@app.errorhandler(404)
def not_found():
    return {'status': 404, 'message': 'Not found'}, 404


@app.errorhandler(500)
def internal_error(error):
    app.logger.debug(error)
    return {'status': 500, 'message': error.description}, 500


# Start the server
try:
    app.run()
except IOError as e:
    app.logger.error(e)

# Tidy up on exit
sb.reset()
print('Bye bye')
