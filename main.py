import pygame
import random

'''
Todo (im not touching this library ever again, would rather experience the aceleration of gravity from the bridge above the oakville downtown library)
- selective reblitting to improve performance
- better structure (done)
- shadows/daynightcycle (hell no)
    - dynamic shadows based on the sun?
    - transparant shading mask?
- hp
- sfx
- transitions
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
speedmodint = 1

# menu
menu_select = 0
list_fontsize=[20,20,20]
score_font = pygame.font.Font(pygame.font.get_default_font(),20)
title_font = pygame.font.Font(pygame.font.get_default_font(),50)

# Assetloader
# music assets
# misc assets
splash_surf = pygame.image.load("assets/splash.png")
splash_rect = splash_surf.get_rect(topleft=(0,0))
transition_surf = pygame.image.load("assets/transition.png") #1600 2x screensize, go left, stop, go left after load
transition_rect = transition_surf.get_rect(topleft=(0,0))
help_surf = pygame.image.load("assets/image.png").convert_alpha()
help_rect = help_surf.get_rect(center=(400, 200))
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
splashtext=[
            'lorem ipsum', 'dolor sit', 'amet consectetur', 'adipiscing elit', 'sed do', 'eiusmod tempor',
            'incididunt ut', 'labore et', 'dolore magna', 'aliqua ut', 'enim ad', 'minim veniam',
            'quis nostrud', 'exercitation ullamco', 'laboris nisi', 'ut aliquip', 'ex ea', 'commodo consequat',
            'duis aute', 'irure dolor', 'in reprehenderit', 'in voluptate', 'velit esse', 'cillum dolore',
            'eu fugiat', 'nulla pariatur', 'excepteur sint', 'occaecat cupidatat', 'non proident', 'sunt in',
            'culpa qui', 'officia deserunt', 'mollit anim', 'id est'
            ]
pygame.display.set_caption(splashtext[random.randint(0,len(splashtext))])

# initial loop setup (changed from a whilerunning if loop to a system inspired by evan's modular stuff)
menustate = 1 #[exit,menu,game,transition]

# func defs
def placeholder():
    """Placeholder function for unfinished defs and loops so I can test code without commenting out unfinished funcs and loops."""
    print("wip")
# Finished
def score_reader(): # Imports and updates the top 3 scores from saved file and returning as a list credits:Dylan L
    """Reads and returns top scores from 'assets/score.txt'.

    Returns:
        list: A list of top 3 scores as integers.
    """
    with open('assets/score.txt', 'r') as file:
        content = file.read()
    return eval(content)
score_ram = score_reader()
def score_eval(newscore:int):
    """Adds a new score to global score_ram and keeps top 3 scores.

    Args:
        newscore (int): The score to evaluate.
    """
    global score_ram
    score_ram.append(newscore)
    score_ram.sort(reverse=True)
    score_ram=score_ram[0:3]
def score_writer(scorelist=None):
    """Writes a list of scores to the score file.

    Args:
        scorelist (list, optional): List of top scores. Defaults to [0, 0, 0] incase stuff goes sideways.
    """
    if scorelist == None: # apparantly list souldent be used as a default value as it can be modified // not really relevant here but i wanted the warning to go away
        scorelist = [0,0,0]
    with open('assets/score.txt', 'w') as file:
        content = file.write(str(scorelist))
def score_formatter():
    """Formats the top scores into a numbered string for the menu.

    Returns:
        str: A formatted multi-line string with the top 3 scores.
    """
    formatted = f"1. {score_ram[0]}\n2. {score_ram[1]}\n3. {score_ram[2]}"
    return formatted
def resize(index:int):
    """Animates menu font scaling for selection feedback.

    Args:
        index (int): The index of the menu option.
    """
    global menu_select
    global list_fontsize
    # size = list_fontsize[index]
    if menu_select == index:
        if list_fontsize[index] < 30: # scale up if active
            list_fontsize[index]+=1
    elif 20 < list_fontsize[index]: # scale down if inactive
        list_fontsize[index]-=1
    # print(index,list_fontsize[index]) # for troubleshooting
def collisioncheck():
    """Checks for collision between the player and any rects in list_collidable.

    Returns:
        bool: True if a collision is detected, otherwise False.
    """
    global list_collidable
    for rect in list_collidable:
        if player_rect.colliderect(rect):
            return True
    return False
def parallex_scroller(sprite, x: int, stepspeed=5):
    """Scrolls a background sprite in a parallax effect with customizable stepspeeds.

    Args:
        sprite (Surface): The background image.
        x (int): Current x-position.
        stepspeed (int, optional): Speed modifier. Defaults to 5.

    Returns:
        int: New x-position after scrolling.
    """
    x -= speedmod(stepspeed)
    if x <= -sprite.get_width():
        x = 0
    return x
def parallex_renderer(sprite, x: int, y=0):
    """Renders the result of parallex_scroller() to avoid it incrementing when dead.

    Args:
        sprite (Surface): The image to render.
        x (int): X-position of the first copy.
        y (int, optional): Y-position. Defaults to 0.
    """
    screen.blit(sprite, (x, y))
    screen.blit(sprite, (x + sprite.get_width(), y))
def spritescroller(rect,min:int,max:int,stepspeed: int=5,isqueue: bool=False):
    """Scrolls a sprite horizontally and allows randomization of obstacles.

    Args:
        rect (Rect): The rect of the sprite.
        min (int): Minimum offset for repositioning.
        max (int): Maximum offset.
        stepspeed (int, optional): Scroll speed. Defaults to 5.
        isqueue (bool, optional): Whether to randomize enemy type. Defaults to False.
    """
    global queue
    rect.x -= speedmod(stepspeed)
    if rect.right <= 0:
        if isqueue:
            queue = random.randint(0,1)
        rect.left = 800+random.randint(min,max)
        rect.x -= speedmod(stepspeed)
def animation_cycler(anim_set:list, delay:int = 200): #200 should cause it to cycle
    """Cycles through animation frames based on game time.

        Args:
            anim_set (list): List of surfaces representing animation frames.
            delay (int, optional): Delay in ms between frames. Defaults to 200.

        Returns:
            int: Index of the current frame.
        """
    time = pygame.time.get_ticks()
    return time//delay%len(anim_set)
def inhelp():
    """Displays the help screen with an infographic.

    Returns:
        str or int: Returns '' on ESC, -1 on window close.
    """
    screen.fill("tan")
    while True:
        screen.blit(help_surf, help_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return ''
def paused():
    """Pauses the game and displays a pause message.

    Returns:
        int: Time spent paused in milliseconds, or -1 if user quits.
    """
    screen.fill("tan")
    global title_font
    time_start = pygame.time.get_ticks()
    while True:
        surf_title = score_font.render("You are paused\npress \"esc\" to unpause", False, "White")
        screen.blit(surf_title, surf_title.get_rect(center=(400,200)))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                time_end=pygame.time.get_ticks()
                return time_end-time_start
def speedmod(startingspeed:int)-> int:
    """Applies the global speed modifier to a base speed.

    Args:
        startingspeed (int): The initial speed value.

    Returns:
        int: Modified speed.
    """
    global speedmodint
    return startingspeed*speedmodint

#body
def menuactive():
    """Handles the main menu logic, including navigation and selection.

    Returns:
        int: Game state ID indicating next state (e.g. 0 = exit, 1 = menu, 2 = play).
    """
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
                return 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and menu_select > 0: #cycle up
                    menu_select -= 1
                if event.key == pygame.K_s and menu_select < 2: #cycle down
                    menu_select += 1
                if event.key == pygame.K_RETURN:
                    if menu_select == 0: # Play
                        return 2
                    elif menu_select == 1: # Settings
                        if inhelp() == 0:
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
        screen.blits(((splash_surf,splash_rect),(surf_title,rect_title),(surf_1,rect_1),(surf_2,rect_2),(surf_3,rect_3),(surf_score_mn,rect_score_mn)))
        pygame.display.flip()
    raise RuntimeError(f"how the hell did you get here")
def gameactive():
    """Runs the main game loop including rendering, logic, and controls.

    Returns:
        int: Game state ID to switch to (e.g. 0 = exit, 1 = menu, 2 = restart).
    """
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
    paused_time_total = 0
    start_time = pygame.time.get_ticks() # relative start time
    tickspeed = TICKSPEED
    speedmodint = 1
    while True:
        current_time = pygame.time.get_ticks()
        score = int(((current_time-start_time-paused_time_total)/100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menustate=0
            if event.type == pygame.KEYDOWN:
                if isalive and event.key == pygame.K_SPACE and not isjumped: # make it a chargeup?
                    players_gravity_speed = -20
                    isjumped = True
                if event.key == pygame.K_TAB:
                    return 1
                if event.key == pygame.K_ESCAPE:
                    paused_time = paused()
                    if paused_time == -1:
                        return 0
                    paused_time_total+=paused_time
                if not isalive and (event.key == pygame.K_r or event.key == pygame.K_SPACE):
                    return 2

        if isalive:
            speedmodint*= 1.0001
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
            tickspeed+=2

        else:
            if not isdeadjumped:
                players_gravity_speed = -20
                isdeadjumped = True
            player_surf = player_surf2
            tickspeed=50
            players_gravity_speed += 1
            player_rect.y += players_gravity_speed

        #renderer
        clock.tick(tickspeed)
        screen.blit(sky_surf, (0, 0))
        parallex_renderer(parallex2,parallex2_x,0)
        parallex_renderer(parallex1,parallex1_x,0)
        parallex_renderer(parallex0,parallex0_x,0)
        parallex_renderer(ground_surf,ground_x,0)
        screen.blits(((cloud1_surf,cloud1_rect),(cloud2_surf,cloud2_rect),(cloud3_surf,cloud3_rect)))
        if isalive:
            score_text = f"Score:{score}"
            screen.blit(list_player[player_index], player_rect)
        else:
            score_text = f"Score:{finalscore}"
            screen.blit(player_surf2, player_rect)
        score_surf = score_font.render(score_text, True, "white")
        screen.blit(score_surf, score_surf.get_rect(center=(400, 80)))
        screen.blit(cacti_surf, cacti_rect)
        screen.blit(list_condor[condor_index], condor_rect)
        screen.blit(yukka_surf, yukka_rect)
        screen.blit(joshuah_surf, joshuah_rect)
        pygame.display.flip()
    raise RuntimeError(f"how the hell did you get here")

# main
def main():
    """Main game loop managing state transitions and lifecycle."""
    global menustate
    queuedstate = None
    while menustate != 0:
        if menustate == 1:
            menustate = menuactive()
            # move transition mask in
        elif menustate == 2:
            menustate = gameactive()
            score_writer(score_ram)
    score_writer(score_ram)
    pygame.quit()

# I think I messed up my sleep for this ._. (not worth it)
main()