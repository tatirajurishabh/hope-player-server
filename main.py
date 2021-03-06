from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import waitress
import bl


app = Flask(__name__, static_folder='static', static_url_path='')
caching_config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["60 per minute"],
)
app.config.from_mapping(caching_config)
cache = Cache(app)
CORS(app)


@app.route('/library')
def get_library():
    return jsonify(bl.get_library()), 200


@app.route('/stream')
def get_stream_url():
    song_id = request.args.get('id', None)
    quality = request.args.get('quality', 'high').lower()

    if song_id is not None:
        result = bl.get_stream_url(song_id, quality)
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


@app.route('/edit', methods=['PUT'])
def edit_song():
    if request.is_json:
        result = bl.edit_song(request.json)
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


@app.route('/artists')
def get_artists():
    result = bl.get_artists()
    return jsonify(result), result['code']


@app.route('/lyrics')
def get_lyrics():
    song_id = request.args.get('id', None)
    if song_id is not None:
        result = bl.get_lyrics(song_id)
        return jsonify(result), result['code']
    else:
        return jsonify({'code': 400, 'msg': 'No Song ID provided'}), 400


@app.route('/library/export')
def export_library():
    result = bl.export_library()
    return jsonify(result), result['code']


@app.route('/library/import', methods=['POST'])
def import_library():
    playlist_file = request.files.get('file', None)
    if playlist_file is not None:
        result = bl.import_library(playlist_file)
        return jsonify(result), result['code']
    else:
        return jsonify({'code': 400, 'msg': 'No import file provided'}), 400


@app.route('/artists/image')
@limiter.exempt
def get_artist_image():
    artist_name = request.args.get('name', None)
    if artist_name is not None:
        result = bl.get_artist_image(artist_name)
        return app.send_static_file(result)
    else:
        return ''


@app.route('/library/liked')
def get_liked_songs():
    return jsonify(bl.get_liked_songs()), 200


@app.route('/like', methods=['POST'])
def like_song():
    song_id = request.args.get('id', None)
    if song_id is not None:
        result = bl.like_unlike_song(song_id, True)
        return jsonify(result), result['code']
    else:
        return jsonify({'code': 400, 'msg': 'No Song ID provided'}), 400


@app.route('/unlike', methods=['POST'])
def unlike_song():
    song_id = request.args.get('id', None)
    if song_id is not None:
        result = bl.like_unlike_song(song_id, False)
        return jsonify(result), result['code']
    else:
        return jsonify({'code': 400, 'msg': 'No Song ID provided'}), 400


if __name__ == '__main__':
    waitress.serve(app, host='0.0.0.0', port=7474, threads=4)
