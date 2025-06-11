import pygame
import random
'''
Todo
- selective reblitting to improve performance
- better structure (done)
- shadows/daynightcycle (hell no)
    - dynamic shadows based on the sun?
    - transparant shading mask?
'''

# Setup
pygame.init()
screen = pygame.display.set_mode((800,400))
clock = pygame.time.Clock()

# constants setup
# game
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_GRAVITY_START_SPEED = -20  # The speed at which the player jumps
WORLD_SCROLLSPEED = 5

# variables init
# menu
menu_select = 0
list_fontsize=[20,20,20]

if True: # delete this iftrue when im on my final pass, ignore for now as its used to collapse the block
    # Assetloader
    # misc assets
    splash_surf = pygame.image.load("assets/splash.png")
    splash_rect = splash_surf.get_rect(topleft=(0,0))
    transition_surf = pygame.image.load("assets/transition.png") #1600 2x screensize, go left, stop, go left after load
    transition_rect = transition_surf.get_rect(topleft=(0,0))
    # Load level assets
    parallex0 = pygame.image.load("assets/backdrop/parallex/back1.PNG")
    parallex1 = pygame.image.load("assets/backdrop/parallex/back1.PNG")
    parallex2 = pygame.image.load("assets/backdrop/parallex/back1.PNG")
    # list_parallex = [parallex0,parallex1,parallex2] # same function can handle scrolling it at different speeds
    # landscape
    ground_surf = pygame.image.load("assets/backdrop/ground1.png").convert_alpha()
    ground_rect = ground_surf.get_rect(topleft=(0,GROUND_Y))
    sky_surf = pygame.image.load("assets/backdrop/sky.PNG").convert_alpha()
    # player
    player_surf0 = pygame.image.load("assets/graphics/player/player_walk_1.png").convert_alpha()
    player_surf1 = pygame.image.load("assets/graphics/player/player_walk_2.png").convert_alpha()
    player_surf2 = pygame.image.load("assets/graphics/player/player_jump.png").convert_alpha()
    player_rect = player_surf0.get_rect(bottomleft=(25, GROUND_Y))
    list_player = [player_surf0,player_surf1,player_surf2]
    # condor
    condor_surf0 = pygame.image.load("assets/sprites/condor/cond1.PNG").convert_alpha()
    condor_surf1 = pygame.image.load("assets/sprites/condor/cond2.PNG").convert_alpha()
    condor_surf2 = pygame.image.load("assets/sprites/condor/cond3.PNG").convert_alpha()
    condor_rect = condor_surf0.get_rect(bottomleft=(800, GROUND_Y-100))
    list_condor = [condor_surf0,condor_surf1,condor_surf2]
    # cacti
    cacti_surf = pygame.image.load("assets/sprites/cacti.PNG").convert_alpha()
    cacti_rect = cacti_surf.get_rect(bottomleft=(800, GROUND_Y+100))
    # decorational assets (unused)
    joshuah_surf = pygame.image.load("assets/sprites/joshuah.PNG").convert_alpha()
    joshuah_rect = joshuah_surf.get_rect(bottomleft=(800, GROUND_Y+100))
    yukka_surf = pygame.image.load("assets/sprites/yukka.PNG").convert_alpha()
    yukka_rect = yukka_surf.get_rect(bottomleft=(800, GROUND_Y+100))
    yukka = (yukka_surf,yukka_rect)
    joshuah = (joshuah_surf,joshuah_rect)
    print("assets loaded")

# window display settings
pygame.display.set_icon(pygame.image.load("assets/graphics/egg/egg_1.png"))
pygame.display.set_caption("Placeholder")

# initial loop setup (changed from a whilerunning if loop to a system inspired by evan's modular stuff)
menustate = 1 #[exit,menu,game,transition]

# func defs
def score_update(): # Imports and updates the top 3 scores from saved file and returning it as a list
    with open('highscores.txt', 'r') as r:
        content = r.read()
    return eval(content)
def collisions(player,objects):
    # if obsticles:
    #     player.colliderect(obstacle_rect): return False
def resize(index:int):
    '''scales text up to size if active'''
    global menu_select
    global list_fontsize
    # size = list_fontsize[index]
    if menu_select == index:
        if list_fontsize[index] < 30: # scale up if active
            list_fontsize[index]+=1
    elif 20 < list_fontsize[index]: # scale down if inactive
        list_fontsize[index]-=1
    # print(index,list_fontsize[index]) # for troubleshooting
def animation_cycler(list: list,delmin:int,delmax:int):
    '''cycles through anim frames for a sprite, set delmin=delmax if want consistant timing'''
def menuactive():
    global menu_select
    # reloads variables
    # invalid catcher
    screen.fill("#B00BA5")
    # variable initialization
    menu_select = 0

    # font loader
    title_font = pygame.font.Font(pygame.font.get_default_font(),50)
    # Title
    surf_title = title_font.render("Placeholder", True, "White")
    rect_title = surf_title.get_rect(topleft=(50,75)) # topleft=(50,75)
    # Menu rect init
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            # pygame.QUIT --> user clicked X to close your window
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
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
                        return 2
                    elif menu_select == 1: # Settings
                        return 0
                    else: #exit
                        return 0
                # # for troubleshooting
                # print("event key",event.key)
                # print("menu index",menu_select)
        resize(0)
        resize(1)
        resize(2)
        # menu renderer
        clock.tick(100)
        screen.fill("#B00BA5") #// holy shit calamity reference
        menu_font1 = pygame.font.Font(pygame.font.get_default_font(),list_fontsize[0])
        menu_font2 = pygame.font.Font(pygame.font.get_default_font(),list_fontsize[1])
        menu_font3 = pygame.font.Font(pygame.font.get_default_font(),list_fontsize[2])
        surf_1 = menu_font1.render("Play", True, "White")
        surf_2 = menu_font2.render("Settings", True, "White")
        surf_3 = menu_font3.render("Exit", True, "White")
        rect_1 = surf_1.get_rect(midleft=(50,211)) # topleft=(50,200)
        rect_2 = surf_2.get_rect(midleft=(50,261)) # topleft=(50,250)
        rect_3 = surf_3.get_rect(midleft=(50,311)) # topleft=(50,300)
        # screen.blit(surf_1,rect_1)
        screen.blits(((splash_surf,splash_rect),(surf_title,rect_title),(surf_1,rect_1),(surf_2,rect_2),(surf_3,rect_3)))
        # print(screen.blits(((surf_title,rect_title),(surf_1,rect_1),(surf_2,rect_2),(surf_3,rect_3)),doreturn=True)) #// selective reblitting? have all updated objects be placed in a tuple list?
        pygame.display.flip()
def gameactive():
    global menustate
    global GROUND_Y
    # Game state variables reinit
    players_gravity_speed = 0  # The current speed at which the player falls
    isalive = True
    cacti_rect.left = 800
    start_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menustate=0
            if event.type == pygame.KEYDOWN:
                if isalive:
                    if event.key == pygame.K_SPACE: # make it a chargeup?
                        players_gravity_speed = -20
                if event.key == pygame.K_ESCAPE:
                    return 1
        # calculations
        # cacti
        cacti_rect.x -= 5
        if cacti_rect.right <= 0:
            cacti_rect.left = 800+random.randint(0,100)
            cacti_rect.x -= 5
        if yukka_rect.right <= 0:
            yukka_rect.left = 800+random.randint(0,100)
            yukka_rect.x -= 5
        if joshuah_rect.right <= 0:
            joshuah_rect.left = 800+random.randint(0,100)
            joshuah_rect.x -= 5
    # player
        players_gravity_speed += 1
        player_rect.y += players_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
        # add a func for checking colision
        # if egg_rect.colliderect(player_rect):
        #         is_playing = False

        clock.tick(100)
        # renderer
        # def renderscroller(sprite_surf,offset=None):
        #     if offset != none spriterect.x+981347
        #     screen.blit(sprite_surf,)
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 0))
        screen.blit(cacti_surf, cacti_rect)
        screen.blit(yukka_surf,yukka_rect)
        screen.blit(joshuah_surf,joshuah_rect)
        screen.blit(list_player[0], player_rect)
        pygame.display.flip()
# def transitionactive():

def main():
    global menustate
    while menustate != 0:
        if menustate == 1:
            menustate = menuactive()
        elif menustate == 2:
            menustate = gameactive()
    pygame.quit()
main()
# imms o fucking tired