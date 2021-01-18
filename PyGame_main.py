import pygame
from pygame import *


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        platform_w = 30
        platform_h = 30
        platform_color = "RED"
        sprite.Sprite.__init__(self)
        self.image = Surface((platform_w, platform_h))
        self.image.fill(Color(platform_color))
        self.rect = Rect(x, y, platform_w, platform_h)


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.move_speed = 5
        self.y_change = 0
        self.width = 20
        self.height = 30
        color_player = "BLUE"
        self.x_change = 0
        self.startX = x
        self.startY = y
        self.image = Surface((self.width,  self.height))
        self.image.fill(Color(color_player))
        self.rect = Rect(x, y, self.width,  self.height)

    def update(self, left, right, up, down, platforms):
        if up:
            self.y_change = -self.move_speed
        if down:
            self.y_change = self.move_speed
        if left:
            self.x_change = -self.move_speed
        if right:
            self.x_change = self.move_speed

        if not (left or right):
            self.x_change = 0
        if not (up or down):
            self.y_change = 0

        self.rect.y += self.y_change
        self.collide(0, self.y_change, platforms)

        self.rect.x += self.x_change
        self.collide(self.x_change, 0, platforms)

    def collide(self, x_change, y_change, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):

                if x_change > 0:
                    self.rect.right = p.rect.left

                if x_change < 0:
                    self.rect.left = p.rect.right

                if y_change > 0:
                    self.rect.bottom = p.rect.top
                    self.y_change = 0

                if y_change < 0:
                    self.rect.top = p.rect.bottom
                    self.y_change = 0


def main():
    pygame.init()
    block_h = 30
    block_w = 30
    size = 750, 600
    screen = pygame.display.set_mode(size)
    bg = Surface((800, 640))
    hero = Player(50, 50)
    left = right = up = down = False
    bg.fill(Color("BLACK"))
    pygame.display.set_caption("Mario")
    clock = pygame.time.Clock()
    running = True
    entities = pygame.sprite.Group()
    platforms = []
    entities.add(hero)
    level = [
        "-------------------------",
        "-                       -",
        "-                       -",
        "-                       -",
        "-                       -",
        "-                       -",
        "-                       -",
        "-                       -",
        "-                       -",
        "-                       -",
        "-                       -",
        "-                       -",
        "-                       -",
        "-                       -",
        "-                       -",
        "-                       -",
        "-                       -",
        "-                       -",
        "-                       -",
        "-------------------------"]
    x = y = 0
    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)

            x += block_w
        y += block_h
        x = 0
    while running:
        clock.tick(30
                   )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_UP:
                up = True
            if event.type == KEYDOWN and event.key == K_LEFT:
                left = True
            if event.type == KEYDOWN and event.key == K_RIGHT:
                right = True
            if event.type == KEYDOWN and event.key == K_DOWN:
                down = True
            if event.type == KEYUP and event.key == K_UP:
                up = False
            if event.type == KEYUP and event.key == K_RIGHT:
                right = False
            if event.type == KEYUP and event.key == K_LEFT:
                left = False
            if event.type == KEYUP and event.key == K_DOWN:
                down = False

        screen.blit(bg, (0, 0))

        hero.update(left, right, up, down, platforms)
        entities.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
