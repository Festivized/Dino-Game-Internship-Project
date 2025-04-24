import pygame

# Setup
pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()
# Conditionals
isrunning = True
ismenuloaded = False
isinmenu = False
istextanim = False
# text variables
game_font = pygame.font.Font(pygame.font.get_default_font(),50)
animsize=50
while isrunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isrunning = False
        elif isinmenu: #if menu is loaded
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                ismenuloaded = False #reloads menu
                istextanim = not istextanim
                print(istextanim)
                print("space registered")
    if not ismenuloaded:
        screen.fill("Purple")
        title_surf = game_font.render("Placeholder", True, "White")
        title_rect = title_surf.get_rect(center=(200,150))
        screen.blit(title_surf,title_rect)
        pygame.display.update()
        print("menu (re)loaded")
        ismenuloaded = True
        isinmenu = True
    if istextanim:
        if animsize<60:
            animsize+=2
            ismenuloaded = False
            print(animsize)
            pygame.font.Font.set_point_size(game_font,animsize)
    else:
        if animsize<=60 and animsize>50:
            animsize-=1
            print(animsize)
            ismenuloaded = False
        pygame.font.Font.set_point_size(game_font,animsize)
    clock.tick(60)

    FUCKING FINALLY