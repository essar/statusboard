import flask
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/status', methods=['GET'])
def home():
    return json.dumps({'status': 'API running'})


app.run()
