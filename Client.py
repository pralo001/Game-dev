from PodSixNet.Connection import connection,ConnectionListener
from time import sleep
import pygame
from _thread import *
from PodSixNet.Connection import connection,ConnectionListener
pygame.init()
rect_list = []
vel = 5
clock1 = pygame.time.Clock()
done = False
right = False
left = False
up = False
down = False
name = input('Enter name: ')
game_id = int(input('Enter game id: '))
class Rectangle:
    def __init__(self,x = 50,y = 50,width = 40, height = 60, colour = (255,0,0)):
        self.x = x
        self.y = y
        self.colour = colour
        self.width = width
        self.height = height
 
class Client(ConnectionListener):
    def Network_init(self,data):
        self.ch = data['ch']
        self.Send({'action' : 'connect' , 'channel' : data['ch'] , 'name' : name , 'game_id' :game_id})
    def Network_colour(self,data):
        global col
        col = data['col']
    def Network_rlist(self,data):
        rect_list.append(Rectangle(50,data['y'],40,60,data['col']))
    def Network_attr(self,data):
        global done
        for r in rect_list:
            if r.colour == data['colour']:
                if (right and r.x <= data['x']) or (left and r.x >= data['x']) and data['colour'] == col:
                   r.x = data['x']
                if data['colour'] != col:
                    r.x = data['x']
                if (down and r.y <= data['y']) or (up and r.y >= data['y']) and data['colour'] == col:
                   r.y = data['y']
                if data['colour'] != col:
                    r.y = data['y']
                done = True
        if not done:
            rect_list.append(Rectangle(data['x'],data['y'],40,60,data['colour']))
 
 
c = Client()
ip = '169.254.204.80'
c.Connect((ip,12345))
win = pygame.display.set_mode((500,500))
run = True
while run:
    clock1.tick(30)
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    keys = pygame.key.get_pressed()
    right = False
    left = False
    up = False
    down = False
    if keys[pygame.K_RIGHT]:
      right = True
      for r in rect_list:
        if r.colour == col:
                r.x += vel
    if keys[pygame.K_LEFT]:
        left = True
        for r in rect_list:
            if r.colour == col:
                r.x -= vel
    if left and right:
        left = right = False
    if keys[pygame.K_UP]:
        up = True
        for r in rect_list:
            if r.colour == col:
                r.y -= vel
    if keys[pygame.K_DOWN]:
        down = True
        for r in rect_list:
            if r.colour == col:
                r.y += vel
    if up and down:
        up = down = False
    win.fill((0,0,0))
    for r in rect_list:
        pygame.draw.rect(win,r.colour,(r.x,r.y,r.width,r.height))
    pygame.display.update()
    for rct in rect_list:
      if rct.colour == col:
        c.Send({'action': 'rect', 'x' : rct.x, 'y': rct.y , 'colour' : rct.colour,'game_id' : game_id})
    connection.Pump()
    c.Pump()
pygame.quit()
