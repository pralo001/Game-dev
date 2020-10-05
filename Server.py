import random
from time import sleep
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
import socket
colours = [(255,0,0),(0,255,0),(0,0,255),(127,127,127),(0,127,127),(0,127,0),(127,127,0),(127,0,127),(255,255,0),(255,0,255),(0,255,255),(255,255,255)]
clients_list = []
port = 12345
y_p = [10,80,140,200,260,320,380,440]
class Game:
   pass
G = Game()
class ClientChannel(Channel):
    def Network_connect(self,data):
        G.channels_dict[data['name']] = data['channel']
        G.games[data['name']] = data['game_id']
        c = random.choice(colours)
        i = data['channel']
        
        G.channels_list[i].Send({'action' : 'colour', 'col' : c })
        colours.remove(c)
        y = random.choice(y_p)
        y_p.remove(y)
        #clients_list.append(channel)
        for x in G.games:
            if G.games[x] == data['game_id']:
                i = G.channels_dict[x]
                ch = G.channels_list[i]
                ch.Send({'action' : 'rlist', 'col' : c , 'y' : y})
        print(G.channels_dict)
        print(G.games)
    def Network_rect(self,data):
        for x in G.games:
            if G.games[x] == data['game_id']:
                i = G.channels_dict[x]
                ch = G.channels_list[i]
                ch.Send({'action' : 'attr', 'x' : data['x'], 'y' : data['y'] , 'colour' : data['colour']})
class MyServer(Server):
    channelClass = ClientChannel
    def __init__(self,*args,**kwargs):
        Server.__init__(self,*args,**kwargs)  
        G.channels_dict = {}
        G.games = {}
        G.channels_list = []
    def Connected(self,channel,addr):
        G.channels_list.append(channel)
        channel.Send({'action': 'init', 'ch' : G.channels_list.index(channel)})

hostname = socket.gethostname()
#print(hostname)
ip = socket.gethostbyname(hostname)
#print(ip)
s = MyServer(localaddr = (ip,port))
while True:
    s.Pump()
    sleep(0.001)

