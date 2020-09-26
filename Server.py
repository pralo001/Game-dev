import random
from time import sleep
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
colours = [(255,0,0),(0,255,0),(0,0,255),(127,127,127),(0,127,127),(0,127,0),(127,127,0),(127,0,127),(255,255,0),(255,0,255),(0,255,255),(255,255,255)]
clients_list = []
port = 12345
y_p = [10,80,140,200,260,320,380,440]
class ClientChannel(Channel):
    def Network_rect(self,data):
        for p in clients_list:
            p.Send({'action' : 'attr', 'x' : data['x'], 'y' : data['y'] , 'colour' : data['colour']})
class MyServer(Server):
    channelClass = ClientChannel
    def Connected(self,channel,addr):
        c = random.choice(colours)
        channel.Send({'action' : 'colour', 'col' : c })
        colours.remove(c)
        y = random.choice(y_p)
        y_p.remove(y)
        clients_list.append(channel)
        for p in clients_list:
            p.Send({'action' : 'rlist', 'col' : c , 'y' : y})
s = MyServer(localaddr = ('localhost',port))
while True:
    s.Pump()
    sleep(0.001)

