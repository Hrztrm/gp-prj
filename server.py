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
print("\n\t~~~~~~~~~~ Simple Game Server ~~~~~~~~~~ ")
print("---------------------------------------------------")
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
menu = "1. Attack\n2. Defend\n3. Analyze\n4. Warp\n5. Wait\n\n"
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

def sto1(cs, msg):
    cs.send(msg.encode())

def stoa(msg):
    for cs in all_cs:
        cs.send(msg.encode())

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
        self.dmg_taken = 1
        self.insight = 0
        if (cl == "Mage"):
            self.spell = ["Magic Bolt", "Mind Shock", "Heal"]
        elif (cl == "Warrior" or cl == "Archer"):
            self.spell = [" ", " ", " "]

    def p_health(self):
        return f"Health {self.c_hp}/{self.m_hp}"

    def take_dmg(self, dmg):
        self.c_hp = self.c_hp - (dmg * self.dmg_taken)
        self.dmg_taken = 1

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

    def analyze(self):
        self.insight = 1

    def deal_dmg(self): #Dealing damage
        if self.cl == "Warrior":
            dmg = self.stren
        elif self.cl == "Archer":
            dmg = self.agil
        elif self.cl == "Mage":
            dmg = self.intel
        return dmg

    def warping(self, targ): #Minus stat
        if targ == "1":
            print("Warping strength")
            self.stren -= 2
        elif targ == "2":
            print("Warping Agility")
            self.agil -= 2
        elif targ == "3":
            print("Warping Intelligence")
            self.intel -= 2

    def sac(self):
        if self.cl == "Warrior":
            self.stren += 10
        elif self.cl == "Archer":
            self.agil += 10
        elif self.cl == "Mage":
            self.intel += 10

    def defend(self):
        self.dmg_taken = 0.5

    def heal(self, h):
        self.c_hp += h
        if self.c_hp > self.m_hp:
            self.c_hp = self.m_hp

def story(part):
    if part == "start":
        for cs in all_cs:
            cs.send(intro.encode())


def warp(player):
    if player == 0:
        sto1(pl1, pl[player].p_stat())
        sto1(pl1, "\n1. Strength\n2. Agility\n3. Intelligence\n\n5. Back")
        return pl1.recv(1024).decode()
    elif player == 1:
        sto1(pl2, pl[player].p_stat())
        sto1(pl2, "\n1. Strength\n2. Agility\n3. Intelligence\n\n5. Back")
        return pl2.recv(1024).decode()

def w_room():
    global pl1
    global pl2
    player = 1
    while player != 3:
    #while True:
        client_socket, client_address = s.accept()
        print(f"[+] {client_address} connected.\n---------------------------------------------------")
        # add the new connected client to connected sockets
        all_cs.add(client_socket)
        if player == 1:
            pl1 = client_socket
            print("player 1")
            sto1(pl1, "Player 1 has entered")
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
    norm = f"1. Player 1: {pl[0].cond()}\n2. Player 2: {pl[1].cond()}\n3. {enemy1.typ}: {enemy1.cond()}\n\n5. Back"
    hide = f"1. Player 1: {pl[0].cond()}\n2. Player 2: {pl[1].cond()}\n3. Hidden: {enemy1.cond()}\n\n5. Back"
    if play == 0:
        if pl[play].insight == 0:
            sto1(pl1, hide)
        else:
            sto1(pl1, norm)
        return pl1.recv(1024).decode()
    elif play == 1:
        if pl[play].insight == 0:
            sto1(pl2, hide)
        else:
            sto1(pl2, norm)
        return pl2.recv(1024).decode()

def death_check():
    global death_count
    i = 0
    for check in pl:
        if pl[i].c_hp <= 0 and pl[i].dead == 0:
            pl[i].death()
            death_count += 1
            if i == 0:
                sto1(pl1, "died")
                sto1(pl1, "no hint yet")
                sto1(pl2, f"Player 1 has died while fighting {enemy1.typ}\n")
            elif i == 1:
                sto1(pl2, "died")
                sto1(pl2, "no hint yet")
                sto1(pl1, f"Player 2 has died while fighting {enemy1.typ}'n")
        i += 1
    if death_count == 2:
        endprog()

def hidden(hid ,player):
    norm = f"\nPlayer 1: {pl[0].cond()}\nPlayer 2: {pl[1].cond()}\n{enemy1.typ}: {enemy1.cond()}\n\n"
    hide = f"\nPlayer 1: {pl[0].cond()}\nPlayer 2: {pl[1].cond()}\nHidden: {enemy1.cond()}\n\n"
    if hid == 0:
        sto1(player, hide)
    elif hid == 1:
        sto1(player, norm)

def turn(play): #play = 0 == PLayer 1 turn, play = 1 == Player 2 turn
    while True:
        act = "0"
        while act != "1" and act != "2" and act != "3" and act != "4" and act != "5":
            if play == 0:
                sto1(pl2, "Waiting for Player 1 to finish turn")
                hidden(pll[play].insight, pl1)
                sto1(pl1, pl[play].p_stat() + "\n\n")
                sto1(pl1, menu)
                act = pl1.recv(1024).decode()
            elif play == 1:
                sto1(pl1, "Waiting for Player 2 to finish turn")
                hidden(pl[play].insight, pl2)
                sto1(pl2, pl[play].p_stat() + "\n\n")
                sto1(pl2, menu)
                act = pl2.recv(1024).decode()

        if act == "1":
            print("Attacking")
            targ = select(play)
            if targ == "3":
                print(f"Attacking {enemy1.typ}\n")
                enemy1.take_dmg(pl[play].deal_dmg())
            elif targ == "1":
                print("Attacking player 1\n")
                pl[0].take_dmg(pl[play].deal_dmg())
            elif targ == "2":
                print("Attacking player 2\n")
                pl[1].take_dmg(pl[play].deal_dmg())
            elif targ == "5": #Back
                print("Back from Attacking\n")
                continue
            break

        elif act == "2":
            print("Defending\n")
            pl[play].defend()
            break

        elif act == "3":
            targ = select(play)
            if targ == "3":
                print("Analyzing enemy")
                stat = enemy1.p_stat()
            elif targ == "1":
                print("Analyzing Player 1")
                stat = pl[0].p_stat()
            elif targ == "2":
                print("Analyzing Player 2")
                stat = pl[1].p_stat()
            elif targ == "5": #Back
                print("Back from analyzing")
                continue
            pl[play].analyze()
            if play == 0:
                sto1(pl1, stat)
            elif play == 1:
                sto1(pl2, stat)
            break
        
        elif act == "4":
            targ = warp(play)
            if targ == "5":
                print("Back from Warping")
                continue
            else:
                pl[play].warping(targ)
                break

        elif act == "5":
            print("Wait")
            break

    death_check()
    print("\n")
    print(enemy1.p_stat())
    print("\n")
    print(pl[1].p_stat())
    print("\n")
    print(pl[0].p_stat())
    print("\n")

def battle():
    play = 0
    if not pl[0].dead:
        sto1(pl1, "You have encountered an enemy, prepare for BATTLE.\n") #Change to stoa
    if not pl[1].dead:
        sto1(pl2, "You have encountered an enemy, prepare for BATTLE.\n") #Change to stoa
    global enemy1
    global death_count
    enemy1 = enemy(random.choice(l_enemy), random.randint(1,2), random.randint(5,10), random.randint(5,10))
    print(enemy1.p_stat())
    while enemy1.c_hp > 0: #Fight until enemy dies
        if pl[0].agil >= pl[1].agil: #Player 1 then player 2
            if not pl[0].dead:
                turn(0)
            if not pl[1].dead:
                turn(1)
        elif pl[1].agil > pl[0].agil: #Player 2 then player 1
            if not pl[1].dead:
                turn(1)
            if not pl[0].dead:
                turn(0)
        if enemy1.c_hp > 0: #Enemy's Turn
            if enemy1.typ == "Goblin":
                if pl[0].stren >= pl[1].stren and not pl[1].dead:
                    pl[1].take_dmg(enemy1.deal_dmg())
                else:
                    pl[0].take_dmg(enemy1.deal_dmg())
            elif enemy1.typ == "Orc":
                if pl[0].stren >= pl[1].stren and not pl[0].dead:
                    pl[0].take_dmg(enemy1.deal_dmg())
                    pl[1].take_dmg(int(enemy1.deal_dmg() * 0.2))
                else:
                    pl[1].take_dmg(enemy1.deal_dmg())
                    pl[0].take_dmg(int(enemy1.deal_dmg() * 0.2))
            elif enemy1.typ == "Kobold":
                hit = random.randint(0,1)
                pl[hit].take_dmg(enemy1.deal_dmg())
        print("\n")
        print(pl[0].p_stat())
        print("\n")
        print(pl[1].p_stat())
        print("\n")
        print(enemy1.p_stat())
        print("\n")
        i = 0
        for check in pl:
            pl[i].dmg_taken = 1 #Reset the defense
            i += 1
        death_check()
    i = 0
    for check in pl:
        pl[i].insight = 0

def sac_room():
    print("Sacrifical Room")
    if not pl[0].dead:
        sto1(pl1, "You encountered a room with an altar in the middle. There are carvings on the floor that says \"Sacrifice some of your partner's life for greater power\"\nWhat will you do?\n\n1. Sacrifice\n2. Leave")
    if not pl[1].dead:
        sto1(pl2, "You encountered a room with an altar in the middle. There are carvings on the floor that says \"Sacrifice some of your partner's life for greater power\"\nWhat will you do?\n\n1. Sacrifice\n2. Leave")
    #sto1(pl2, "Sac room. 1 or 2")
    if not pl[0].dead:
        com1 = pl1.recv(1024).decode()
        if com1 == "1":
            pl[0].sac()
            pl[1].take_dmg(10)
            death_check()
    if not pl[1].dead:
        com2 = pl2.recv(1024).decode()
        if com1 == "1":
            pl[1].sac()
            pl[0].take_dmg(10)
            death_check()

def rec_room():
    print("Recovery Room")
    if not pl[0].dead:
        sto1(pl1, "You encountered a room with a statue inside. Carvings on the statues that says \"Answer with unison, fruition shall follow. Answer with contrast, only dust will follow\"\nWhat will you do?\n\n1. Single heal\n2. All heal")
    if not pl[1].dead:
        sto1(pl2, "You encountered a room with a statue inside. Carvings on the statues that says \"Answer with unison, fruition shall follow. Answer with contrast, only dust will follow\"\nWhat will you do?\n\n1. Single heal\n2. All heal")
    #sto1(pl2, "1 singel heal\n2 all heal")
    if not pl[0].dead:
        com1 = pl1.recv(1024).decode()
        if com1 == "1":
            sto1(pl1, "Who Shall be healed?\n\n1. Player 1\n2. Player 2")
            h1 = pl1.recv(1024).decode()
            print(f"h1: {h1}")
        else:
            com1 = "2"
    if not pl[1].dead:
        com2 = pl2.recv(1024).decode()
        if com2 == "1":
            sto1(pl2, "Who Shall be healed?\n\n1. Player 1\n2. Player 2")
            h2 = pl2.recv(1024).decode()
            print(f"h2: {h2}")
        else:
            com2 = "2"
    if pl[0].dead:
        com1 = com2
        h1 = h2
    if pl[1].dead:
        com2 = com1
        h2 = h1
    if com1 == "2" and com2 == "2":
        pl[0].heal(5)
        pl[1].heal(5)
        print("All Heal by 5")
    elif com1 == com2 and h1 == h2:
        if h1 == "1":
            print("Heal player 1 by 10")
            pl[0].heal(10)
        elif h1 == "2":
            print("Heal player 2 by 10")
            pl[1].heal(10)
    else:
        if not pl[0].dead:
            sto1(pl1, "No help will be given to people with no unison")
        if not pl[1].dead:
            sto1(pl2, "No help will be given to people with no unison")

def endprog():
    global death_count
    if death_count == 2:
        print("Both players has died")
        for cs in all_cs:
            cs.close()
        s.close()
        quit()

w_room()
n_enc = 0

#story("start")
while n_enc <= 5:
    n_enc += 1
    if n_enc == 3:
        sac_room()
    elif n_enc == 5:
        rec_room()
    else:
        battle()


# close client sockets
for cs in all_cs:
    cs.close()
# close server socket
s.close()
