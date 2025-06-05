import pygame

# Setup
pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
ismenuloaded = False
isrunning = True

# window display settings
pygame.display.set_icon(pygame.image.load("assets/graphics/egg/egg_1.png"))
pygame.display.set_caption("Placeholder")

#load music
pygame.mixer.init()
pygame.mixer.music.load("assets/music/1.mp3")

# Constants
animsize = 50

while isrunning:
    while not ismenuloaded: # menu asset loader
        # invalid catcher
        screen.fill("#B00BA5")
        # menu status conditionals
        istextanim = False
        ismenuinteract = False
        isquitloaded = False
        # variable initialization
        menu_select = 0
        quit_select = True

        # font loader
        title_font = pygame.font.Font(pygame.font.get_default_font(),50)
        fontsize_1 = 20
        menu_font1 = pygame.font.Font(pygame.font.get_default_font(),fontsize_1)
        fontsize_2 = 20
        menu_font2 = pygame.font.Font(pygame.font.get_default_font(),fontsize_2)
        fontsize_3 = 20
        menu_font3 = pygame.font.Font(pygame.font.get_default_font(),fontsize_3)
        # Title
        title_surf = title_font.render("Placeholder", True, "White")
        title_rect = title_surf.get_rect(topleft=(50,75))
        screen.blit(title_surf,title_rect)
        # Menu1
        play_surf = menu_font1.render("Play", True, "White")
        play_rect = play_surf.get_rect(topleft=(50,200))
        screen.blit(play_surf,play_rect)
        # Menu 2
        settings_surf = menu_font2.render("Settings", True, "White")
        settings_rect = settings_surf.get_rect(topleft=(50,225))
        screen.blit(settings_surf,settings_rect)
        # Menu 3
        exit_surf = menu_font3.render("Exit", True, "White")
        exit_rect = exit_surf.get_rect(topleft=(50,250))
        screen.blit(exit_surf,exit_rect)
        # Finishes Initial Load
        ismenuloaded = True
        isinmenu =True
        print("menu loaded")
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

        for event in pygame.event.get():
            # pygame.QUIT --> user clicked X to close your window
            if event.type == pygame.QUIT:
                isrunning = False
            if event.type == pygame.KEYUP:
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

        if ismenuinteract:
            if menu_select == 0: # Play
                ismenuloaded = False
                isqueueloaded = True
            elif menu_select == 1: # Settings
                isquitloaded = True
            else: #exit
                isrunning = False
                # open exit splash and then exits
            # ismenuinteract = False

        # take menu inputs

        if istextanim and animsize<60:
            animsize+=2
            ismenuloaded = False
            print(animsize)
            pygame.font.Font.set_point_size(game_font,animsize)
        # if not istextanim and 60 >= animsize > 50:
        elif 60 >= animsize > 50: #might be able to simplify?
            animsize-=1
            print(animsize)
            ismenuloaded = False
            pygame.font.Font.set_point_size(game_font,animsize)
        pygame.display.update()


        # make the text an object that takes inputs,
# while isinmenu:
        # game_font
        # 0 = play, 1 = settings, 2 = exit
        # selectedbutton = 0
        # ui shit
    clock.tick(60)
    # print("Hwrld")
