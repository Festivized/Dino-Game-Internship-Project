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

# variables setup
# game
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_GRAVITY_START_SPEED = -20  # The speed at which the player jumps
WORLD_SCROLLSPEED = 5
TICKSPEED = 100
queue = None # enemyqueue randomizer

# menu
menu_select = 0
list_fontsize=[20,20,20]
score_font = pygame.font.Font(pygame.font.get_default_font(),20)
title_font = pygame.font.Font(pygame.font.get_default_font(),50)
if True: # delete this iftrue when im on my final pass, ignore for now as its used to collapse the block
    # Assetloader
    # music assets
    # misc assets
    splash_surf = pygame.image.load("assets/splash.png")
    splash_rect = splash_surf.get_rect(topleft=(0,0))
    transition_surf = pygame.image.load("assets/transition.png") #1600 2x screensize, go left, stop, go left after load
    transition_rect = transition_surf.get_rect(topleft=(0,0))
    # Load level assets
    parallex0 = pygame.image.load("assets/backdrop/parallex/back1.PNG")
    parallex1 = pygame.image.load("assets/backdrop/parallex/back2.PNG")
    parallex2 = pygame.image.load("assets/backdrop/parallex/back3.PNG")
    parallex0_x = parallex1_x = parallex2_x = 0
    # landscape
    ground_surf = pygame.image.load("assets/backdrop/ground1.png").convert_alpha()
    ground_x = 0
    sky_surf = pygame.image.load("assets/backdrop/sky.PNG").convert_alpha()
    cloud1_surf = pygame.image.load("assets/sprites/cloud/cloud1.PNG").convert_alpha()
    cloud1_rect = cloud1_surf.get_rect(topleft=(0,0))
    cloud2_surf = pygame.image.load("assets/sprites/cloud/cloud2.PNG").convert_alpha()
    cloud2_rect = cloud2_surf.get_rect(topleft=(0,0))
    cloud3_surf = pygame.image.load("assets/sprites/cloud/cloud3.PNG").convert_alpha()
    cloud3_rect = cloud3_surf.get_rect(topleft=(0,0))

    # player
    player_surf0 = pygame.image.load("assets/graphics/player/player_walk_1.png").convert_alpha()
    player_surf1 = pygame.image.load("assets/graphics/player/player_walk_2.png").convert_alpha()
    player_surf2 = pygame.image.load("assets/graphics/player/player_jump.png").convert_alpha()
    player_rect = player_surf0.get_rect(bottomleft=(25, GROUND_Y))
    list_player = [player_surf0,player_surf1]
    # condor
    condor_surf0 = pygame.image.load("assets/sprites/condor/cond1.png").convert_alpha()
    condor_surf1 = pygame.image.load("assets/sprites/condor/cond2.png").convert_alpha()
    condor_surf2 = pygame.image.load("assets/sprites/condor/cond3.png").convert_alpha()
    condor_rect = condor_surf0.get_rect(bottomleft=(800, GROUND_Y-100))
    list_condor = [condor_surf0,condor_surf1,condor_surf2]
    # cacti
    cacti_surf = pygame.image.load("assets/sprites/cacti.png").convert_alpha()
    cacti_rect = cacti_surf.get_rect(bottomleft=(800, GROUND_Y))
    # collidable sprites
    list_collidable = [cacti_rect,condor_rect]
    # decorational assets (unused)
    joshuah_surf = pygame.image.load("assets/sprites/joshuah.PNG").convert_alpha()
    joshuah_rect = joshuah_surf.get_rect(bottomleft=(800, GROUND_Y+150))
    yukka_surf = pygame.image.load("assets/sprites/yukka.PNG").convert_alpha()
    yukka_rect = yukka_surf.get_rect(bottomleft=(800, GROUND_Y+150))
    yukka = (yukka_surf,yukka_rect)
    joshuah = (joshuah_surf,joshuah_rect)
    print("assets loaded")

# window display settings
pygame.display.set_icon(pygame.image.load("assets/graphics/egg/egg_1.png"))
pygame.display.set_caption("Hey chat have we heard of skibity toilet")

# initial loop setup (changed from a whilerunning if loop to a system inspired by evan's modular stuff)
menustate = 1 #[exit,menu,game,transition]

# func defs
def placeholder():
    print("wip")
# WIP
def score_reader(): # Imports and updates the top 3 scores from saved file and returning as a list credits:Dylan L
    with open('assets/score.txt', 'r') as file:
        content = file.read()
    return eval(content)
score_ram = score_reader()
def score_eval(newscore:int):
    global score_ram
    score_ram.append(newscore)
    score_ram.sort(reverse=True)
    score_ram=score_ram[0:3]
    placeholder()
def score_writer(scorelist=None):
    if scorelist == None: # apparantly list souldent be used as a default value as it can be modified // not really relevant here but i wanted the warning to go away
        scorelist = [0,0,0]
    with open('assets/score.txt', 'w') as file:
        content = file.write(str(scorelist))
def score_formatter():
    formatted = f"1. {score_ram[0]}\n2. {score_ram[1]}\n3. {score_ram[2]}"
    return formatted
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
    placeholder()
def collisioncheck():
    '''checks player_rect against collidables list, if hit return bool:True'''
    global list_collidable
    for rect in list_collidable:
        if player_rect.colliderect(rect):
            return True
    return False
def parallex_scroller(sprite, x: int, scrollspeed=5):
    x -= scrollspeed
    if x <= -sprite.get_width():
        x = 0
    return x
def parallex_renderer(sprite, x: int, y=0):
    screen.blit(sprite, (x, y))
    screen.blit(sprite, (x + sprite.get_width(), y))
def spritescroller(rect,min:int,max:int,stepspeed: int=5,isqueue: bool=False):
    global queue
    rect.x -= stepspeed
    if rect.right <= 0:
        if isqueue:
            queue = random.randint(0,1)
        rect.left = 800+random.randint(min,max)
        rect.x -= stepspeed
def animation_cycler(anim_set:list, delay:int = 200): #200 should cause it to cycle
    '''cycles through anim frames for a sprite, set delmin=delmax if want consistant timing'''
    time = pygame.time.get_ticks()
    return time//delay%len(anim_set)
def paused():
    global title_font
    while True:
        surf_title = score_font.render("You are paused\npress \"esc\" to unpause", False, "White")
        screen.blit(surf_title, surf_title.get_rect(center=(400,200)))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 1

#body
# def transition(nextup:int):

def menuactive():
    global menu_select, score_font, title_font
    # variable initialization
    menu_select = 0
    # Title
    surf_title = title_font.render("Placeholder 2", True, "White")
    rect_title = surf_title.get_rect(topleft=(50,75)) # topleft=(50,75)
    surf_score_mn = score_font.render(f"Topscores:\n{score_formatter()}", True, "White")
    rect_score_mn = surf_score_mn.get_rect(topright=(750,75)) # topleft=(50,75)
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
                if event.key == pygame.K_s and menu_select < 2: #cycle down
                    menu_select += 1
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
        clock.tick(TICKSPEED)
        screen.fill("#B00BA5") #// holy shit calamity reference
        menu_font1 = pygame.font.Font(pygame.font.get_default_font(),list_fontsize[0])
        menu_font2 = pygame.font.Font(pygame.font.get_default_font(),list_fontsize[1])
        menu_font3 = pygame.font.Font(pygame.font.get_default_font(),list_fontsize[2])
        surf_1 = menu_font1.render("Play", True, "White")
        surf_2 = menu_font2.render("Help", True, "White")
        surf_3 = menu_font3.render("Exit", True, "White")
        rect_1 = surf_1.get_rect(midleft=(50,211)) # topleft=(50,200)
        rect_2 = surf_2.get_rect(midleft=(50,261)) # topleft=(50,250)
        rect_3 = surf_3.get_rect(midleft=(50,311)) # topleft=(50,300)
        # screen.blit(surf_1,rect_1)
        screen.blits(((splash_surf,splash_rect),(surf_title,rect_title),(surf_1,rect_1),(surf_2,rect_2),(surf_3,rect_3),(surf_score_mn,rect_score_mn)))
        # print(screen.blits(((surf_title,rect_title),(surf_1,rect_1),(surf_2,rect_2),(surf_3,rect_3)),doreturn=True)) #// selective reblitting? have all updated objects be placed in a tuple list?
        pygame.display.flip()
def gameactive():
    global menustate, GROUND_Y, TICKSPEED, score_font, parallex0_x, parallex1_x, parallex2_x, ground_x, condor_surf, queue
    parallex0_x = parallex1_x = parallex2_x = ground_x = 0
    player_index = condor_index = 0
    finalscore = 0
    players_gravity_speed = 0
    queue = random.randint(0,1)
    # conditionals init
    loadbuffer = True
    isalive = True
    isjumped = False
    isdeadjumped = False
    cacti_rect.left = condor_rect.left = 800
    yukka_rect.left = 400
    joshuah_rect.left = 650
    start_time = pygame.time.get_ticks()
    tickspeed = TICKSPEED
    while True:
        score = int((pygame.time.get_ticks()-start_time)/100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menustate=0
            if event.type == pygame.KEYDOWN:
                if isalive and event.key == pygame.K_SPACE and not isjumped: # make it a chargeup?
                    players_gravity_speed = -20
                    isjumped = True
                if event.key == pygame.K_ESCAPE:
                    if paused() == 0:
                        return 0
                if not isalive and (event.key == pygame.K_r or event.key == pygame.K_SPACE):
                    return 2

        if isalive:
            player_index = animation_cycler(list_player,200)
            parallex2_x = parallex_scroller(parallex2,parallex2_x,1)
            parallex1_x = parallex_scroller(parallex1,parallex1_x,2)
            parallex0_x = parallex_scroller(parallex0,parallex0_x,4)
            ground_x = parallex_scroller(ground_surf,ground_x,5)
            if queue == 0:
                spritescroller(cacti_rect,0,400,5,True)
            else:
                condor_index = animation_cycler(list_condor,100)
                spritescroller(condor_rect,100,300,5,True)
            spritescroller(yukka_rect,0,800,5)
            spritescroller(joshuah_rect,400,1200,5)
            spritescroller(cloud1_rect,0,200,1)
            spritescroller(cloud2_rect,0,200,2)
            spritescroller(cloud3_rect,0,200,3)

            print(queue)
            # player
            players_gravity_speed += 1
            player_rect.y += players_gravity_speed
            if player_rect.bottom > GROUND_Y:
                player_rect.bottom = GROUND_Y
                isjumped = False

            if collisioncheck():
                isalive = False
                finalscore = score
                score_eval(finalscore)
            tickspeed+=1

        else:
            if not isdeadjumped:
                players_gravity_speed = -20
                isdeadjumped = True
            player_surf = player_surf2
            tickspeed=50
            players_gravity_speed += 1
            player_rect.y += players_gravity_speed

        #renderere
        clock.tick(tickspeed)
        screen.blit(sky_surf, (0, 0))
        parallex_renderer(parallex2,parallex2_x,0)
        parallex_renderer(parallex1,parallex1_x,0)
        parallex_renderer(parallex0,parallex0_x,0)
        parallex_renderer(ground_surf,ground_x,0)
        if isalive:
            score_text = f"Score:{score}"
        else:
            score_text = f"Score:{finalscore}"
        screen.blit(list_player[player_index], player_rect)
        score_surf = score_font.render(score_text, True, "white")
        screen.blit(score_surf, score_surf.get_rect(center=(400, 80)))
        screen.blit(cacti_surf, cacti_rect)
        screen.blit(list_condor[condor_index], condor_rect)
        screen.blit(yukka_surf, yukka_rect)
        screen.blit(joshuah_surf, joshuah_rect)
        screen.blits(((cloud1_surf,cloud1_rect),(cloud2_surf,cloud2_rect),(cloud3_surf,cloud3_rect)))
        pygame.display.flip()

        # could cause problems, trying to give plr a second to respond before gamestart
        if loadbuffer:
            if paused() == 0:
                return 0
            loadbuffer = False


# main
def main():
    global menustate
    queuedstate = None
    while menustate != 0:
        if menustate == 1:
            menustate = menuactive()
        elif menustate == 2:
            menustate = gameactive()
            score_writer(score_ram)
    score_writer(score_ram)
    pygame.quit()
main()
# imms o fucking tired