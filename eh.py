from PyCinno import *
#make a clock, also add another way of rendering text
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
