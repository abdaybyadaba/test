import pygame.sprite
import pygame
from settings import *
from utils.spritesheet import SpriteSheet

class Player(pygame.sprite.Sprite):
    def __init__(self, life_num):
        super().__init__()
        self.w, self.h = self.size = (42, 70)

        self.frames = {'right': [pygame.transform.scale(pygame.image.load(f"imgs/moving/r{i}.png"), self.size) for i in
                                 range(1, 6)],
                       'left': [pygame.transform.scale(pygame.image.load(f"imgs/moving/l{i}.png"), self.size) for i in
                                range(1, 6)],
                       'stand': pygame.transform.scale(pygame.image.load("imgs/moving/0.png"), self.size)}
        self.walk_speed = 3
        self.direction_idx = 0  # 1 - right , -1 - left, 0 - stand, 2 - fall
        self.is_jump = False
        self.t = DEFAULT_JUMP_H
        self.anim_number = 0
        self.block_vertical = 0  # 0- give permission 1 - not give permission

        self.image = self.frames[DIRECTION_MAP[self.direction_idx]]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(10, 334)
        self.game_over = False
        self.n_lifes = life_num


    def move_right(self, platform_speed):
        if self.rect.x + self.walk_speed + platform_speed > WIN_W:
            self.rect.x = -self.w
        else:
            self.rect.x = self.rect.x + self.walk_speed + platform_speed
        self.direction_idx = 1

    def move_left(self, platform_speed):
        self.rect.x = max(0, self.rect.x - self.walk_speed + platform_speed)
        self.direction_idx = -1

    def move_vertical(self, platform_speed):
        self.rect.y = self.rect.y + platform_speed

    def jump(self, sprites, player):
        if self.t < -10:
            self.stop_jump()
        else:
            if self.block_vertical == 0:
                print(self.block_vertical)
                self.rect.x += self.direction_idx * self.walk_speed * 2
                self.rect.y -= self.walk_speed * self.t

            if self.rect.x < 0:
                self.rect.x = 0
            elif self.rect.x + self.w > WIN_W:
                self.rect.x = WIN_W - self.w
            self.t -= 1

    def stop_jump(self):
        self.is_jump = False
        self.t = 10

    def stand(self, platform_speed):
        self.direction_idx = 0
        self.rect.x += platform_speed
        print("all ok")

    def fall(self):
        if self.block_vertical == 1:
            self.direction_idx = 0
            #self.n_lifes -= 1
            #if self.n_lifes == 0:
                #self.game_over = True
        else:
            self.rect.y += 5 # обновлено

    def update(self):
        direction = DIRECTION_MAP[self.direction_idx]
        if direction == "stand":
            self.image = self.frames[direction]
        elif direction == "fall" and not self.game_over:
            self.fall()
        else:
            self.image = self.frames[direction][self.anim_number // 6]
            self.anim_number = 0 if (self.anim_number + 1) == 30 else self.anim_number + 1

    def check_touch_winfloor(self):
        if self.rect.y >= (WIN_H - self.rect.size[0]):
            self.n_lifes -= 1
            return True
        else:
            self.direction_idx = 2

    def move_player(self, dp_speed_x, dp_speed_y, sprites, player):
        self.move_vertical(dp_speed_y)
        keys = pygame.key.get_pressed()
        sep1, sep2 = 0, 0

        l = pygame.sprite.spritecollideany(player, sprites)
        if not type(l) == type(None):
            if self.rect.bottom > l.rect.centery:
                if (self.rect.right + dp_speed_x) > l.rect.left and self.rect.centerx < l.rect.centerx:
                    sep2 = 1
                if (self.rect.left - dp_speed_x) < l.rect.right and self.rect.centerx > l.rect.centerx:
                    sep1 = 1
            if self.rect.bottom >= l.rect.top:
                self.block_vertical = 1
        else:
            sep1, sep2 = 0, 0
            self.block_vertical = 0



        if keys[pygame.K_LEFT] and sep1 == 0:
            self.move_left(dp_speed_x)
        elif keys[pygame.K_RIGHT] and sep2 == 0:
            self.move_right(dp_speed_x)

        elif keys[pygame.K_SPACE]:
            self.is_jump = True
            self.jump(sprites, player)
        else:
            self.stand(dp_speed_x)

    def kill_player(self, sprites_group):
        pygame.sprite.Sprite.remove(self, sprites_group)


