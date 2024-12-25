from PyCinno import *

clock = pygame.time.Clock()


maps = [["AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"] for _ in range(15)]
#SPRITE DEETS: 15X25 size!! 6 y gap between layers

counter = 0
aniturtle = 0
# main loop to run the game
char = character("helpme.png",(15,25),(200,200),2)
char.save_sprites(4,4,(2,40),6)
char.create_sheet_bindings(["front","right","back","left"])
char.set_current_sprite(0,label='front')

char1 = character("helpme.png",(15,25),(200,200),2)
char1.save_sprites(4,4,(2,40),6)
char1.create_sheet_bindings(["front","right","back","left"])
char1.set_current_sprite(0,label='front')
#add other stuff like better motion, with smoothing, probably w lerp (can also just use step wise increment)
# also add spritesheet display
tiles = []
for i in range(len(maps)):
    for j in range(len(maps[i][0])):
        if maps[i][0][j] == "A":
            tiles.append(character(("grass.png"),(32,32),(j*32,i*32),1,is_solid=False))
            tiles[-1].save_sprites(1,1,(0,0),0)
            tiles[-1].set_current_sprite(0,y=0)
        if maps[i][0][j] == "B":
            tiles.append(character(("brick.png"),(32,32),(j*32,i*32),1))
            tiles[-1].save_sprites(1,1,(0,0),0)
            tiles[-1].set_current_sprite(0,y=0)

#a = dialogbox("THIS IS A REALLY REALLY STUPID PROJECT I DONT REALLY KNOW WHAT TO WRITE AHHH",(450,450),30,imgsource="textbox.jpg",font="pkmnfl.ttf")
render=False

wn = pygame.display.set_mode((450,450))

while True:
    wn.fill((255,255,255))
    for i in tiles:
        i.display_sprite(wn)
    char.display_sprite(wn)
    char1.display_sprite(wn)
    temp_surf = wn.copy()
    wn.fill((0,0,0))
    wn.blit(temp_surf,(200-char.Rect.x,200-char.Rect.y))
    handle_text(wn,5,text_offset=(20,30))
    #a.render_strobe(wn,(0,300),5,offset=(20,30))
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                if char.Rect.bottom == char1.Rect.top or char.Rect.top == char1.Rect.bottom or char.Rect.right == char1.Rect.left or char.Rect.left==char1.Rect.right:
                    char1.speak_several(["Hello","Raghav is very very stupid","I pity him"])

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
