
import pygame
from pygame.locals import QUIT, K_LEFT, K_RIGHT, K_SPACE, Rect
from pygame.gfxdraw import rectangle
import math 

import pandas
import csv



with open('TrainingData.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

new = {}
for i in data[1:]:
    a = str(i[:5])
    b = i[-3:-1]
    
    new.update({a:b})

pygame.init()
vec = pygame.math.Vector2    # 2 for two dimensional

 
HEIGHT = 600
WIDTH = 600
FPS = 60

FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode([WIDTH, HEIGHT])
displaysurface.fill([255,255,255])

pygame.display.set_caption("Game")
pygame.display.update()
class Player(pygame.sprite.Sprite):
        def __init__(self):
                super().__init__() 
                self.rotation = 180
                self.dr = 0
                self.vroom = False
                self.surf = pygame.Surface((15, 25))
                self.color = (255,0,0)
                self.surf.fill(self.color)
                self.surf.set_colorkey((255,255,255)) 
                self.rect = self.surf.get_rect(center = (30, 420))
                self.pos = vec((300 - 15/2,0 - 25/2))
                self.vel = vec(0,0)
                
        
        def setDr(self, dr):
                self.dr = dr
        def getDr(self):
                return(self.dr)
        def setDx(self, dx):
                self.vel[0] = dx
        def getDx(self):
                return(self.vel[0])                
        def setDy(self, dy):
                self.vel[1] = dy
        def getDy(self):
                return(self.vel[1])
        
        def setX(self, x):
                self.pos[0] = x
        def getX(self):
                return(self.pos[0])
        def setY(self, y):
                self.pos[1] = y
        def getY(self):
                return(self.pos[1])
        
        def setVroom(self, b):
                self.vroom = b
        def getVroom(self):
                return(self.vroom)
        
        def setPos(self, x, y):
                self.pos = (x,y)
        def getPos(self):
                return(self.pos)
        
        def update(self):
                
                self.rotation += self.dr
                mu = 1/2
                self.vel = vec(math.sin(math.radians(int(-self.rotation))) * mu, math.cos(math.radians(int(-self.rotation)))*mu)
        
                m = 1
                if self.vroom:
                        m *= 2
                        self.vel *= 2
                '''
                if self.vel[0] > m * math.sin(math.radians(-self.rotation)) and -self.vel[0] < -m * math.sin(math.radians(-self.rotation)) :
                        self.vel[0] = m * math.sin(math.radians(-self.rotation))
                if self.vel[1] > m * math.sin(math.radians(-self.rotation)) and -self.vel[1] < -m * math.cos(math.radians(-self.rotation)) :
                        self.vel[1] = m * math.cos(math.radians(-self.rotation))
                '''
                self.pos[0] += self.vel[0] * 10
                self.pos[1] -= self.vel[1] * 10
                
        def move(self):
                #self.vel = vec(0,0)
                self.rotation += self.dr
                
                #self.pos = vec(self.pos[0] + self.vel[0], self.pos[1] + self.vel[1])

                self.rect = self.surf.get_rect()
                self.rect.center = (300, 300)    

                old_center = self.rect.center    
                self.new_image = pygame.transform.rotate(self.surf, int(self.rotation))    
                self.rect = self.new_image.get_rect()    
                self.rect.center = old_center    

        def repaint(self):
                displaysurface.blit(self.new_image , self.rect)    
class Block(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h, c):
                super().__init__() 
                self.surf = pygame.Surface((w, h))
                self.color = c
                self.surf.fill(self.color)
                
                
                self.w = w
                self.h = h
                self.surf.set_colorkey((255,255,255)) 
                self.rect = self.surf.get_rect(center = (x, y))
                
                self.aPos = vec(x,y)
                self.rPos = vec(0,0)
        
        
        def getRectangle(self):
                return(Rect(self.aPos[0] + self.rPos[0] - self.w/2, self.aPos[1] + self.rPos[1] - self.h/2, self.w, self.h))
                
        def setPosition(self, x, y):
                self.rPos = (x,y)
                self.rect = self.surf.get_rect(center = (self.aPos + self.rPos))
        def setLoc(self, x ,y):
                self.rPos = (x,y)
                self.rect = self.surf.get_rect(center = (self.rPos))

        def getPosition(self):
                return(vec(self.aPos + self.rPos))
        def getRel(self):
                return(self.rPos)
        def setRel(self, x, y):
                self.rPos = (x,y)

player = Player()
all_sprites = pygame.sprite.Group()
#all_sprites.add(player)
characters = []
blocks = []
disTesters = []
for i in range(5):
        temp = Block(displaysurface.get_width()/2 - 3, displaysurface.get_height()/2 - 3, 6, 6, [255,0,0])
        all_sprites.add(temp)
        disTesters.append(temp)
players = []

center = Block(300,300, 6, 6, (0,0,0))
all_sprites.add(center)
lines = []
with open("HairPin.txt", "r") as f:
        lines = f.readlines()
new = []
for i in lines:
        new.append( "".join(i).replace("\t", "").replace("\n", "").replace(" ", "") )
w = 50
for i in range(len(new)):
        for j in range(len(new[i])):
                if (new[i][j] == "0"):                        
                        b = Block(j*w-300, i*w-500, w, w, (0,0,0))
                        blocks.append(b)
                        all_sprites.add(b)

                        
def checkDistanceToWall(part, ang):
        part.setLoc(displaysurface.get_width()/2, displaysurface.get_height()/2)
        ang %= 360
        ang *= -1
        
        
        per = 30
        i = 0
        
        while( i < per ): 
        
                i += 1

                part.setLoc(part.getRel()[0] + math.cos(math.radians(ang)) * i, part.getRel()[1] + math.sin(math.radians(ang)) * i)
                for b in blocks:         
                        p = b.getPosition()
                        if p[0] < 600 and p[0] > 0 and p[1] < 600 and p[1] > 0:    
                                r = (b.getRectangle())
                                if(r.collidepoint(part.getRel()[0]+part.w/2, part.getRel()[1]+part.h/2)):
                                        return(i)                
        return(100)
frames = 0
end = False        

while not end:
        
        for event in pygame.event.get():
                if event.type == QUIT:
                        pygame.quit()
        temp = []
        if(frames == 0):
                arr = player.rotation + 180
                for b in disTesters:
                    temp.append(checkDistanceToWall(b, arr, player))
                    arr -= 45
                        
                frames = 1
        frames -=    1
        pressed_keys = pygame.key.get_pressed()
        
        if pressed_keys[K_LEFT]:
                
                player.setDr(2)
                temp.append(-1)
                
        elif pressed_keys[K_RIGHT]:
                
                player.setDr(-2)
                temp.append(1)
        else:
                player.setDr(0)
                temp.append(0)
        if pressed_keys[K_SPACE]:
                player.setVroom(True)
                temp.append(1)
        else:
                player.setVroom(False)
                temp.append(0)
        if not (temp in data):
            data.append(temp)
        
        player.update()
        player.move()
        
        
        for entity in blocks:
            entity.setPosition(-player.getPos()[0], -player.getPos()[1])
        for entity in blocks:        
            if(entity.getRectangle().collidepoint(center.rect.center)):
                #'''
                df = pandas.DataFrame(data[0:-20],columns=['L','FL','F','FR','R','Turn','Vroom'])
                df.to_csv('TrainingData.csv')
                print('done')
                end = True
                player.rotation += 180
                player.update()
                player.rotation += 180
                        #'''
                        #end = True
                        #player.move
         
                 
        displaysurface.fill([255,255,255])
        for entity in blocks:
                displaysurface.blit(entity.surf, entity.rect)
        for entity in disTesters:
                displaysurface.blit(entity.surf, entity.rect)
 
        player.repaint()
        displaysurface.blit(center.surf, center.rect)
        
        
        pygame.display.update()
        FramePerSec.tick(FPS)
