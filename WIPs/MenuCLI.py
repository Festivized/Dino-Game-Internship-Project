import pygame

# Setup
pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()
# Conditionals
isrunning = True
ismenuloaded = False
isinmenu = False
ismenu_updated = False
# text variables
# game_font = pygame.font.Font(pygame.font.get_default_font(),50)
# animsize=50
menu_txt=["o 1\n- 2\n- 3","- 1\no 2\n- 3","- 1\n- 2\no 3"]
menu_select = 0
while isrunning:
    if not ismenuloaded:
        print(menu_txt[0])
        ismenuloaded = True
        isinmenu = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isrunning = False
        elif isinmenu: #if menu is loaded
            if event.type == pygame.KEYUP and event.key == pygame.K_w and menu_select > 0: #cycle up
                menu_select -= 1
                ismenu_updated = True
            if event.type == pygame.KEYUP and event.key == pygame.K_s and menu_select < 2: #cycle down
                menu_select += 1
                ismenu_updated = True
    if not ismenuloaded:
        print(menu_txt[0])
        ismenuloaded = True
        isinmenu = True
    if ismenuloaded and ismenu_updated:
        print(menu_txt[menu_select])
        ismenu_updated = False
    clock.tick(60)

    # FUCKING FINALLY