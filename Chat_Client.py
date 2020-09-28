from PodSixNet.Connection import ConnectionListener,connection
from time import sleep
import tkinter as tk 
from tkinter import scrolledtext
from _thread import *
name = input('Enter name: ')
game_id = input('Enter game_id: ')
class Client(ConnectionListener):
    printed = True
    def Network_init(self,data):
        self.ch = data['ch']
        self.Send({'action' : 'connect' , 'channel' : data['ch'] , 'name' : name , 'game_id' :game_id})
    def Network_send(self,data):
        self.win.addMgs(data["name"], data["msg"])
        self.printed = True
    def Input(self,msg):
          if self.printed:
            self.msg = msg
            self.printed = False
            self.Send({'action' : 'msg' , 'game_id' : game_id, 'name' : name, 'msg' : self.msg})
    def Loop(self):
        self.Pump()
        connection.Pump()
 
 
class Chat(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title(self.__class__.__name__)
        self.geometry("500x500")
        self.bind('<Return>',self.addSelf)
        ## data ## 
        self.frame_height = 2
        self.username = name
 
    def addMgs(self, author, msg):
        self.msg.configure(state=tk.NORMAL)
        text = "{0}: {1}\n".format(author, msg)
        self.msg.insert(tk.INSERT, text)
        self.msg.configure(state=tk.DISABLED)
        
 
    def addSelf(self, clear=True , event = None):
        text = self.text.get("1.0",'end-1c').strip()
        if not text:
            return "no text"
        c.Input(text)
        if clear:
            self.text.delete("1.0", "end")
 
    def create(self):
        ## bottom input frame ##
        self.frame_inp = tk.Frame(self, height=100, bg="black")
        self.frame_inp.pack(side="bottom", fill="x")
 
        ## widgets for the input frame ##
        self.send = tk.Button(self.frame_inp, width=10, height=1, text="send", command=self.addSelf)
        self.send.pack(side="right", anchor="e",fill="y")
 
        self.text = tk.Text(self.frame_inp, height=self.frame_height)
        self.text.pack(fill="x")
 
 
        ## scrolled text ##
        self.msg = scrolledtext.ScrolledText(
            self,
            wrap=tk.WORD,
            height=200
        )
        self.msg.pack(fill="both")
        self.msg.configure(state=tk.DISABLED, font = ('Calibri',12 ,'bold'))
 
 
 

c =Client()
c.Connect(('localhost',12346)) 
def create_window():
    win = Chat()
    c.win = win
    win.create()
    win.mainloop() 
t2 = start_new_thread(create_window,())
while True:
    c.Loop()
 
