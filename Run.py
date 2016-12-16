# Feel free to use this code
# Special thank you to Jochem van der Spek who helped me greatly while developing this
# And to Just van Rossum for getting me interested in Python

import Tkinter as tk
import time
import socket
from Read import getUser, getMessage
from Socket import openSocket, sendMessage
from Initialize import joinRoom
from collections import OrderedDict

class SampleApp(tk.Tk):

    alGestemd = []
    voteTestAmount = 0

    voteAamount = 0
    voteBamount = 0
    voteCamount = 0

    optieA = ""
    optieB = ""
    optieC = ""
    lol = 0


    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.overrideredirect(True)
        self['background']='black'
        self.geometry("+0+20")
        self.attributes("-alpha", 1)

        self.s = openSocket()
        joinRoom(self.s)
        self.readbuffer = ""

        self.vraaglabel = tk.Label(self, text="", bg="black", 
                fg="white", 
                font="HouseSlant-Regular 15", 
                anchor="w")
        self.vraaglabel.pack()

        self.voteA = tk.Label(self, text="", bg="black", 
                fg="white", 
                font="HouseSlant-Regular 30", 
                anchor="w")
        self.voteA.pack()
        self.voteB = tk.Label(self,text="", bg="black", 
                fg="white", 
                font="HouseSlant-Regular 30", 
                anchor="w")
        self.voteB.pack()
        self.voteC = tk.Label(self,text="", bg="black", 
                fg="white", 
                font="HouseSlant-Regular 30", 
                anchor="w")
        self.voteC.pack()

        self.update_tekst()
        self.get_votes()
        # self.anderemethod()
        # self.after(500,self.get_votes)
        # self.after(500,self.update_tekst)

    def update_tekst(self):
        resultA = self.optieA+": "+str(self.voteAamount)
        resultB = self.optieB+": "+str(self.voteBamount)
        resultC = self.optieC+": "+str(self.voteCamount)

        devraagtekst = str(self.lol)

        self.voteA.configure(text=resultA)
        self.voteB.configure(text=resultB)
        self.voteC.configure(text=resultC)

        self.vraaglabel.configure(text=devraagtekst)

        print("updated tekst!")

        # self.after(500, self.update_tekst)

    def get_votes(self):
        # print "About to read"
        try:
            chat_data =  self.s.recv(1024)
        except socket.timeout:
            self.after(500,self.get_votes)
            return

        self.readbuffer = self.readbuffer + chat_data
        print "Reading successful"
        temp = self.readbuffer.split('\n')
        self.readbuffer = temp.pop() #save the last (possibly incomplete) line for later
        if self.readbuffer == "":
            pass #no further messages in the queue
            #you should add a sleep time here for the sake of your hot NIC

        for line in temp:
            print(line)
 
            if "PING" in line:
                s.send("PONG :tmi.twitch.tv\r\n".encode())
                break
 
            user = getUser(line)
            message = getMessage(line)
 
            print "{} typed: {}".format(user, message)
           
            if "!commands" in message:
                sendMessage(self.s, "'!voteA','!voteB','!voteC'")
                break

            #optie toevoegen !optieEen lol
            if "!options" in message:
                #print de laatste optieEen (by default is dat "lol")
                # print(optieEen)
                #!opties lol1 lol2 lol3
                #a = de message, split de message, de delimiter is een spatie, en we splitten het 1 keer, en dan willen we het tweede list item hebben
                #want dat is het woord dat we nodig hebben, dus:
                # !optieEen lol, dan is lol [1]
                devraag = message.split('? ', 1)[0]+"?"
                devraag2 = devraag.replace("!options", "")

                deopties = message.split('? ', 1)[1]

                a = deopties.split(' ', 4)[0]
                b = deopties.split(' ', 4)[1]
                c = deopties.split(' ', 4)[2]
                
                #post het nog ff in de chat, niet vergeten nog een string te maken van 'a'
                sendMessage(self.s, "Vote with: !"+str(a)+" !"+str(b)+" !"+str(c))
                #sla de nieuwe optie op in 'optieEen'
                self.lol = str(devraag2)
                self.optieA = str(a)
                self.optieB = str(b)
                self.optieC = str(c)

                if "leeg" in self.optieA:
                    self.optieA = " "


                self.voteAamount = 0
                self.voteBamount = 0
                self.voteCamount = 0

                self.alGestemd = []


                self.update_tekst()
                time.sleep(1)
                self.update()
                break
                #print het ff om te checken
                # print(optieEen)



            if "!"+self.optieA in message and user != "appie_bot":
                self.voteAamount += 1
                print(self.voteAamount)
                self.update_tekst() 
                time.sleep(1)
                self.update()
                break

            if "!"+self.optieB in message and user != "appie_bot":
                self.voteBamount += 1
                print(self.voteBamount)
                self.update_tekst() 
                time.sleep(1)
                self.update()
                break

            if "!"+self.optieC in message and user != "appie_bot":
                self.voteCamount += 1
                print(self.voteCamount)
                self.update_tekst() 
                time.sleep(1)
                self.update()
                break

            if "!reset" in message:
                self.voteAamount = 0
                self.voteBamount = 0
                self.voteCamount = 0

                self.alGestemd = []

                self.update_tekst()
                time.sleep(1)
                self.update()

            if "!voteTest" in message and user not in self.alGestemd:
                self.voteTestAmount += 1
                self.alGestemd.append(user)
                break

            if "!exit" in message and user == "appie_bot_master":
                exit()


        self.update()
        self.after(500, self.get_votes)


app = SampleApp()
app.call('wm', 'attributes', '.', '-topmost', '1')
app.mainloop()