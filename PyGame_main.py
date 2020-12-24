import pygame



if __name__ == '__main__':
    size = width, heigt
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
