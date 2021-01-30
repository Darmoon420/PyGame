import pygame
from pygame import *
import pyganim


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        platform_w = 30
        platform_h = 30
        sprite.Sprite.__init__(self)
        self.image = Surface((platform_w, platform_h))
        self.image = image.load("image/block.png")
        self.rect = Rect(x, y, platform_w, platform_h)


class Cam(object):
    def __init__(self, camera, width, height):
        self.camera = camera
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera(self.state, target.rect)


class Player(sprite.Sprite):
    def __init__(self, x, y):
        self.move_speed = 5
        self.win = False
        self.life = False
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
        color_fon = "BLACK"
        self.image = Surface((800, 640))
        self.image.fill(Color(color_fon))
        self.image.set_colorkey(Color(color_fon))
        speed_anim = 60
        left_anim = [('image/left_1.png'),
                     ('image/left_2.png'),
                     ('image/left_3.png')]

        right_anim = [('image/right_1.png'),
                      ('image/right_2.png'),
                      ('image/right_3.png')]

        up_anim = [('image/up.png', 1)]
        stay_anim = [('image/stay.png', 1)]
        fon = [('image/fon.png', 1)]
        bolt_anim = []

        for anim in right_anim:
            bolt_anim.append((anim, speed_anim))

        self.boltAnimRight = pyganim.PygAnimation(bolt_anim)
        self.boltAnimRight.play()
        print(bolt_anim)
        bolt_anim = []
        for anim in left_anim:
            bolt_anim.append((anim, speed_anim))
        self.boltAnimLeft = pyganim.PygAnimation(bolt_anim)
        self.boltAnimLeft.play()

        self.boltAnimStay = pyganim.PygAnimation(stay_anim)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))

        self.boltAnimJump = pyganim.PygAnimation(up_anim)
        self.boltAnimJump.play()

        sprite.Sprite.__init__(self)

    def die(self):
        self.teleporting(self.startX, self.startY)

    def teleporting(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self, left, right, up, down, platforms):
        color = "BLACK"
        if up:
            self.y_change = -self.move_speed
            self.image.fill(Color(color))
            self.boltAnimJump.blit(self.image, (0, 0))
        if down:
            self.y_change = self.move_speed
        if left:
            self.x_change = -self.move_speed
            self.image.fill(Color(color))
            self.boltAnimLeft.blit(self.image, (0, 0))
        if right:
            self.x_change = self.move_speed
            self.image.fill(Color(color))
            self.boltAnimRight.blit(self.image, (0, 0))
        if not (left or right or down or up):
            self.x_change = 0
            self.y_change = 0
            self.image.fill(Color(color))
            self.boltAnimStay.blit(self.image, (0, 0))

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

                if isinstance(p, Trap):
                    self.die()
                    self.life = True

                elif isinstance(p, WinBlock):
                    self.win = True


class Trap(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("image/trap_1.png")


class WinBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("image/chest.png")


def camera_settings(camera, target_rect):
    left, top = target_rect[0:2]
    w, h = camera[-2:]
    left, top = -left + 800 / 2, -top + 640 / 2
    left = min(0, left)
    left = max(-(camera.width - 800), left)
    top = max(-(camera.height - 640), top)
    top = min(0, top)

    return Rect(left, top, w, h)


def main():
    fon = image.load('image/fon.png')
    pygame.init()
    block_h = 30
    block_w = 30
    size = 800, 640
    screen = pygame.display.set_mode(size)
    bg = Surface((800, 640))
    hero = Player(510, 30)
    left = right = up = down = False
    bg.fill(Color("BLACK"))
    pygame.display.set_caption("Mario")
    clock = pygame.time.Clock()
    running = True
    entities = pygame.sprite.Group()
    platforms = []
    mixer.music.load("sounds/main_theme.mp3")
    mixer.music.play(-1)
    entities.add(hero)
    level = [
        "----------------------------------",
        "---*           *- -*            --",
        "------ -- ---   - -   --- -- -- --",
        "-      --  --         --- -- --*--",
        "- --------  ----- -----   --    *-",
        "-*       -     *- -   - ----- -- -",
        "-------- --- ---- - -       -  * -",
        "-        --   --- - ------- -- ---",
        "---- --- -- - --- - ------  --   -",
        "-              *- -        --   *-",
        "- ------ -------- -            - -",
        "- ------ -      - --------- ---- -",
        "- ------ - -  - - -          --  -",
        "- ------ - -  - - - --------------",
        "- ------ - -  - - - -   -   -    -",
        "- ------ - -  - - - - - - - - -  -",
        "- ------ - -  - - - - - - - - -  -",
        "- -      - -  - - - - - - - - -  -",
        "- - ------ -  - - - - - - - - -  -",
        "- -        -**- - -   -   -   -* -",
        "- ------------- -*-------------- -",
        "-      *------- *W               -",
        "----------------------------------"]
    total_level_width = len(level[0]) * 30
    total_level_height = len(level) * 30
    camera = Cam(camera_settings, total_level_width, total_level_height)
    x = y = 0
    for row in level:
        for col in row:
            if col == "-":
                block = Platform(x, y)
                entities.add(block)
                platforms.append(block)
            if col == "*":
                trap = Trap(x, y)
                entities.add(trap)
                platforms.append(trap)
            if col == "W":
                win = WinBlock(x, y)
                entities.add(win)
                platforms.append(win)

            x += block_w
        y += block_h
        x = 0
        flPause = False
    while running:
        clock.tick(30)

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                flPause = not flPause
                if flPause:
                    mixer.music.pause()
                else:
                    mixer.music.unpause()

        screen.blit(bg, (0, 0))

        hero.update(left, right, up, down, platforms)
        camera.update(hero)
        for ent in entities:
            screen.blit(ent.image, camera.apply(ent))
        screen.blit(fon, (camera.apply(hero)[0] - 1000, camera.apply(hero)[1] - 950))
        pygame.display.flip()
        if hero.win:
            font = pygame.font.Font(None, 150)
            text = font.render("YOU WIN", True, "BlUE")
            text_x = size[0] // 2 - text.get_width() // 2
            text_y = size[1] // 2 - text.get_height() // 2
            screen.blit(text, (text_x, text_y))
            pygame.display.flip()
            time.wait(3600)
            hero.die()
            hero.win = False
        if hero.life:
            font = pygame.font.Font(None, 150)
            text = font.render("YOU DIED", True, "RED")
            text_x = size[0] // 2 - text.get_width() // 2
            text_y = size[1] // 2 - text.get_height() // 2
            screen.blit(text, (text_x, text_y))
            pygame.display.flip()
            time.wait(1200)
            hero.die()
            hero.life = False


if __name__ == '__main__':
    main()


