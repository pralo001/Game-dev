from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from time import sleep
class Game:
   pass
G = Game()
class ClientChannel(Channel):
    def __init__(self,*args,**kwargs):
        Channel.__init__(self,*args,**kwargs)
    def Network_connect(self,data):
        G.channels_dict[data['name']] = data['channel']
        G.games[data['name']] = data['game_id']
        print(G.channels_dict)
        print(G.games)
    def Network_msg(self,data):
        for x in G.games:
            if G.games[x] == data['game_id']:
                i = G.channels_dict[x]
                ch = G.channels_list[i]
                ch.Send({'action' : 'send' , 'name' : data['name'] ,'msg' : data['msg']})
class Game_Server(Server):
    channelClass = ClientChannel
    def __init__(self,*args,**kwargs):
        Server.__init__(self,*args,**kwargs)  
        G.channels_dict = {}
        G.games = {}
        G.channels_list = []
    def Connected(self,channel,addr):
        G.channels_list.append(channel)
        channel.Send({'action': 'init', 'ch' : G.channels_list.index(channel)})
   
s = Game_Server(localaddr = ('localhost',12346))
while True:
    s.Pump()
    sleep(0.001)