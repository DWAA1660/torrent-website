import time
import string
import random
import os
import shutil
import libtorrent as lt
import ffmpeg
import subprocess

def generate_id():
    id = ""
    for i in range(18):
        char = random.choice(string.ascii_letters + string.digits)
        id = id + char
    return id

def move_files_to_directory(id, NAME):
    destination_dir = f"./static/{NAME}"
    os.makedirs(destination_dir, exist_ok=True)
    print("test")
    source_dir = f"./pending_torents/{id}"
    print(source_dir)
    for thing in os.listdir(source_dir):
        print(thing, "MAINNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNn")
        file_path = os.path.join(source_dir, thing)
        if os.path.isfile(file_path):
            print(thing, 3333333333333333333333)
            file_to_move_path = os.path.join(destination_dir, thing)
            shutil.move(file_path, file_to_move_path)
        elif os.path.isdir(file_path):
            print(thing, "IS A DIR!")
            for file2 in os.listdir(file_path):
                print(file2, 222222222222222222222222222)
                file2_path = os.path.join(file_path, file2)
                file2_dest_path = os.path.join(destination_dir, file2)
                shutil.move(file2_path, file2_dest_path)

    for potential_videos in os.listdir(f"./static/{NAME}"):
        if potential_videos.endswith(".mp4"):
            input_file = f"./static/{NAME}/{potential_videos}"
            output_file = f"./static/{NAME}/converted-{potential_videos}"

            command = ['ffmpeg', '-i', input_file, '-c', 'copy', '-movflags', 'faststart', output_file]
            subprocess.call(command)
            os.remove(input_file)

def convert_mkv_to_mp4(input_file, output_file):
    # Run the ffmpeg command to convert the file
    subprocess.run(['ffmpeg', '-i', input_file, '-c', 'copy', output_file])
        
        
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

    for file in os.listdir(f"./pending-torents/{id}"):
        file_path = os.path.join(f"./pending-torents/{id}", file)
        new_file = file.replace(".mkv", ".mp4")
        convert_mkv_to_mp4(file_path, f"./pending-torents/{id}/{new_file}")

    move_files_to_directory(id=id, NAME=NAME)
    

    shutil.rmtree(f"./pending_torents/{id}")
    print("\nDownload complete!")

