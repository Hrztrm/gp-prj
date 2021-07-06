import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back
import time
import sys
from os import system, name

<<<<<<< HEAD
SERVER_HOST = "192.168.56.106"
=======
# set the available colors
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

# choose a random color for the client
client_color = random.choice(colors)

# server's IP address
# if the server is not on this machine, 
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "192.168.56.105"
>>>>>>> 2aedde634e14c58f831a0fb12fa75a076a2e7679
SERVER_PORT = 8888 # server's port
end = 0
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")
<<<<<<< HEAD
print("\n---------- HELLO PLAYER!! WELCOME TO NO-FEAR GAME ----------\t\t\t---- The game whereas only the brave player will survive----")

=======
print("\n---------- HELLO PLAYER!! WELCOME TO NO-FEAR GAME ----------\n---- The game whereas only the brave player will survive----")
print("\n\t****** PLAY TO WIN, BUT ENJOY THE FUN ******")
# prompt the client for a name
#name = input("Enter your name: ")
>>>>>>> 2aedde634e14c58f831a0fb12fa75a076a2e7679
def winner():
    print("\nWith the final encouter, encountered. You left the place with a code in hand. Waiting eagerly for the next adventure to come.\n")
    message = s.recv(1024).decode()
    print("\n\n" + message)
    global end
    end = 1

def dead():
    print("\nWith the final breath, breathed. You fell to the floor in anger and sadness. Hopefully in the next life, you shall emerge victorious")
    message = s.recv(1024).decode()
    print("\n\n" + message)
    global end
    end = 1

def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        if message == "win":
            winner()
            break
        elif message == "died":
            dead()
            break
        else:
            print("\n" + message)

def send_message(s):
    while True:
        msg = input()
        s.send(msg.encode())
        time.sleep(0.05)
    global end
    end = 1


# make a thread that listens for messages to this client & print them
t1 = Thread(target=listen_for_messages)
t2 = Thread(target=send_message, args=(s,))
# make the thread daemon so it ends whenever the main thread ends
t1.daemon = True
t2.daemon = True
# start the thread
t1.start()
t2.start()

while True:
    if end == 1:
        break

# close the socket
s.close()
