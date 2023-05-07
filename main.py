from flask import Flask, jsonify, render_template, request
import threading
import libtorrent as lt
from download_torrent import *


app = Flask(__name__)

@app.route('/')
def index():
    torrents = []
    for torrent in os.listdir("./finished_torents"):
        torrents.append(torrent)
    print(torrents)
    return render_template('index.html', torrents=torrents)
    
    
@app.route('/torrent_folder/<folder>', methods=['GET', 'POST'])
def torrent_folder(folder):
    files = os.listdir(f"./finished_torents/{folder}")
    return render_template("folder_template.html", files=files)

@app.route('/torrent', methods=['GET', 'POST'])
def torrent():
    if request.method == 'POST':
        url = request.form['magnet_url']
        print(url)
        task_thread = threading.Thread(target=download_torrent, args=[url])
        task_thread.start()
        return f'Started downloading please give it some time'
    return render_template('form.html')


if __name__ == '__main__':
    app.run(debug=True)
