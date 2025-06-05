import pygame

# Setup
pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

# window display settings
pygame.display.set_icon(pygame.image.load("assets/graphics/egg/egg_1.png"))
pygame.display.set_caption("Placeholder")

# initial loop setup
isrunning = True # initiates main loop
isinmenu = True # enters menu load loop
ismenuloaded = False # forces first menu load

# # load music
# pygame.mixer.init()
# pygame.mixer.music.load("assets/music/1.mp3")

while isrunning:
    while isinmenu:
        while not ismenuloaded: # menu asset loader
            # reloadS variables
            # invalid catcher
            screen.fill("#B00BA5")
            # menu status conditionals
            ismenuinteract = False
            isquitloaded = False
            # variable initialization
            menu_select = 0
            quit_select = True
            ismenuloaded = True
            isinmenu =True

            # font loader
            title_font = pygame.font.Font(pygame.font.get_default_font(),50)
            # menu font
            fontsize_1 = fontsize_2 = fontsize_3 = 20
            menu_font1 = pygame.font.Font(pygame.font.get_default_font(),fontsize_1)
            menu_font2 = pygame.font.Font(pygame.font.get_default_font(),fontsize_2)
            menu_font3 = pygame.font.Font(pygame.font.get_default_font(),fontsize_3)
            # Title
            surf_title = title_font.render("Placeholder", True, "White")
            rect_title = surf_title.get_rect(topleft=(50,75))
            # Menu1
            surf_1 = menu_font1.render("Play", True, "White")
            rect_1 = surf_1.get_rect(topleft=(50,200))
            # Menu 2
            surf_2 = menu_font2.render("Settings", True, "White")
            rect_2 = surf_2.get_rect(topleft=(50,250))
            # Menu 3
            surf_3 = menu_font3.render("Exit", True, "White")
            rect_3 = surf_3.get_rect(topleft=(50,300))
            print("menu loaded",ismenuloaded)
            pygame.display.update()

        while ismenuloaded:
            # if isquitloaded: # quit menu
            #     for event in pygame.event.get():
            #     # pygame.QUIT --> user clicked X to close your window
            #         if event.type == pygame.QUIT:
            #             isrunning = False
            #         if event.type == pygame.KEYUP:
            #             if event.key == pygame.K_w and quit_select: #cycle left
            #                 quit_select = not quit_select
            #                 ismenu_updated = True
            #             if event.key == pygame.K_s and not quit_select: #cycle right
            #                 quit_select = not quit_select
            #                 ismenu_updated = True
            #             if event.key == pygame.K_RETURN and quit_select:
            #                 isquitloaded = False
            #             else:
            #                 isrunning = False
            screen.fill("#B00BA5")
            for event in pygame.event.get():
                # pygame.QUIT --> user clicked X to close your window
                if event.type == pygame.QUIT:
                    isrunning = False
                if event.type == pygame.KEYUP:
                    print(event)
                    if event.key == pygame.K_w and menu_select > 0: #cycle up
                        menu_select -= 1
                        ismenu_updated = True
                    if event.key == pygame.K_s and menu_select < 2: #cycle down
                        menu_select += 1
                        ismenu_updated = True
                    if event.key == pygame.K_RETURN:
                        ismenuinteract = True
                    print(event.key)
                    print(menu_select)

            # if ismenuinteract:
            #     if menu_select == 0: # Play
            #         ismenuloaded = False
            #         isqueueloaded = True
            #     elif menu_select == 1: # Settings
            #         isquitloaded = True
            #     else: #exit
            #         isrunning = False
                    # open exit splash and then exits
                # ismenuinteract = False

            # take menu inputs
            # have it modify the font size value directly instead of shoving a variable in?
            if menu_select == 0 and fontsize_1 < 60: # start resize
                fontsize_1+=2
                print("f1",fontsize_1)
            if menu_select != 0 and 20 < fontsize_1: #might be able to simplify?
                fontsize_1-=1
                print("f1",fontsize_1)

            if menu_select == 1 and fontsize_2 < 60: # settings resize
                fontsize_2+=2
                print("f2",fontsize_2)
            if menu_select != 1 and 20 < fontsize_2: #might be able to simplify?
                fontsize_2-=1
                print("f2",fontsize_2)

            if menu_select == 2 and fontsize_3 < 60: # exit resize
                fontsize_3+=2
                print("f3",fontsize_3)
            if menu_select != 2 and 20 < fontsize_3: #might be able to simplify?
                fontsize_3-=1
                print("f3",fontsize_3)

            pygame.font.Font.set_point_size(menu_font1,fontsize_1)
            pygame.font.Font.set_point_size(menu_font2,fontsize_2)
            pygame.font.Font.set_point_size(menu_font3,fontsize_3)
            screen.blits(((surf_title,rect_title),(surf_1,rect_1),(surf_2,rect_2),(surf_3,rect_3))) #//selective reblitting? have all updated objects be placed in a tuple list?
            pygame.display.update()
pygame.display.update()


        # make the text an object that takes inputs,
# while isinmenu:
        # game_font
        # 0 = play, 1 = settings, 2 = exit
        # selectedbutton = 0
        # ui shit
clock.tick(10)
    # print("Hwrld")
