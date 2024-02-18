from pytube import YouTube
import os
import subprocess
import shutil
import time

def mp3(link):
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    print("Enter the destination (leave blank for current directory)")
    destination = str(input(">>> ")) or '.'
    try:
        out_file = video.download(output_path=destination)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
    except:
        print("There has been an error and the file could not be downloaded!")
    print(yt.title + " has been successfully downloaded.")


def mp4(link):
    yt = YouTube(link)
    print("Enter the destination (leave blank for current directory)")
    destination = str(input(">>> ")) or ''
    video = yt.streams.filter(res="1080p", progressive=False).first().download(filename="video.mp4")
    audio = yt.streams.filter(abr="160kbps", progressive=False).first().download(filename="audio.mp3")
    try:
        cmd = f'ffmpeg -y -i audio.mp3  -r 60 -i video.mp4 -strict -2 -filter:a aresample=async=1 -c:a flac -c:v copy "{yt.title}.mp4"'
        subprocess.call(cmd, shell=True)
        if destination != '':
            shutil.move(f"{os.getcwd()}\\{yt.title}.mp4", destination)
        time.sleep(2)
        os.remove(f"{os.getcwd()}\\video.mp4")
        os.remove(f"{os.getcwd()}\\audio.mp3")
        print('Muxing Done')
    except:
        print("There has been an error and the file could not be downloaded!")
    
    print(f"{yt.title} has been successfully downloaded.")

choose = input("Please choose if you want to download MP3[1] or MP4[2]: ")

if int(choose) == 1:
    link = input("Please enter your url from YT you want to download here!: ")
    mp3(link)
elif int(choose) == 2:
    link = input("Please enter your url from YT you want to download here!: ")
    mp4(link)