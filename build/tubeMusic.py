from urllib import request
import sys
query="+".join(sys.argv[1:])
#query=query.replace(" ","+")
url="https://www.youtube.com/results?search_query="+query
response=request.urlopen(url)
html=response.read()
html=html.decode("utf-8")
vid=html.find("/watch?v=")
if vid==-1:
    #print("No video found")
    sys.exit()
vid=html[vid:vid+30]
vid=vid[:vid.find("\"")]
vid="https://www.youtube.com"+vid
#print(vid)

import pafy
video=pafy.new(vid)
audio=video.getbestaudio()

import vlc
player=vlc.MediaPlayer(audio.url)

from pynput.keyboard import Key, Listener

def on_press(key):
    #print(key)
    if key==Key.media_play_pause:
        if player.is_playing():
            player.pause()
        else:
            player.play()

Listener(on_press=on_press).start()

import socket
from threading import Thread

running=True

def sockThread():
    global running
    so=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    so.bind(("127.0.0.1",16000))
    so.listen(1)
    while True:
        sock,addr=so.accept()
        data=sock.recv(1024)
        sock.close()
        if data==b"quit":
            break
    so.close()
    running=False

t=Thread(target=sockThread)
t.setDaemon(True)
t.start()

import time
player.play()
while(running and player.get_state()!=vlc.State.Ended):
    time.sleep(1)    


