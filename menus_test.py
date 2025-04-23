import pygame

# Setup
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
# Conditionals
isrunning = True
ismenuloaded = False
isinmenu = False
# window display settings
pygame.display.set_icon(pygame.image.load("assets/graphics/egg/egg_1.png"))
pygame.display.set_caption("Placeholder")
screen.fill("#131314")
pygame.mixer.init()
pygame.mixer.music.load("assets/music/1.mp3")
# Constants
# Asset load
while isrunning:
    for event in pygame.event.get():
        print(pygame.event.get())
        # pygame.QUIT --> user clicked X to close your window
        if event.type == pygame.QUIT:
            isrunning = False

    while not ismenuloaded:
        screen.fill("#ff00ff")
        # load menu assets
        pygame.display.update()
        ismenuloaded = True
        isinmenu =True
    # while isinmenu:
        # ui shit
    clock.tick(60)
    print("Hwrld")