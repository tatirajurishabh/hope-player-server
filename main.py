from flask import Flask, jsonify, request
from flask_cors import CORS
import waitress
import bl

app = Flask(__name__)
CORS(app)


@app.route('/library')
def get_library():
    return jsonify(bl.get_library()), 200


@app.route('/stream')
def get_stream_url():
    song_id = request.args.get('id', None)
    if song_id is not None:
        result = bl.get_stream_url(song_id)
        return jsonify(result), result['code']
    else:
        return jsonify({'code': 400, 'msg': 'No Song ID provided'}), 400


@app.route('/add', methods=['POST'])
def add_song():
    if request.is_json:
        result = bl.add_song(request.json)
        return jsonify(result), result['code']
    else:
        return jsonify({'code': 400, 'msg': 'No data provided'}), 400


@app.route('/delete', methods=['DELETE'])
def delete_song():
    song_id = request.args.get('id', None)
    if song_id is not None:
        result = bl.delete_song(song_id)
        return jsonify(result), result['code']
    else:
        return jsonify({'code': 400, 'msg': 'No Song ID provided'}), 400


if __name__ == '__main__':
    waitress.serve(app, host='0.0.0.0', port=7474)
