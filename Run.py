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
from Settings import IDENT, CHANNEL

class SampleApp(tk.Tk):

    alreadyVoted = []
    voteTestAmount = 0

    voteAamount = 0
    voteBamount = 0
    voteCamount = 0

    optionA = ""
    optionB = ""
    optionC = ""
    questionUpdated = 0


    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.overrideredirect(True)
        self['background']='black'
        self.geometry("+0+20")
        self.attributes("-alpha", 1)

        self.s = openSocket()
        joinRoom(self.s)
        self.readbuffer = ""

        self.questionLabel = tk.Label(self, text="", bg="black", 
                fg="white", 
                font="HouseSlant-Regular 15", 
                anchor="w")
        self.questionLabel.pack()

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


    def update_tekst(self):
        resultA = self.optionA+": "+str(self.voteAamount)
        resultB = self.optionB+": "+str(self.voteBamount)
        resultC = self.optionC+": "+str(self.voteCamount)

        theQuestiontekst = str(self.questionUpdated)

        self.voteA.configure(text=resultA)
        self.voteB.configure(text=resultB)
        self.voteC.configure(text=resultC)

        self.questionLabel.configure(text=theQuestiontekst)

        print("updated tekst!")



    def get_votes(self):

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


            if "!options" in message and user == CHANNEL:





                # Setting up the question/options to vote on
                # This is a bit of a work in progress

                theQuestion = message.split('? ', 1)[0]+"?"
                theQuestion2 = theQuestion.replace("!options", "")

                theOptions = message.split('? ', 1)[1]

                a = theOptions.split(' ', 4)[0]
                b = theOptions.split(' ', 4)[1]
                c = theOptions.split(' ', 4)[2]
                

                sendMessage(self.s, "Vote with: !"+str(a)+" !"+str(b)+" !"+str(c))

                self.questionUpdated = str(theQuestion2)
                self.optionA = str(a)
                self.optionB = str(b)
                self.optionC = str(c)

                # create empty options, needs a fix
                if "empty" in self.optionA:
                    self.optionA = " "


                self.voteAamount = 0
                self.voteBamount = 0
                self.voteCamount = 0

                self.alreadyVoted = []


                self.update_tekst()
                time.sleep(1)
                self.update()
                break




                #to do: Wrap if statements in separate functions
            if "!"+self.optionA in message and user != IDENT:
                self.voteAamount += 1
                print(self.voteAamount)
                self.update_tekst() 
                time.sleep(1)
                self.update()
                break

            if "!"+self.optionB in message and user != IDENT:
                self.voteBamount += 1
                print(self.voteBamount)
                self.update_tekst() 
                time.sleep(1)
                self.update()
                break

            if "!"+self.optionC in message and user != IDENT:
                self.voteCamount += 1
                print(self.voteCamount)
                self.update_tekst() 
                time.sleep(1)
                self.update()
                break

            if "!reset" in message and user == CHANNEL:
                self.voteAamount = 0
                self.voteBamount = 0
                self.voteCamount = 0

                self.alreadyVoted = []

                self.update_tekst()
                time.sleep(1)
                self.update()

            if "!voteTest" in message and user not in self.alreadyVoted:
                self.voteTestAmount += 1
                self.alreadyVoted.append(user)
                break

            if "!exit" in message and user == CHANNEL:
                exit()


        self.update()
        self.after(500, self.get_votes)


app = SampleApp()
app.call('wm', 'attributes', '.', '-topmost', '1')
app.mainloop()