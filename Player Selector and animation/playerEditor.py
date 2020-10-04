import pygame
import os
import random
from playerCodeAssets import playerT_animate,playerR_animate
screen_x = 0
screen_y = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (screen_x,screen_y)
pygame.init()

# screen width and height and Fps
SCREEN_WIDTH = 1370
SCREEN_HEIGHT= 700
FPS =  100
# setup
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Single player mode")
FONT = pygame.font.SysFont("inkfree",32,bold=True,italic=True)
CLOCK = pygame.time.Clock()

class Character:
    def __init__(self,Dict,lst):
        self.Dict = Dict
        self.x,self.y,self.width, self.height  = self.Dict['x'],self.Dict['y'],self.Dict['width'],self.Dict['height']
        self.col,self.lst,self.frames,self.path = self.Dict['col'],lst,self.Dict['frames'],self.Dict['path']
        self.text = self.Dict['text']
        self.text_pos  = self.Dict['text_pos']
        self.rct = (self.Dict['rect_x'],self.Dict['rect_y'],self.Dict['width'],self.Dict['height'])
        self.anim_start,self.animated = 0,True
        self.image = self.lst[self.anim_start]
        self.textSurf,self.textShadow = FONT.render(self.text,True,(0,0,0)),FONT.render(self.text,True,(128,128,128))
        self.img = pygame.image.load(os.path.join(Dict['path'],self.image)).convert()
    def draw(self):
        self.img.set_colorkey((self.col))
        SCREEN.blit(self.textShadow,(self.text_pos[0]+3,self.text_pos[1]))
        SCREEN.blit(self.textSurf,(self.text_pos[0],self.text_pos[1]))
        SCREEN.blit(self.img,(self.x,self.y))
    def animate(self):
        if self.animated:
            self.image = self.lst[int(self.anim_start)]
            self.img = pygame.image.load(os.path.join(self.path,self.image)).convert()
            self.anim_start += 0.5
        if self.anim_start > self.frames:
            self.animated = False

AssasinDict = {'x':467,'y':175,'width':150,'height':400,'col':(255,255,255),'frames':21,
               'path':'assasin_animation','text':'The Wannabe Assasin','rect_x':547,
               'rect_y':215,'text_pos':(500,150)}

RobotDict = {'x':342,'y':175,'width':350,'height':440,'col':(255,255,255),'frames':9,
               'path':'robo_animation','text':'The Slow Robot','rect_x':492,
               'rect_y':175,'text_pos':(500,100)}

assasin = Character(AssasinDict,playerT_animate)
robot = Character(RobotDict,playerR_animate)



pressed = 0
profiles = [assasin,robot]
    
        
Kindex = 0    
def drawProfiles():
    profiles[Kindex].draw()
    profiles[Kindex].animate()
    
def collisions():
      if mbox.colliderect(profiles[Kindex].rct) and event.type == pygame.MOUSEBUTTONDOWN:
            profiles[Kindex].anim_start = 0
            profiles[Kindex].animated = True
    
#mainloop
buttonloop = 0
RUN = True 
while RUN:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

    keys = pygame.key.get_pressed()
    if buttonloop == 13:
        buttonloop = 0
    if buttonloop == 0:
        if keys[pygame.K_SPACE]:
            if Kindex == len(profiles) -1:
                Kindex = 0
            else:
                Kindex += 1
    buttonloop += 1
    mx,my = pygame.mouse.get_pos()
    mbox = pygame.Rect(mx,my,10,17)
    collisions()
    SCREEN.fill((210,210,210))
    pygame.draw.rect(SCREEN,(0,0,0),(0,0,1370,700),5)
    
 
    drawProfiles()
    pygame.display.update()
    CLOCK.tick(FPS)

pygame.quit()
