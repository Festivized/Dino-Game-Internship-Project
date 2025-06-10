import pygame

'''
Todo
- selective reblitting to improve performance
- better structure
- finish tutorial
- draw the assets
- shadows/daynightcycle
    - dynamic shadows based on the sun?
    - transparant shading mask?
'''


# Setup
pygame.init()
screen = pygame.display.set_mode((800,400))
clock = pygame.time.Clock()

# window display settings
pygame.display.set_icon(pygame.image.load("assets/graphics/egg/egg_1.png"))
pygame.display.set_caption("Placeholder")

# initial loop setup
isrunning = True # initiates main loop
isinmenu = True # enters menu load loop
isingame = False # enters gameplay loop
ismenuloaded = False # forces first menu load
isgameloaded = False # forces game load
def close():
    # changes all runtime variables to False, exiting loop
    global isrunning
    global isinmenu
    global ismenuloaded
    isrunning = isinmenu = ismenuloaded = False

# # load music
# pygame.mixer.init()
# pygame.mixer.music.load("assets/music/1.mp3")

while isrunning:
    while isinmenu:
        while not ismenuloaded: # menu asset loader
            # reloads variables
            # invalid catcher
            screen.fill("#B00BA5")
            # menu status conditionals
            ismenuinteract = False
            isquitloaded = False
            ismenuloaded = True
            isinmenu =True
            # variable initialization
            menu_select = 0
            quit_select = True

            # font loader
            title_font = pygame.font.Font(pygame.font.get_default_font(),50)
            # menu font
            fontsize_1 = fontsize_2 = fontsize_3 = 20
            # Title
            surf_title = title_font.render("Placeholder", True, "White")
            rect_title = surf_title.get_rect(topleft=(50,75)) # topleft=(50,75)
            # Menu rect init
            # rect_1 = surf_1.get_rect(center=(71,211)) # topleft=(50,200)
            # rect_2 = surf_2.get_rect(center=(92,261)) # topleft=(50,250)
            # rect_3 = surf_3.get_rect(center=(69,311)) # topleft=(50,300)
            print("menu loaded",ismenuloaded)
            pygame.display.update()
        while ismenuloaded:
            for event in pygame.event.get():
                # pygame.QUIT --> user clicked X to close your window
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYUP:
                    print("event",event)
                    if event.key == pygame.K_w and menu_select > 0: #cycle up
                        menu_select -= 1
                        ismenu_updated = True
                    if event.key == pygame.K_s and menu_select < 2: #cycle down
                        menu_select += 1
                        ismenu_updated = True
                    if event.key == pygame.K_RETURN:
                        print("kreturn")
                        if menu_select == 0: # Play
                            ismenuloaded = False
                            isinmenu = False
                            isingame = True
                        elif menu_select == 1: # Settings
                            close()
                        else: #exit
                            close()
                    # for troubleshooting
                    # print("event key",event.key)
                    # print("menu index",menu_select)

            # take menu inputs
            # have it modify the font size value directly instead of shoving a variable in?
            if menu_select == 0:
                if fontsize_1 < 30: # start resize
                    fontsize_1+=1
                    # print("f1",fontsize_1)
            elif 20 < fontsize_1: #might be able to simplify?
                fontsize_1-=1
                # print("f1",fontsize_1)

            if menu_select == 1:
                if fontsize_2 < 30: # settings resize
                    fontsize_2+=1
                    # print("f2",fontsize_2)
            elif 20 < fontsize_2: # might be able to simplify?
                fontsize_2-=1
                # print("f2",fontsize_2)

            if menu_select == 2:
                if fontsize_3 < 30: # exit resize
                    fontsize_3+=1
                    # print("f3",fontsize_3)
            elif 20 < fontsize_3: # might be able to simplify?
                fontsize_3-=1
                # print("f3",fontsize_3)

            # menu renderer
            clock.tick(100)
            screen.fill("#B00BA5") #// holy shit calamity reference
            menu_font1 = pygame.font.Font(pygame.font.get_default_font(),fontsize_1)
            menu_font2 = pygame.font.Font(pygame.font.get_default_font(),fontsize_2)
            menu_font3 = pygame.font.Font(pygame.font.get_default_font(),fontsize_3)
            surf_1 = menu_font1.render("Play", True, "White")
            surf_2 = menu_font2.render("Settings", True, "White")
            surf_3 = menu_font3.render("Exit", True, "White")
            rect_1 = surf_1.get_rect(midleft=(50,211)) # topleft=(50,200)
            rect_2 = surf_2.get_rect(midleft=(50,261)) # topleft=(50,250)
            rect_3 = surf_3.get_rect(midleft=(50,311)) # topleft=(50,300)
            # screen.blit(surf_1,rect_1)
            screen.blits(((surf_title,rect_title),(surf_1,rect_1),(surf_2,rect_2),(surf_3,rect_3)))
            # print(screen.blits(((surf_title,rect_title),(surf_1,rect_1),(surf_2,rect_2),(surf_3,rect_3)),doreturn=True)) #// selective reblitting? have all updated objects be placed in a tuple list?
            pygame.display.flip()
    while isingame:
        while not isgameloaded: # game (re)loader
            # Game state variables
            GROUND_Y = 300  # The Y-coordinate of the ground level
            JUMP_GRAVITY_START_SPEED = -20  # The speed at which the player jumps
            players_gravity_speed = 0  # The current speed at which the player falls
            # Load level assets
            SKY_SURF = pygame.image.load("assets/graphics/level/sky.png").convert()
            GROUND_SURF = pygame.image.load("assets/graphics/level/ground.png").convert()
            game_font = pygame.font.Font(pygame.font.get_default_font(), 50)
            score_surf = game_font.render("SCORE?", False, "Black")
            score_rect = score_surf.get_rect
            # Load sprite assets
            player_surf = pygame.image.load("assets/graphics/player/player_walk_1.png").convert_alpha()
            player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))
            egg_surf = pygame.image.load("assets/graphics/egg/egg_1.png").convert_alpha()
            egg_rect = egg_surf.get_rect(bottomleft=(800, GROUND_Y))


        while isgameloaded:
                    for event in pygame.event.get():
                        # pygame.QUIT --> user clicked X to close your window
                        if event.type == pygame.QUIT:
                            close()
                        if event.type == pygame.KEYUP:
                            print("event",event)
                            if event.key == pygame.K_w and menu_select > 0: #cycle up
                                menu_select -= 1
                                ismenu_updated = True
                            if event.key == pygame.K_s and menu_select < 2: #cycle down
                                menu_select += 1
                                ismenu_updated = True
                            if event.key == pygame.K_RETURN:
                                print("kreturn")
                                if menu_select == 0: # Play
                                    ismenuloaded = False
                                    isinmenu = False
                                    isingame = True
                                elif menu_select == 1: # Settings
                                    close()
                                else: #exit
                                    close()
                            # for troubleshooting
                            # print("event key",event.key)
                            # print("menu index",menu_select)
                    for event in pygame.event.get():
                    # pygame.QUIT --> user clicked X to close your window
                    if event.type == pygame.QUIT:
                        running = False

                    elif is_playing:
                        # When player wants to jump by pressing SPACE
                        if (
                                event.type == pygame.KEYDOWN
                                and event.key == pygame.K_j
                                or event.type == pygame.K_f
                        ) and player_rect.bottom >= GROUND_Y:
                            players_gravity_speed = JUMP_GRAVITY_START_SPEED
                    else:
                        # When player wants to play again by pressing SPACE
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            is_playing = True
                            egg_rect.left = 800

                if is_playing:
                    screen.fill("purple")  # Wipe the screen

                    # Blit the level assets
                    screen.blit(SKY_SURF, (0, 0))
                    screen.blit(GROUND_SURF, (0, GROUND_Y))
                    # pygame.draw.rect(screen, "#c0e8ec", score_rect)
                    # pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
                    screen.blit(score_surf, score_rect)

                    # Adjust egg's horizontal location then blit it
                    egg_rect.x -= 5
                    if egg_rect.right <= 0:
                        egg_rect.left = 800
                    screen.blit(egg_surf, egg_rect)

                    # Adjust player's vertical location then blit it
                    players_gravity_speed += 1
                    player_rect.y += players_gravity_speed
                    if player_rect.bottom > GROUND_Y:
                        player_rect.bottom = GROUND_Y
                    screen.blit(player_surf, player_rect)

                    # When player collides with enemy, game ends
                    if egg_rect.colliderect(player_rect):
                        is_playing = False

                # When game is over, display game over message
                else:
                    screen.fill("black")

                # flip() the display to put your work on screen
                pygame.display.flip()

                clock.tick(100)  # Limits game loop to 60 FPS
pygame.display.flip()