import pygame
from pygame import *
import pyganim
import sys

info = pygame.Surface((800, 30))
screen = pygame.Surface((800, 640))
window = pygame.display.set_mode((800, 670))


class Menu:
    """
    Класс меню, который отображается в начале и при нажатии Esc.
    """
    def __init__(self, buttons=[]):
        self.button = buttons
        self.map = 0

    def render(self, surface, font, num_punkt):
        """
        Функция отображения меню.
        """
        for i in self.button:
            if num_punkt == i[5]:
                surface.blit(font.render(i[2], 1, i[4]), (i[0], i[1] - 30))
            else:
                surface.blit(font.render(i[2], 1, i[3]), (i[0], i[1] - 30))

    def menu(self):
        """
        Функция в которой происхожит основная работа меню.
        """
        flag = False
        done = True
        font_menu = pygame.font.Font(None, 50)
        pygame.key.set_repeat(0, 0)
        pygame.mouse.set_visible(True)
        button = 0

        while done:
            info.fill((255, 255, 255))
            screen.fill((255, 255, 255))

            mouse_pos = pygame.mouse.get_pos()
            for i in self.button:
                if mouse_pos[0] > i[0] and mouse_pos[0] < i[0] + 155 and mouse_pos[1] > i[1] and mouse_pos[1] < i[1] + 50:
                    button = i[5]
            self.render(screen, font_menu, button)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = False
                    if event.key == pygame.K_UP:
                        if button > 0:
                            button -= 1
                    if event.key == pygame.K_DOWN:
                        if button < len(self.button) - 1:
                            button += 1
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button == 0:
                        done = False
                        self.new_game = False
                    elif button == 1:
                        exit()
                    elif button == 2:
                        flag = not flag
                        if flag:
                            mixer.music.pause()
                        else:
                            mixer.music.unpause()
                    elif button == 3:
                        self.new_game = True
                        self.map = 1
                        done = False
                    elif button == 4:
                        self.new_game = True
                        self.map = 2
                        done = False
            window.blit(info, (0, 0))
            window.blit(screen, (0, 30))
            pygame.display.flip()


class Platform(sprite.Sprite):
    """
    Класс блоков из которых состоит лабиринт.
    """
    def __init__(self, x, y):
        platform_w = 30
        platform_h = 30
        sprite.Sprite.__init__(self)
        self.image = Surface((platform_w, platform_h))
        self.image = image.load("image/block.png")
        self.rect = Rect(x, y, platform_w, platform_h)


class Cam(object):
    """
    Класс камеры, которая следует за персонажем.
    """
    def __init__(self, camera, width, height):
        self.camera = camera
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera(self.state, target.rect)


class Player(sprite.Sprite):
    """
    Класс персонажа.
    Создает персонаж и устанавливаются его характеристики.
    """
    def __init__(self, x, y):
        self.level = 0
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
        bolt_anim = []

        for anim in right_anim:
            bolt_anim.append((anim, speed_anim))

        self.boltAnimRight = pyganim.PygAnimation(bolt_anim)
        self.boltAnimRight.play()
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
        """
        Переносит игрока в начальные координаты.
        """
        self.teleporting(self.startX, self.startY)

    def teleporting(self, x, y):
        """
        Телепортирует игрока в полученные координаты.
        """
        self.rect.x = x
        self.rect.y = y

    def update(self, left, right, up, down, platforms):
        """
        Обновление координат персонажа.
        """
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
        """
        Проверка на столкновение игрока и объектов.
        """
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
                    self.level = 2


class Trap(Platform):
    """
    Класс ловушки, которая взаимодействует с игроком.
    """
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("image/trap_1.png")


class WinBlock(Platform):
    """
    Класс финиша.
    """
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("image/chest.png")




def camera_settings(camera, target_rect):
    """
    Основные параметры камеры.
    """
    left, top = target_rect[0:2]
    w, h = camera[-2:]
    left, top = -left + 800 / 2, -top + 640 / 2
    left = min(0, left)
    left = max(-(camera.width - 800), left)
    top = max(-(camera.height - 640), top)
    top = min(0, top)

    return Rect(left, top, w, h)


def main():
    """
    Основная функия программы.
    """
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
    entities_1 = pygame.sprite.Group()
    entities_2 = pygame.sprite.Group()
    platforms = []
    platforms_1 = []
    platforms_2 = []
    mixer.music.load("sounds/main_theme.ogg")
    mixer.music.play(-1)
    entities.add(hero)
    entities_2.add(hero)
    entities_1.add(hero)
    punkts = [(350, 230, 'Play', (11, 0, 77), (226, 139, 0), 0),
              (350, 270, 'Exit', (11, 0, 77), (226, 139, 0), 1),
              (350, 310, 'Music', (11, 0, 77), (226, 139, 0), 2),
              (350, 350, 'Level 1', (11, 0, 77), (226, 139, 0), 3),
              (350, 390, 'Level 2', (11, 0, 77), (226, 139, 0), 4)]
    game = Menu(punkts)
    game.menu()
    level_1 = [
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
    level = [
        "----------------------------------",
        "--             -- -             --",
        "--   --- -- -- -- -   --- -- -- --",
        "-    --- -- --*--     --- -- --*--",
        "-- -       -    - -----   --     -",
        "-    *   -        -   - ----- -- -",
        "-- ----- --- ---- - -       -    -",
        "-  ----- ---- --- - ------- -- ---",
        "-    --- ---- --- - ------  --   -",
        "- ------  --   -  -       -      -",
        "- -*  -- -------- -            - -",
        "- --- -- -      - --------- ---- -",
        "- --- -- - -  - - -          --* -",
        "- --- -- - -  - - - --------------",
        "- --- -- - -  - - -   -   -      -",
        "- --- -- - -  - - - - - - - - -  -",
        "- --- -- - -  - - - - - - - - -  -",
        "- -      - -  - - - - - - - - -  -",
        "- - ------ -  - - - - - - - - -  -",
        "- -        -**- - -   -   -   -  -",
        "- ------------- - -------------- -",
        "-       ------- *W*              -",
        "----------------------------------"]
    x = y = 0
    for row in level_1:
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
    run_music = pygame.mixer.Sound("sounds/run.ogg")
    total_level_width = len(level[0]) * 30
    total_level_height = len(level) * 30
    camera = Cam(camera_settings, total_level_width, total_level_height)
    flag_music = False
    pause = False
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
                pause = not pause
                if pause:
                    mixer.music.pause()
                else:
                    mixer.music.unpause()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run_music.stop()
                    flag_music = False
                    game.menu()

            if game.map == 1:
                game.map = 0
                x = y = 0
                for row in level_1:
                    for col in row:
                        if col == "-":
                            block = Platform(x, y)
                            entities_1.add(block)
                            platforms_1.append(block)
                        if col == "*":
                            trap = Trap(x, y)
                            entities_1.add(trap)
                            platforms_1.append(trap)
                        if col == "W":
                            win = WinBlock(x, y)
                            entities_1.add(win)
                            platforms_1.append(win)

                        x += block_w
                    y += block_h
                    x = 0

                entities = entities_1
                platforms = platforms_1

            elif game.map == 2 or hero.level == 2:
                game.map = 0
                hero.level = 0
                x = y = 0
                for row in level:
                    for col in row:
                        if col == "-":
                            block = Platform(x, y)
                            entities_2.add(block)
                            platforms_2.append(block)
                        if col == "*":
                            trap = Trap(x, y)
                            entities_2.add(trap)
                            platforms_2.append(trap)
                        if col == "W":
                            win = WinBlock(x, y)
                            entities_2.add(win)
                            platforms_2.append(win)

                        x += block_w
                    y += block_h
                    x = 0

                entities = entities_2
                platforms = platforms_2

        screen.blit(bg, (0, 0))
        for ent in entities:
            screen.blit(ent.image, camera.apply(ent))
        hero.update(left, right, up, down, platforms)
        if (left or right or up or down) == True:
            if flag_music == False:
                run_music.play(-1)
                flag_music = True
        else:
            run_music.stop()
            flag_music = False
        camera.update(hero)
        screen.blit(fon, (camera.apply(hero)[0] - 1000, camera.apply(hero)[1] - 950))
        pygame.display.flip()
        if game.new_game:
            run_music.stop()
            flag_music = False
            hero.die()
            game.new_game = False

        if hero.win:
            run_music.stop()
            flag_music = False
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
            run_music.stop()
            flag_music = False
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
