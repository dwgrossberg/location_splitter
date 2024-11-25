from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask.helpers import send_from_directory
import re


class Config:
    SCHEDULER_API_ENABLED = True


app = Flask(__name__, static_folder='frontend', static_url_path='')
app.config.from_object(Config())


CORS(app)


def split_locations(locations):
    if 'locations' in locations:
        idx = locations.index('locations')
        locations = locations[idx+9:]
    split = [s for s in re.split('(?<=[A-Z]{2})(?=[A-Z])', locations) if s]
    return '\n'.join(split)


@app.route('/splitter', methods=['POST'])
@cross_origin()
def split():
    data = request.get_json()
    for post in data:
        post[3] = split_locations(post[2])
    return jsonify(data)


@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run()
