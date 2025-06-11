"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame.
Made by intern: @bassemfarid, no one or nothing else.
"""

import pygame
import random

pygame.mixer.init()
pygame.mixer.music.load("Project_3.mp3")
pygame.mixer.music.play(loops=-1)

# make sure that the audio doesn't instantly die during the phase change
music_flipswitch = 0

# self explanatory
score = 0

# 1 billion variables to ensure that the boss works correctly

DEFAULT_BOSS_HEALTH = 250

BOSS_HP_SCALING = 250

boss_health = DEFAULT_BOSS_HEALTH

boss_phase = 0

boss_triggered = 0

boss_beaten = 0

boss_momentum = 2

# prevents attack spam
flag = 1

is_attacking = False

BOSS_START = 100

# This is very important for the animations
frame_counter = 0

ATTACK_DURATION = 15

attack_length = 0

attack_delay = -1

# Making sure that commands don't run like 83 times (*ahem* leaderboard)
flip_switch = 0

# make sure egg doesn't spam after you Asplode the boss
flipswitch_2 = 0

# leaderboard 
lb = []

player_momentum = 0

landmine_momentum = 0

# Initialize Pygame and create a window
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Dinosaur Game!!!")
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills the pygame when False

# Game state variables
is_playing = True  # Whether the game is currently being played
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_GRAVITY_START_SPEED = -20  # The speed at which the player jumps
MIN_DIST = 150
players_gravity_speed = 0  # The current speed at which the player falls

# animation variables
speed = 5 # somewhat related to the FPS
egg_speed = 4 # how fast the egg be going
skyline_speed = 1 # how fast the skyline goes

# Load level assets
sky_surf = pygame.image.load("graphics/level/sky.png").convert()
skyline1_surf = pygame.image.load("graphics/level/skyline1.png").convert_alpha()
skyline2_surf = pygame.image.load("graphics/level/skyline2.png").convert_alpha()
ground_surf = pygame.image.load("graphics/level/ground.png").convert()
game_font = pygame.font.Font("font/Pixeltype.ttf", 50)
gameover_font = pygame.font.Font("font/Pixeltype.ttf", 100)
gameover_surf = pygame.image.load("graphics/level/gameover.png").convert()
score_surf = game_font.render(f"SCORE: {score}", False, "Black")
score_rect = score_surf.get_rect(center=(400, 50))
boss_hp_surf = score_surf = game_font.render(f"placeholder lmao", False, "Black")
boss_hp_rect = boss_hp_surf.get_rect(center=(400, 350))
instruction_surf = game_font.render("Press the Up Arrow while jumping to attack!", False, "Cyan")
instruction_rect = instruction_surf.get_rect(center=(400, 100))



# Load sprite assets
player_surf = pygame.image.load("graphics/player/player_walk0001.png").convert_alpha()
player_surf2 = pygame.image.load("graphics/player/player_walk0004.png").convert_alpha()
player_surf3 = pygame.image.load("graphics/player/player_walk0007.png").convert_alpha()
player_surf4 = pygame.image.load("graphics/player/player_walk0010.png").convert_alpha()
player_surf5 = pygame.image.load("graphics/player/player_jump.png").convert_alpha()
player_attack = pygame.image.load("graphics/player/jump_attack.png").convert_alpha()
player_sprint1 = pygame.image.load("graphics/player/player_sprinting0000.png").convert_alpha()
player_sprint2 = pygame.image.load("graphics/player/player_sprinting0003.png").convert_alpha()
player_sprint3 = pygame.image.load("graphics/player/player_sprinting0006.png").convert_alpha()
player_sprint4 = pygame.image.load("graphics/player/player_sprinting0009.png").convert_alpha()
player_sprint5 = pygame.image.load("graphics/player/jump_alt.png").convert_alpha()
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))
egg_surf = pygame.image.load("graphics/egg/egg_1.png").convert_alpha()
egg_surf2 = pygame.image.load("graphics/egg/egg_2.png").convert_alpha()
truck_kun_surf = pygame.image.load("graphics/egg/truck_kun.png").convert_alpha()
egg_list = []
enemy_surf = pygame.image.load("graphics/boss/enemy.png").convert_alpha()
enemy_alt_surf = pygame.image.load("graphics/boss/enemy_alt.png")
enemy_rect = enemy_surf.get_rect(bottomright=(750, GROUND_Y - 50))
lazer_surf = pygame.image.load("graphics/player/lazer.png").convert_alpha()
lazer_rect = lazer_surf.get_rect()

# load in mine tutle (this is very relevant trust me)
mineturtle_surf = pygame.image.load("graphics/boss/mine_turtle.png").convert_alpha()
mineturtle_rect = mineturtle_surf.get_rect(bottomleft=(-25, GROUND_Y))

# load bearing coconut lets go
coconut_surf = pygame.image.load("graphics/load_bearing_coconut.png").convert_alpha()
coconut_rect = coconut_surf.get_rect(center=(0, 0))

# load in the warning signs
warning = pygame.image.load("graphics/warning_sign.png").convert_alpha()
warnings = []

# load stuff for the bossfight!!!
attack1_surf = pygame.image.load("graphics/boss/attack1.png").convert_alpha()
attack_list = []

egg_timer = pygame.USEREVENT + 1
coconut_timer = pygame.USEREVENT + 1
pygame.time.set_timer(egg_timer, 1500)

which_sprite = 0
egg_sprite = 0
skyline1_x = 0
skyline2_x = -500

# function hell let's go

def sprite(num, isattacking):
    """Handles the animation.

    Args:
        num (int): Basically, which part of the run cycle we're in right now/which frame.
        isattacking (bool): Is the player attacking? Attack animation if  yes

    Returns:
        surface: Which frame should be displayed"""

    global boss_health
    if score <= BOSS_START:
        if num == 0:
            return player_surf5
        elif num % (4 * speed) <= speed:
            return player_surf
        elif num % (4 * speed) <= 2 * speed:
            return player_surf2
        elif num % (4 * speed) <= 3 * speed:
            return player_surf3
        elif num % (4 * speed) >= 3 * speed:
            return player_surf4
    else:
        if num == 0:
            if isattacking == True:
                lazer_rect.y = player_rect.y + 58
                lazer_rect.x = player_rect.x + 60
                screen.blit(lazer_surf, lazer_rect)
                return player_attack
            else:
                lazer_rect.y = 1000
                return player_sprint5
        elif num % (4 * speed) <= speed:
            return player_sprint1
        elif num % (4 * speed) <= 2 * speed:
            return player_sprint2
        elif num % (4 * speed) <= 3 * speed:
            return player_sprint3
        elif num % (4 * speed) >= 3 * speed:
            return player_sprint4

def enemy_hitreg(enemy_rect, attack_rect):
    """Handles the hit registration for the boss.

    Args:
        enemy_rect (rectangle): Hitbox of the enemy.
        attack_rect (rectangle): Hitbox of the attack.

    Returns:
        bool: Are you hitting the enemy right now?
    """
    if enemy_rect.colliderect(attack_rect):
        global boss_health
        boss_health -= 1
        return True
    else:
        return False

def egg(num):
    """Handles the animation for the egg.

    Args:
        num (int): Basically which frame we are on

    Returns:
        surface: The frame of animation to display.
    """
    if num % 30 <= 14:
        return egg_surf
    elif num % 30 >= 15:
        return egg_surf2

def egg_move(egglist):
    """Handles the movement for the eggs.

    Args:
        egglist (list): A list of all the eggs' hitboxes.

    Returns:
        list: The same list of the eggs' hitboxes.
    """
    if egglist:
        for rect in egglist:
            rect.x -= egg_speed
            if rect.bottom == GROUND_Y:
                screen.blit(egg(egg_sprite), rect)
            else:
                screen.blit(truck_kun_surf, rect)
        egglist = [egg for egg in egglist if egg.x > -100]
        return egglist
    else:
        return []

def attack(attack):
    """Handles the enemy's attacks on the screen.

    Args:
        attack (list): A list of all the enemy's lightning strike attacks currently onscreen.

    Returns:
        list: The same list.
    """
    if attack:
        for rect in attack:
            screen.blit(attack1_surf, rect)
        attack = [thing for thing in attack if thing.x > -100]
        return attack
    else:
        return []

def warn(attack):
    """Displays the warning signs on the screen.

    Args:
        attack (list): A list of all the warnings onscreen.

    Returns:
        list: list of the same stuff
    """
    if attack:
        for rect in attack:
            screen.blit(warning, rect)
        attack = [thing for thing in attack if thing.x > -100]
        return attack
    else:
        return []


def collisions(player, eggs):
    """Handles the hitreg between the player and the eggs.

    Args:
        player (rectangle): The hitbox of the player.
        eggs (rectangle): The hitbox of the egg.

    Returns:
        bool: False if they are colliding, True if not
    """
    if eggs:
        for eggrect in eggs:
            if player.colliderect(eggrect):
                return False
    return True


# unfinished leaderboard thing because i spent all my time on the advertisement instead
with open("leaderboard.txt", "r") as file:
    for line in file:
        lb.append(int(line.rstrip("\n")))

# gameplay loop!!!
while running:
    score_surf = game_font.render(f"SCORE: {score}", False, "Black")
    boss_hp_surf = game_font.render(f"BOSS HEALTH: {boss_health}", False, "Black")
    # Poll for events
    for event in pygame.event.get():
        # pygame.QUIT --> user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

        elif is_playing:
            # When player wants to jump by pressing SPACE
            if boss_triggered == 0:
                if score >= BOSS_START and boss_beaten == 0:
                    boss_phase = 1
                    boss_triggered = 1
            if boss_triggered == 1:
                if music_flipswitch == 0:
                    pygame.mixer.music.load("Project_2.mp3")
                    pygame.mixer.music.play(loops=-1)
                    music_flipswitch = 1
            if (
                    event.type == pygame.KEYDOWN
                    and event.key == pygame.K_SPACE
                    or event.type == pygame.MOUSEBUTTONDOWN
            ) and player_rect.bottom >= GROUND_Y:
                players_gravity_speed = JUMP_GRAVITY_START_SPEED
                which_sprite = 0
            if(
                    event.type == pygame.KEYDOWN and event.key == pygame.K_UP
            ):
                is_attacking = True

        else:
            # When player wants to play again by pressing SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player_rect.x = 25
                speed = 5
                skyline_speed = 1
                if flip_switch == 0:
                    lb.append(score)

                    # Ensure that everything in the leaderboard is an int
                    for i in range(len(lb)):
                        lb[i] = int(lb[i])

                    #Sort the values in order
                    lb.sort()

                    # Convert everything in the leaderboard to a string in peparation for joining all the values
                    for i in range(len(lb)):
                        lb[i] = str(lb[i])

                    with open("leaderboard.txt", "w") as file:
                        file.write("\n".join(lb))
                    flip_switch = 1
                flip_switch = 0
                is_playing = True
                score = 0


        if event.type == coconut_timer and is_playing and (boss_phase == 1 or boss_phase == 3):
            # i didn't feel like making another variable so i just used the x value of an otherwise unused asset
            coconut_rect.x = random.randint(0, 800)
            warnings.append(warning.get_rect(bottomleft=(coconut_rect.x - 15, 100)))
            attack_delay = 60
            attack_length = 0
            flag = 1

        # spawn eggs!!!
        if event.type == egg_timer and is_playing:
            if random.randint(0, 10) >= 7:
                n = 100
            else:
                n = GROUND_Y

            egg_list.append(egg_surf.get_rect(bottomleft=(random.randint(900, 1100), n)))


    if is_playing:
        screen.fill("purple")  # Wipe the screen

        # frame counter is very important for my totally efficient animation
        if frame_counter > 60:
            frame_counter = 0
            is_attacking = False
        else:
            frame_counter += 1

        if attack_delay != 0:
            attack_delay -= 1
        else:
            warnings.clear()
            if flag == 1:
                attack_list.append(attack1_surf.get_rect(bottomleft=(coconut_rect.x, GROUND_Y)))
                flag = 0
            if attack_length >= ATTACK_DURATION:
                attack_list.clear()
            else:
                attack_length += 1

        # increase score
        score += 1

        # keys!!!
        if score >= 0 and abs(player_momentum) <= 5:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_momentum -= 1
            if keys[pygame.K_RIGHT]:
                player_momentum += 1

            # if (
            #     event.type == pygame.KEYDOWN
            #     and event.key == pygame.K_LEFT
            # ):
            #     player_momentum -= 1
            # if (
            #     event.type == pygame.KEYDOWN
            #     and event.key == pygame.K_RIGHT
            # ):
            #     player_momentum += 1

        # move the player
        player_rect.x += player_momentum

        if player_rect.left <= 0:
            player_rect.left = 0
        if player_rect.right >= 800:
            player_rect.right = 800

        if player_rect.bottom == GROUND_Y:
            if player_momentum > 0:
                player_momentum -= 0.5
            elif player_momentum < 0:
                player_momentum += 0.5
        else:
            if player_momentum > 0:
                player_momentum -= 0.05
            elif player_momentum < 0:
                player_momentum += 0.05

        # if the boss' phase is 2 or above then summon mine turtle
        if boss_phase >= 2:
            if mineturtle_rect.x > player_rect.x:
                landmine_momentum -= 0.1
            elif mineturtle_rect.x < player_rect.x:
                landmine_momentum += 0.1
            if landmine_momentum > 5:
                landmine_momentum = 5
            elif landmine_momentum < -5:
                landmine_momentum = -5
            mineturtle_rect.x += landmine_momentum

        if boss_health <= 0:
            boss_phase += 1
            boss_health += BOSS_HP_SCALING * boss_phase

        if boss_phase >= 4:
            if flipswitch_2 == 0:
                egg_list.clear()
                flipswitch_2 = 1
            boss_triggered = 0
            boss_beaten = 1

        # Blit the level assets
        screen.blit(sky_surf, (0, 0))
        screen.blit(skyline1_surf, (skyline1_x, 0))

        # move the back layer of the skyline
        skyline1_x -= skyline_speed * 0.9
        if skyline1_x <= -800:
            screen.blit(skyline1_surf, (skyline1_x + 1600, 0))
        if skyline1_x <= -1600:
            skyline1_x = 0

        # front layer of the skyline
        screen.blit(skyline2_surf, (skyline2_x, 0))
        skyline2_x -= skyline_speed
        if skyline2_x <= -800:
            screen.blit(skyline2_surf, (skyline2_x + 1600, 0))
        if skyline2_x <= -1600:
            skyline2_x = 0

        # blit the rest of the stuff
        screen.blit(ground_surf, (0, GROUND_Y))
        screen.blit(score_surf, score_rect)
        if boss_triggered == 1:
            screen.blit(boss_hp_surf, boss_hp_rect)
            screen.blit(mineturtle_surf, mineturtle_rect)
            screen.blit(instruction_surf, instruction_rect)
            if enemy_hitreg(enemy_rect, lazer_rect):
                screen.blit(enemy_alt_surf, enemy_rect)
            else:
                screen.blit(enemy_surf, enemy_rect)


        if enemy_rect.y < 75:
            boss_momentum += 0.1
        elif enemy_rect.y > 75:
            boss_momentum -= 0.1
        enemy_rect.y += boss_momentum

        if boss_triggered == 0:
            egg_move(egg_list)
            egg_list = egg_move(egg_list)
        else:
            attack(attack_list)
            attack_list = attack(attack_list)
            warn(warnings)

        # difficulty ramping lets go
        # it only goes up to 5000 score and then you trigger the bossfight
        if score % 500 == 0 and score < 5000:
            speed -= speed ** 2 * 0.01
            egg_speed += ((egg_speed) / (egg_speed + 10))

        # Adjust player's vertical location then blit it
        players_gravity_speed += 1
        player_rect.y += players_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
            which_sprite += 1
        screen.blit(sprite(which_sprite, is_attacking), player_rect)

        # When player collides with enemy, game ends
        if boss_triggered == 0:
            is_playing = collisions(player_rect, egg_list)
        else:
            is_playing = collisions(player_rect, attack_list) and not player_rect.colliderect(mineturtle_rect)

        if which_sprite > 4 * speed:
            which_sprite = 1

        egg_sprite +=  1

    # When game is over, display game over message
    else:
        # clear lists
        warnings.clear()
        egg_list.clear()
        attack_list.clear()

        # reset boss phase stuff
        boss_health = DEFAULT_BOSS_HEALTH
        boss_phase = 0

        # reset everythng else
        pygame.mixer.music.load("project_3.mp3")
        pygame.mixer.music.play(loops=-1)
        screen.fill("black")
        egg_speed = 4
        flipswitch_2 = 0
        screen.blit(gameover_surf, (0, 0))
        mineturtle_rect.x = -25
        boss_triggered = 0
        boss_beaten = 0
        score_surf = gameover_font.render(f"SCORE: {score}", False, "Cyan")
        game_over = gameover_font.render("GAME OVER", False, "Cyan")
        screen.blit(score_surf, (360, 200))
        screen.blit(game_over, (360, 50))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()