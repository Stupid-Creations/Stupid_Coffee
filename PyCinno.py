import pygame
import sys

pygame.init()
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
        self.render=False
        self.currentlog = 0
        self.dialogue=None
        self.dbox = dialogbox("",(450,450),30,imgsource="textbox.jpg",font="pkmnfl.ttf")
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
        self.Rect.x += change[0]*self.scale*self.shape[0]/8
        self.Rect.y += change[1]*self.scale*self.shape[1]/8
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
    def speak(self,dialogue):
        self.dialogue = dialogue
        self.dbox.update_text(dialogue)
        self.render = True
    def rendertext(self,surface,text_strobe_rate = 5, text_offset = (0,0)):
        if self.render:
            self.dbox.render_strobe(surface,(0,int(3/4*surface.get_height())),text_strobe_rate,offset=text_offset)
    def speak_several(self,dialogues):
        if self.currentlog < len(dialogues):
            self.dialogues = dialogues
            self.speak(dialogues[self.currentlog])
            self.currentlog+=1
        else:
            self.render = False
    def check_adjacent(self,char):
        return self.Rect.bottom == char.Rect.top or self.Rect.top == char.Rect.bottom or self.Rect.left == char.Rect.right or self.Rect.right == char.Rect.left
    
def handle_text(surface,text_strobe_rate=5,text_offset=(0,0)):
    for i in character.instances:
        if i.dialogue:
            i.rendertext(surface,text_strobe_rate,text_offset)


#add nice looking dialogue box (pictures)
#add strobing
class dialogbox: 
    def __init__(self,text,windim,size=36,font = None,imgsource = None):
        self.text = text
        self.anitimer = 0
        self.width = windim[0] 
        self.size = size
        self.font = pygame.font.Font(font=font,size=size)
        self.ts = self.font.render(self.text,True,(255,255,255))
        self.lines = self.wrap_text(self.text,self.width-20)
        self.height = sum([self.font.size(i)[1]*2 for i in self.lines])
        self.add = 0
        self.cl = 0
        self.done = False
        self.stroby_text = [[""] for i in self.lines]
        self.fontsource = font
        if imgsource is None:
            self.img = None
            self.imsource = None
        else:
            self.imsource = imgsource
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
        if self.cl >= len(self.lines):
            self.done = True
        if self.img is None:
            pygame.draw.rect(screen,(125,255,0),pygame.Rect(x,originaly,self.width,self.height))
        else:
            screen.blit(pygame.transform.scale(self.img,(self.width,max(self.height+offset[1],screen.get_height()/4))),(x-offset[0],originaly-offset[1]))
        if self.anitimer >= fbu and not self.done:
            if self.add >= len(self.lines[self.cl]):
                self.add = 0
                self.cl+=1
                if self.cl >= len(self.lines):
                    self.done = True  
            if not self.done:  
                self.stroby_text[self.cl]+=self.lines[self.cl][self.add]
                self.anitimer = 0
                self.add+=1

        for line in self.stroby_text:
            screen.blit(self.font.render(''.join(line),True,(0,0,0)),(x,y))
            y+=self.font.get_height()*2+10
    def update_text(self,newtext):
        self.text = newtext
        self.ts = self.font.render(self.text,True,(255,255,255))
        self.lines = self.wrap_text(self.text,self.width-20)
        self.height = sum([self.font.size(i)[1]*2 for i in self.lines])
        self.stroby_text = [[""] for i in self.lines]
        self.done = False
        self.anitimer = 0
        self.add = 0
        self.cl = 0
    

        





