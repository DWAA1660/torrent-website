from flask import Flask, jsonify, render_template, request, send_file, Response
import threading
import libtorrent as lt
from download_torrent import *
import cv2 as cv
from time import sleep
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    torrents = []
    for torrent in os.listdir("./static"):
        torrents.append(torrent)
    print(torrents)
    return render_template('index.html', torrents=torrents)
    
    
@app.route('/torrent_folder/<folder>', methods=['GET', 'POST'])
def torrent_folder(folder):
    paths = []
    files = os.listdir(f"./static/{folder}/")
    print(folder)

    for file in files:
        paths.append(f'{file}')

    print(paths)
    return render_template("folder_template.html", files=files, folder=folder)

@app.route('/torrent', methods=['GET', 'POST'])
def torrent():
    if request.method == 'POST':
        url = request.form['magnet_url']
        print(url)
        task_thread = threading.Thread(target=download_torrent, args=[url])
        task_thread.start()
        return f'Started downloading please give it some time'
    return render_template('form.html')

@app.route('/video_feed/<folder>/<filename>')
def video_feed(folder, filename):
    return render_template("video.html", folder=folder, filename=filename)
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=6969)
