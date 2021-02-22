import shutil
import os
from bing_image_downloader import downloader
import shutil
import os
import da


def get_valid_filename(name):
    return name.replace('&', 'and').replace('+', 'and')


def generate_artist_images():
    songs = [song.to_dict() for song in da.get_library()]
    artist_names = []
    for song in songs:
        name = get_valid_filename(song['artist'])
        if name not in artist_names:
            artist_names.append(name)

        base_save_path = 'static/artists/' + name
        if not os.path.exists(base_save_path):
            downloader.download(
                name, limit=1,  output_dir='bing_download_artists', adult_filter_off=False, force_replace=True, timeout=60)

            base_download_path = 'bing_download_artists/' + name + '/Image_1'
            if os.path.exists(base_download_path + '.jpg'):
                shutil.copyfile(base_download_path + '.jpg', base_save_path)
            elif os.path.exists(base_download_path + '.png'):
                shutil.copyfile(base_download_path + '.png', base_save_path)
            elif os.path.exists(base_download_path + '.jpeg'):
                shutil.copyfile(base_download_path + '.jpeg', base_save_path)
            else:
                pass

    shutil.rmtree('bing_download_artists', ignore_errors=True, onerror=None)


generate_artist_images()
