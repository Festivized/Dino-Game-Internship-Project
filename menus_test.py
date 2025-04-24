import pygame

# Setup
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
# Conditionals
isrunning = True
ismenuloaded = False
isinmenu = False
istextanim = False
# window display settings
pygame.display.set_icon(pygame.image.load("assets/graphics/egg/egg_1.png"))
pygame.display.set_caption("Placeholder")
screen.fill("#131314") # render dark grey
#load music
pygame.mixer.init()
pygame.mixer.music.load("assets/music/1.mp3")
# Constants
animsize = 50
# base_font = pygame.font.Font(pygame.font.get_default_font(),50)
title_font = pygame.font.Font(pygame.font.get_default_font(),100)
game_font = pygame.font.Font(pygame.font.get_default_font(),50)
# title_font = pygame.font.Font.set_point_size(base_font,100)
# game_font = pygame.font.Font.set_point_size(base_font,50)
# Asset load

while isrunning:
    for event in pygame.event.get():
        # pygame.QUIT --> user clicked X to close your window
        if event.type == pygame.QUIT:
            isrunning = False
        elif isinmenu: #if menu is loaded
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                ismenuloaded = False #reloads menu
                istextanim = not istextanim
                print(istextanim)
                print("space registered")
    while not ismenuloaded:
        screen.fill("#ff00ff")
        # load menu assets
        title_surf = title_font.render("Placeholder", True, "White")
        title_rect = title_surf.get_rect(topleft=(100,75))
        screen.blit(title_surf,title_rect)

        play_surf = game_font.render("Play", True, "White")
        play_rect = play_surf.get_rect(topleft=(100,550))
        screen.blit(play_surf,play_rect)

        settings_surf = game_font.render("Settings", True, "White")
        settings_rect = settings_surf.get_rect(topleft=(100,625))
        screen.blit(settings_surf,settings_rect)

        exit_surf = game_font.render("Exit", True, "White")
        exit_rect = exit_surf.get_rect(topleft=(100,700))
        screen.blit(exit_surf,exit_rect)
        ismenuloaded = True
        isinmenu =True
        print("menu loaded")
        pygame.display.update()
    pygame.display.update()
    if isinmenu:
        # take menu inputs
        if istextanim and animsize<60:
            animsize+=2
            ismenuloaded = False
            print(animsize)
            pygame.font.Font.set_point_size(game_font,animsize)
        if not istextanim and animsize<=60 and animsize>50:
            animsize-=1
            print(animsize)
            ismenuloaded = False
            pygame.font.Font.set_point_size(game_font,animsize)
    pygame.display.update()
# while isinmenu:
        # game_font
        # 0 = play, 1 = settings, 2 = exit
        # selectedbutton = 0
        # ui shit
    clock.tick(20)
    # print("Hwrld")
