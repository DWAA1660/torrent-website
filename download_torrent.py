import time
import string
import random
import os
import shutil
import libtorrent as lt

def generate_id():
    id = ""
    for i in range(18):
        char = random.choice(string.ascii_letters + string.digits)
        id = id + char
    return id

def download_torrent(url):
    id = generate_id()
    ses = lt.session()
    ses.listen_on(6881, 6891)

    # add the torrent file
    params = {"save_path": f"./pending_torents/{id}"}
    torrent = lt.add_magnet_uri(ses, url, params)

    while(not torrent.has_metadata()):
        time.sleep(1)

    NAME = torrent.get_torrent_info().name()
    
    # start the torrent download
    ses.start_dht()
    while (not torrent.is_seed()):
        s = torrent.status()
        print(f"\rDownloading... {s.progress * 100:.2f}% complete (down: {s.download_rate/1000:.1f} kB/s | up: {s.upload_rate/1000:.1f} kB/s | peers: {s.num_peers})", end="")
        
        # wait for a short time before checking again
        time.sleep(1)

    os.mkdir(f"./static/{NAME}")
    for file in os.listdir(f'./pending_torents/{id}'):
        file_path = os.path.join(f'./pending_torents/{id}', file)

    # Move the file to the destination directory
        shutil.move(file_path, f"./static/{NAME}")
    os.rmdir(f"./pending_torents/{id}")
    print("\nDownload complete!")

