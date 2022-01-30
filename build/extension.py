# Built using vscode-ext

import sys
import vscode
import os
import subprocess
import socket

ext = vscode.Extension(name = "mTubeMusic", display_name = "mTubeMusic", version = "0.0.1")
playing=False

def communicate(cmd=""):
    playing=False
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        sock.connect(("127.0.0.1" ,16000))
        playing=True
        if cmd!="":
            sock.send(cmd.encode("utf-8"))
        sock.close()
    except:
        pass
    return playing

@ext.event
def on_activate():
    return "The Extension"+ext.name+" has started"

@ext.command()
def play_song():
    if communicate():
        vscode.window.show_info_message("Already playing")
        return
    query=vscode.window.show_input_box()
    #vscode.window.show_info_message("type song name")
    if query!=None:
        query=query.split(" ")
        query=[q for q in query if q!=""]
        filename=os.path.join(os.path.dirname(os.path.realpath(__file__)),"tubeMusic.py")
        subprocess.Popen(["python",filename]+query)
    

@ext.command()
def stop_song():
    if(not communicate("quit")):
        vscode.window.show_info_message("Not playing")
        return
    vscode.window.show_info_message("Stopped")



def ipc_main():
    globals()[sys.argv[1]]()

ipc_main()
