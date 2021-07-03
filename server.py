import socket
from threading import Thread
import random

# server's IP address
SERVER_HOST = "192.168.56.106"
SERVER_PORT = 8888 # port we want to use
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize list/set of all connected client's sockets
all_cs = set()
pl = []
l_enemy = ["Goblin", "Kobold", "Orc"]
# create a TCP socket
s = socket.socket()
# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))
# listen for upcoming connections
s.listen(5)
intro = "tes test test" #needs changing
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
menu = "1. Attack\n2. Defend\n3. Magic\n4. Item\n5. Wait\n\n"
death_count = 0
class enemy:
    def __init__(self, typ, stren, agil, intel):
        self.typ = typ
        if self.typ == "Goblin":
            self.m_hp = stren + 5
        elif self.typ == "Kobold":
            self.m_hp = stren + 10
        elif self.typ == "Orc":
            self.m_hp = stren + 15
        self.c_hp = self.m_hp
        self.stren = stren
        self.agil = agil
        self.intel = intel
    
    def p_stat(self):
        return f"Type: {self.typ}\nHealth: {self.c_hp}/{self.m_hp}\nStrength: {self.stren}\nAgility: {self.agil}\nIntelligence: {self.intel}"
    
    def take_dmg(self, dmg):
        self.c_hp = self.c_hp - dmg

    def cond(self):
        if self.c_hp >= self.m_hp * 3/4:
            return "Healthy"
        elif self.c_hp >= self.m_hp * 2/4:
            return "Hurt"
        elif self.c_hp >= self.m_hp * 1/ 4:
            return "Very Hurt"
        else:
            return "Near Death"

    def deal_dmg(self):
        if self.typ == "Orc":
            dmg = self.stren
        elif self.typ == "Kobold":
            dmg = self.agil
        elif self.typ == "Goblin":
            dmg = self.intel
        return dmg

"""
def battle(cs, c, player):
    menu(cs)
    target_list = ["1. Player 1", "2. Player 2", "3. Enemy"]
    while True:
        try:
            command = cs.recv(1024).decode()
        except Exception as e:
            print(f"Error: {e}")
            all_cs.remove(cs)
        if command == "1":
            cs.send(target_list.encode())
"""

def sto1(cs, msg):
    cs.send(msg.encode())

def stoa(msg):
    for cs in all_cs:
        cs.send(msg.encode())

"""
def adventure(cs):

    menu(cs)
    while True:
        try:
            # keep listening for a message from `cs` socket
            msg = cs.recv(1024).decode()
            
        except Exception as e:
            print(f"[!] Error: {e}")
            all_cs.remove(cs)
        # iterate over all connected sockets
        for client_socket in all_cs:
            if msg == "stat":
                client_socket.send(pl[0].p_stat().encode())
            if msg == "magic":
                client_socket.send(pl[1].m_list().encode())
                msg = cs.recv(1024).decode()
            if msg == "a":
                client_socket.send(pl[0].p_stat().encode())
                #if msg == "1":
                    #Damage definiontn
                #elif msg == "2":
                    #dmg
                #elif msg == "3":
                    #stuff
                #elif msg == "5"
                    #back
                #    continue
"""

class adv:
    def __init__(self, cl, stren, agil, intel):
        self.cl = cl
        if cl == "Warrior":
            self.c_hp = stren + 10
            self.m_hp = stren + 10
        elif cl == "Archer":
            self.c_hp = stren + 5
            self.m_hp = stren + 5
        elif cl == "Mage":
            self.c_hp = stren
            self.m_hp = stren
        self.stren = stren
        self.agil = agil
        self.intel = intel
        self.dead = 0
        if (cl == "Mage"):
            self.spell = ["Magic Bolt", "Mind Shock", "Heal"]
        elif (cl == "Warrior" or cl == "Archer"):
            self.spell = [" ", " ", " "]

    def p_health(self):
        return f"Health {self.c_hp}/{self.m_hp}"

    def take_dmg(self, dmg):
        self.c_hp = self.c_hp - dmg

    def p_stat(self):
        return f"Class: {self.cl}\nHealth: {self.c_hp}/{self.m_hp}\nStrength: {self.stren}\nAgility: {self.agil}\nIntelligence: {self.intel}"

    def m_list(self):
        return f"Magic\n1. {self.spell[0]}\n2. {self.spell[1]}\n3. {self.spell[2]}\n\n5. Back"

    def cond(self):
        if self.c_hp >= self.m_hp * 3/4:
            return f"Healthy"
        elif self.c_hp >= self.m_hp * 2/4:
            return f"Hurt"
        elif self.c_hp >= self.m_hp * 1/ 4:
            return f"Very Hurt"
        elif self.c_hp > 0:
            return f"Near Death"
        else:
            return f"Dead"

    def death(self):
        self.m_hp = 0
        self.stren = 0
        self.agil = 0
        self.intel = 0
        self.dead = 1

    def deal_dmg(self):
        if self.cl == "Warrior":
            dmg = self.stren
        elif self.cl == "Archer":
            dmg = self.agil
        elif self.cl == "Mage":
            dmg = self.intel
        return dmg

    def buff(self):
        print("hi")

def story(part):
    if part == "start":
        for cs in all_cs:
            cs.send(intro.encode())


def w_room():
    global pl1
    global pl2
    player = 1
    while player != 3:
    #while True:
        client_socket, client_address = s.accept()
        print(f"[+] {client_address} connected.")
        # add the new connected client to connected sockets
        all_cs.add(client_socket)
        if player == 1:
            pl1 = client_socket
            print("player 1")
            pl.append(adv("Warrior", 10, 5, 3)) #Should be changed with random class
        elif player == 2:
            pl2 = client_socket
            print("player 2")
            msg = "Player 2 has joined"
            pl1.send(msg.encode())
            pl.append(adv("Archer", 5, 10, 3)) #Also changed with random class
        player+=1

    # start a new thread that listens for each client's messages
        #t = Thread(target=create_player, args=(client_socket,len(all_cs)))
    # make the thread daemon so it ends whenever the main thread ends
        #t.daemon = True
    # start the thread
        #t.start()

def select(play):
    s = f"1. Player 1: {pl[0].cond()}\n2. Player 2: {pl[1].cond()}\n3. {enemy1.typ}: {enemy1.cond()}\n\n5. Back"
    print(s)
    if play == 0:
        pl1.send(s.encode())
        return pl1.recv(1024).decode()
    elif play == 1:
        pl2.send(s.encode())
        return pl2.recv(1024).decode()

def turn(play):
    while True:
        act = "0"
        while act != "1" and act != "2" and act != "3" and act != "4":
            if play == 0:
                #sto1(pl2, "Waiting for Player 1 to finish turn")
                sto1(pl1, menu)
                act = pl1.recv(1024).decode()
            elif play == 1:
                #sto1(pl1, "Waiting for Player 2 to finish turn")
                sto1(pl2, menu)
                act = pl2.recv(1024).decode()

        if act == "1":
            targ = select(play)
            if targ == "3":
                enemy1.take_dmg(pl[play].deal_dmg())
            elif targ == "1":
                pl[0].take_dmg(pl[play].deal_dmg())
            elif targ == "2":
                pl[1].take_dmg(pl[play].deal_dmg())
            elif targ == "5": #Back
                continue
            break

        elif act == "2":
            print("Defending")
            break

        elif act == "3":
            if play == 0:
                pl1.send(pl[play].m_list().encode())
                pl1.send("\n5. Back".encode())
            elif play == 1:
                pl2.send(pl[play].m_list().encode())
                pl2.send("\n5. Back".encode())
            if play == 0:
                mgc = pl1.recv(1024).decode()
                if mgc == "5":
                    continue
            elif play == 1:
                mgc = pl2.recv(1024).decode()
                if mgc == "5":
                    continue
            targ = select(play)
            print("progs")
            #damage for type spell or stuff
    global death_count
    i = 0
    for check in pl:
        if pl[i].c_hp <= 0:
            pl[i].death()
            death_count += 1
            if i == 0:
                sto1(pl1, "died")
                sto1(pl1, "no hint yet")
            elif i == 1:
                sto1(pl2, "died")
                sto1(pl2, "no hint yet")
        i += 1
    #here will be the magic and def and item part

    print(enemy1.p_stat())
    print("\n")
    print(pl[1].p_stat())

def battle():
    play = 0
    sto1(pl2, "You have encountered an enemy, prepare for BATTLE.") #Change to stoa
    global enemy1
    global death_count
    enemy1 = enemy(random.choice(l_enemy), random.randint(1,2), random.randint(5,10), random.randint(5,10))
    print(enemy1.p_stat())
    while enemy1.c_hp > 0:
        if pl[0].agil >= pl[1].agil:
            if not pl[0].dead:
                turn(0)
            if not pl[1].dead:
                turn(1)
        elif pl[1].agil > pl[0].agil:
            if not pl[1].dead:
                turn(1)
            #if not pl[0].dead:
                #turn(0)
        if enemy1.c_hp > 0:
            if enemy1.typ == "Goblin":
                if pl[0].stren >= pl[1].stren and not pl[1].dead:
                    pl[1].take_dmg(enemy1.deal_dmg())
                else:
                    pl[0].take_dmg(enemy1.deal_dmg())
            elif enemy1.typ == "Orc":
                if pl[0].stren >= pl[1].stren and not pl[0].dead:
                    pl[0].take_dmg(enemy1.deal_dmg())
                    pl[1].take_dmg(enemy1.deal_dmg() * 0.1)
                else:
                    pl[1].take_dmg(enemy1.deal_dmg())
                    pl[0].take_dmg(enemy1.deal_dmg() * 0.1)
            elif enemy1.typ == "Kobold":
                hit = random.randint(0,1)
                pl[hit].take_dmg(enemy1.deal_dmg())
        print(pl[0].p_stat())
        print(pl[1].p_stat())
        print(enemy1.p_stat())
        i = 0
        for check in pl:
            if pl[i].c_hp <= 0:
                pl[i].death()
                death_count += 1
                if i == 0:
                    sto1(pl1, "died")
                    sto1(pl1, "no hint yet")
                elif i == 1:
                    sto1(pl2, "died")
                    sto1(pl2, "no hint yet")
            i += 1

def trap():
    sto1(pl2, "Trap")

w_room()
n_enc = 0
print(pl1)
print(pl2)

#story("start")
while n_enc <= 5:
    enc = random.randint(1,2)
    print(enc)
    n_enc += 1
    enc = 1
    if enc == 1:
        battle()
    elif enc == 2:
        trap()








"""
#This is the before version of Waiting room, should be not relevant now
while True:
    # we keep listening for new connections all the time
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    # add the new connected client to connected sockets
    all_cs.add(client_socket)
    if player == 1:
        pl1 = client_socket
        print("player 1")
        pl.append(adv("Warrior", 10, 5, 3))
    elif player == 2:
        pl2 = client_socket
        print("player 2")
        msg = "Player 2 has joined"
        pl1.send(msg.encode())
        pl.append(adv("Archer", 10, 5, 3))
    player+=1
    
    # start a new thread that listens for each client's messages
    t = Thread(target=create_player, args=(client_socket,len(all_cs)))
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()
"""
# close client sockets
for cs in all_cs:
    cs.close()
# close server socket
s.close()
