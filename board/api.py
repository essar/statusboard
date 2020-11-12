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


# Reset board
@app.route('/leds/reset', methods=['POST'])
def reset():
    sb.reset()
    return get_leds()


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
    except KeyError:
        return bad_request()


# Set LED states
@app.route('/leds', methods=['PATCH'])
def set_leds():
    try:
        leds = flask.request.get_json()['leds']
        sb.set_leds({int(k): leds[k] for k in leds.keys()}, merge=True)
        return get_leds()
    except KeyError:
        return bad_request()


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


@app.route('/leds/<pin>', methods=['PUT'])
def set_led(pin):
    try:
        state = flask.request.get_json()['state']
        if state >= 1:
            sb.enable_leds(sb.led_map[int(pin)])
        elif state == 0:
            sb.disable_leds(sb.led_map[int(pin)])
        else:
            return bad_request()

        return get_led(pin)
    except KeyError:
        return bad_request()
    except ValueError:
        return not_found()


# Error handlers
@app.errorhandler(400)
def bad_request():
    return {'status': 400, 'message': 'Bad request'}, 400


@app.errorhandler(404)
def not_found():
    return {'status': 404, 'message': 'Not found'}, 404


@app.errorhandler(500)
def internal_error(error):
    return {'status': 500, 'message': error.description}, 500


# Start the server
app.run()
