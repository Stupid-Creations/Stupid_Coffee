from PyCinno import *

clock = pygame.time.Clock()

#12,10 12,11

maps = [["KKKKBSSSSSSSSD"],
        ["ASSSNSSSSSSSSD"],
        ["ASSSNSSSSSSSSD"],
        ["ASSSNSSSSSSSSD"],
        ["ASSSNSSSSSSSSD"],
        ["ASSSNSSSSSSSSD"],
        ["ASSSNSSSSSSSSD"],
        ["ASSSNSSSSSSSSD"],
        ["ASSSNSSSSSSSSD"],
        ["ASSSNSSSSSSSSD"],
        ["ASSSNSSSSSSSSD"],
        ["ASSSNSSSSSSSSD"],
        ["ASSSNSSSSSSSSD"],
        ["ASSSNSSSSSSSSD"],
        ["ASSSMSSSSSSSSD"]]

class drink(character):
    def __init__(self,sprites,shape,coords,scale=1):
        character.__init__(self,sprites,shape,coords,scale,is_solid=False)
        self.toppings = {"milk":0}
        self.adder = False
        #MAKE THE TOPPINGS THING A LIST LIKE [0,TRUE] where the bool is the adder state for the topping
    def increment(self,topping):
        if self.adder:
            self.toppings[topping]+=1
#SPRITE DEETS: 15X25 size!! 6 y gap between layers
xoff = 200
counter = 0
aniturtle = 0
# main loop to run the game
char = character("helpme.png",(15,25),(50,200),2)
char.save_sprites(4,4,(2,40),6)
char.create_sheet_bindings(["front","right","back","left"])
char.set_current_sprite(0,label='front')

char1 = character("helpme.png",(15,25),(200,200),2)
char1.save_sprites(4,4,(2,40),6)
char1.create_sheet_bindings(["front","right","back","left"])
char1.set_current_sprite(0,label='front')
#add other stuff like better motion, with smoothing, probably w lerp (can also just use step wise increment)
# also add spritesheet display
small = character(None,(40,60),(20,60),1)
medium = character(None,(50,70),(100,50),1)
large = character(None,(60,80),(180,40),1)
milk = character(None,(60,100),(300,20),1)
drink = drink(None,(60,100),(-123,1230),1)
tiles = []

for i in range(len(maps)):
    for j in range(len(maps[i][0])):
        if maps[i][0][j] == "A":
            tiles.append(character(("Tilesheets/roguelikeIndoor_transparent.png"),(16,16),(j*32,i*32),2,is_solid=False))
            tiles[-1].save_sprites(1,1,(17*23,0),1)
            tiles[-1].set_current_sprite(0,y=0)
        if maps[i][0][j] == "S":
            tiles.append(character(("Tilesheets/roguelikeIndoor_transparent.png"),(16,16),(j*32,i*32),2,is_solid=False))
            tiles[-1].save_sprites(1,1,(17*24,0),1)
            tiles[-1].set_current_sprite(0,y=0)
            a = pygame.transform.rotate(tiles[-1].sprites[0][0], -45)
            tiles[-1].sprites[0][0] = a
            b = tiles[-1].sprites[0][0]
        if maps[i][0][j] == "D":
            tiles.append(character(("Tilesheets/roguelikeIndoor_transparent.png"),(16,16),(j*32,i*32),2,is_solid=False))
            tiles[-1].save_sprites(1,1,(17*25,0),1)
            tiles[-1].set_current_sprite(0,y=0)
            tiles[-1].sprites[0][0] = pygame.transform.rotate(tiles[-1].sprites[0][0],45)
        if maps[i][0][j] == "B":
            tiles.append(character(("Tilesheets/roguelikeIndoor_transparent.png"),(16,16),(j*32,i*32),2))
            tiles[-1].save_sprites(1,1,(17*10,17*12),1)
            tiles[-1].set_current_sprite(0,y=0)
            tiles[-1].sprites[0][0] = pygame.transform.rotate(tiles[-1].sprites[0][0],45)
        if maps[i][0][j] == "N":
            tiles.append(character(("Tilesheets/roguelikeIndoor_transparent.png"),(16,16),(j*32,i*32),2))
            tiles[-1].save_sprites(1,1,(17*10,17*13),1)
            tiles[-1].set_current_sprite(0,y=0)
        if maps[i][0][j] == "M":
            tiles.append(character(("Tilesheets/roguelikeIndoor_transparent.png"),(16,16),(j*32,i*32),2))
            tiles[-1].save_sprites(1,1,(17*11,17*12),1)
            tiles[-1].set_current_sprite(0,y=0)
        if maps[i][0][j] == "K":
            tiles.append(character(("Tilesheets/roguelikeIndoor_transparent.png"),(16,16),(j*32,i*32),2))
            tiles[-1].save_sprites(1,1,(16*19,18*2),1)
            tiles[-1].set_current_sprite(0,y=0)

render=False

wn = pygame.display.set_mode((450,450))
scene = 1

while True:
    wn.fill((255,255,255))
    keys = pygame.key.get_pressed()
    if scene == 0:
        for i in tiles:
            i.display_sprite(wn)
        handle_text(wn,5,text_offset=(20,30))

        char.display_sprite(wn)
        char1.display_sprite(wn)

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
    if scene == 1:
        if keys[pygame.K_RIGHT] and xoff < 600:
            xoff += 5
        if keys[pygame.K_LEFT] and xoff > 200:
            xoff-=5

        mouse_pos = pygame.mouse.get_pos()
        mouseRect = pygame.Rect(mouse_pos[0]-12.5,mouse_pos[1]-12.5,25,25)

        small.display_sprite(wn)
        medium.display_sprite(wn)
        large.display_sprite(wn)
        milk.display_sprite(wn)

        temp_surf = wn.copy()
        wn.fill((255,255,255))
        wn.blit(temp_surf,(200-xoff,0))

        pygame.draw.rect(wn,(255,125,0),mouseRect)
        if render:
            drink.display_sprite(wn)


    # temp_surf = wn.copy()
    # wn.fill((0,0,0))
    # wn.blit(temp_surf,(200-char.Rect.x,200-char.Rect.y))
    # handle_text(wn,5,text_offset=(20,30)) #ADD THIS AFTER THE DISPLACEMENT OF SPRITES ABOVE

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                if scene == 0 and char.check_adjacent(tiles[17]):
                    char1.speak_several(["Hello","Raghav is very very stupid","I pity him"])
                if scene == 0 and char.check_adjacent(tiles[0]) or char.check_adjacent(tiles[1]) or char.check_adjacent(tiles[2]) or char.check_adjacent(tiles[3]) or char.check_adjacent(tiles[4]):
                    scene = 1
        if event.type == pygame.MOUSEBUTTONDOWN and scene == 1:
            if mouseRect.colliderect(small.Rect):
                render = True
                drink.Rect.x = 300
                drink.Rect.y = 300    
                drink.Rect.width,drink.Rect.height = small.Rect.width,small.Rect.height        
            if mouseRect.colliderect(medium.Rect):
                render = True
                drink.Rect.x = 300
                drink.Rect.y = 300    
                drink.Rect.width,drink.Rect.height = medium.Rect.width,medium.Rect.height  
            if mouseRect.colliderect(large.Rect):
                render = True
                drink.Rect.x = 300
                drink.Rect.y = 300    
                drink.Rect.width,drink.Rect.height = large.Rect.width,large.Rect.height
            if mouseRect.colliderect(milk.Rect):
                drink.adder=True
                drink.increment("milk")
                print(drink.toppings['milk'])

    pygame.display.update()
    clock.tick(60)
