# Yuri trojan
reverse shell trojan written in python.
It's more of a fun project for me, so please don't judge the code quality :)


# You need some libs to run the server!
To install them open your cmd and type:

`pip install colorama`

### if you get an error that `pip` isn't recognized as a command try replacing it with `pip3`
### if you still get package not found error, install it with `pip install <yourpackage>`

# Setup & Tutorial
## Setup
### Starting the server
To start the server head to [server](server/main.py) and start it with this command `python main.py` OR `python3 main.py`
After starting the server you can use it's console, please type `help` to see all the commands, as anything that isn't recognized locally will be SENT TO THE CLIENT AND EXECUTED
### Connecting the client
To start the client head to [client](client/main.py) and start it with this command `python main.py` OR `python3 main.py`
After starting the client it is ready to receive and run commands

## Tutorial
### Commands
`help` - displays all the commands 

`info` - shows info about the program

`clients` - shows all clients that connected(even those who disconnected, they are skipped when sending comms so it's fine)



 > anything WILL be sent to the client as a command
