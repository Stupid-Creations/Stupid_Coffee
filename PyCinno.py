import pygame
import sys

pygame.font.init()
class SpriteSheet:
    def __init__(self,image):
        self.sheet = pygame.image.load(image)
    def return_sprite(self,Rect,size=None):
        rect = pygame.Rect(Rect)
        surf = pygame.Surface(rect.size)
        surf.blit(self.sheet,(0,0),rect)
        if size is not None:
            surf = pygame.transform.scale(surf,size)
        return surf
    def get_sprites(self,rect,n_sprites,size=None):
        return [self.return_sprite((rect[0]+(rect[2]*i),rect[1],rect[2],rect[3]),size) for i in range(n_sprites)]
    
class character:
    instances = []
    def __init__(self,sprites,shape,coords,scale,is_solid = True):
        self.spritesheet = SpriteSheet(sprites)
        self.shape = shape
        self.current_sprite = None
        self.counter = None
        self.anitimer = 0
        self.scale = scale
        self.solid = is_solid
        self.Rect = pygame.Rect(coords[0],coords[1],self.shape[0]*scale,self.shape[1]*scale)
        if is_solid:
            character.instances.append(self)

    def save_sprites(self,n_vertical,n_horizontal,start,gap):
        sprites = [self.spritesheet.get_sprites((start[0],start[1]+(self.shape[1]*i)+(gap*i),self.shape[0],self.shape[1]),n_horizontal) for i in range(n_vertical)]
        self.sprites = [[pygame.transform.scale(i,(self.shape[0]*self.scale,self.shape[1]*self.scale)) for i in j] for j in sprites]

    def display_spritesheet(self,surface):
       surface.blit(self.spritesheet.sheet,(0,0))

    def set_current_sprite(self,x,y=None,label = None):
        if label is not None:
            if type(self.sprites) != dict:
                raise ValueError("sprites are in list form")
            else:
                self.current_sprite = self.sprites[label][x]
                self.counter = x
                self.row = label
                return 
        self.current_sprite = self.sprites[y][x]
        self.row = y
        self.counter = x

    def animate(self,frames_before_update):            
        if self.counter >= len(self.sprites[self.row]):
            self.counter = 0
        self.set_current_sprite(self.counter,self.row)
        fbu = frames_before_update
        self.anitimer+=1
        if self.anitimer >= fbu:
            self.counter += 1
            self.anitimer = 0
            return 0
        return 1/frames_before_update
    
    def create_sheet_bindings(self,labels):
        if len(labels) != len(self.sprites):
            raise ValueError("Bindings not equal to number of sprites D:")
        self.sprites = {labels[i]:self.sprites[i] for i in range(len(labels))}
        self.labels = labels
        
    def display_sprite(self,surface):
        if self.current_sprite == None:
            raise ValueError("sprite not set")
        surface.blit(self.current_sprite,(self.Rect.x,self.Rect.y))

    def move(self,change):
        self.Rect.x += change[0]*self.scale
        self.Rect.y += change[1]*self.scale

        if self.solid:
            for i in character.instances:
                if self.Rect.colliderect(i.Rect) and i != self:
                    if change[0] > 0:
                        self.Rect.right = i.Rect.left
                    if change[0] < 0:
                        self.Rect.left = i.Rect.right
                    if change[1] > 0:
                        self.Rect.bottom = i.Rect.top
                    if change[1] < 0:
                        self.Rect.top = i.Rect.bottom

#add nice looking dialogue box (pictures)
#add strobing
class dialogbox:
    def __init__(self,text,windim,size=36,font = None,imgsource = None):
        self.text = text
        self.anitimer = 0
        self.width = windim[0] 
        self.font = pygame.font.Font(font=font,size=size)
        self.ts = self.font.render(self.text,True,(255,255,255))
        self.lines = self.wrap_text(self.text,self.width-20)
        self.height = sum([self.font.size(i)[1]*2 for i in self.lines])
        self.add = 0
        self.cl = 0
        self.stroby_text = [[""] for i in self.lines]
        if imgsource is None:
            self.img = None
        else:
            self.img = pygame.image.load(imgsource)
    def wrap_text(self,text,width):
        words = text.split(" ")
        lines = []
        current = [] #defines the list of words currently in use 
        for i in words:
            checker = ' '.join(current+[i])
            if self.font.size(checker)[0] < width:
                current.append(i) 
            else:
                lines.append(' '.join(current))
                current = [i]
        if current:
            lines.append(' '.join(current))
        return lines
    def render(self,screen,pos):
        x,y = pos
        for line in self.lines:
            final = ""
            for letter in line:
                final+=letter
                screen.blit(self.font.render(final,True,(255,255,255)),(x,y))
            y+=self.font.get_height()*2
    def render_strobe(self,screen,pos,fbu,offset=(0,0)):
        x,y = pos
        x+=offset[0]
        y+=offset[1]
        originaly = y
        self.anitimer += 1
        if self.img is None:
            pygame.draw.rect(screen,(125,255,0),pygame.Rect(x,originaly,self.width,self.height))
        else:
            screen.blit(pygame.transform.scale(self.img,(self.width,max(self.height+offset[1],screen.get_height()/4))),(x-offset[0],originaly-offset[1]))
        if self.anitimer >= fbu and ''.join(self.stroby_text[-1]) != self.lines[-1]:
            if self.add >= len(self.lines[self.cl]):
                self.add = 0
                self.cl+=1
            self.stroby_text[self.cl]+=self.lines[self.cl][self.add]
            self.anitimer = 0
            self.add+=1

        for line in self.stroby_text:
            screen.blit(self.font.render(''.join(line),True,(0,0,0)),(x,y))
            y+=self.font.get_height()*2+10


#make a clock
pygame.display.init()
clock = pygame.time.Clock()

wn = pygame.display.set_mode((450,450))

maps = [["A_A_A_A_A_A"],
        ["A_A_A_A_A_A"],
        ["A_A_A_A_A_A"],
        ["A_A_A_A_A_A"],
        ["A_A_A_A_A_A"]]
#SPRITE DEETS: 15X25 size!! 6 y gap between layers

counter = 0
aniturtle = 0
# main loop to run the game
char = character("helpme.png",(15,25),(200,200),2)
char.save_sprites(4,4,(2,40),6)
char.create_sheet_bindings(["front","right","back","left"])
char.set_current_sprite(0,label='front')

tiles = []
for i in range(len(maps)):
    for j in range(len(maps[i][0])):
        if maps[i][0][j] == "A":
            tiles.append(character(("helpme.png"),(15,25),(j*char.scale*char.shape[0],i*char.scale*char.shape[1]),2))
            tiles[-1].save_sprites(4,4,(2,40),6)
            tiles[-1].create_sheet_bindings(["front","right","back","left"])
            tiles[-1].set_current_sprite(0,label='front')

a = dialogbox("THIS IS A REALLY REALLY STUPID PROJECT I DONT REALLY KNOW WHAT TO WRITE AHHH",(450,450),30,imgsource="textbox.jpg",font="pkmnfl.ttf")

while True:
    wn.fill((0,0,0))
    for i in tiles:
        i.display_sprite(wn)
    char.display_sprite(wn)
    a.render_strobe(wn,(0,300),5,offset=(20,30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        if char.row!="right":
            char.set_current_sprite(0,label="right")
        char.animate(15)
        char.move((1,0))

    if keys[pygame.K_DOWN]:
        if char.row != "front":
            char.set_current_sprite(0,label="front")
        char.animate(15)
        char.move((0,1))

    if keys[pygame.K_UP]:
        if char.row != "back":
            char.set_current_sprite(0,label="back")
        char.animate(15)
        char.move((0,-1))

    if keys[pygame.K_LEFT]:
        char.animate(15)
        if char.row != "left":
            char.set_current_sprite(0,label="left")
        char.move((-1,0))

    pygame.display.update()
    clock.tick(60)

