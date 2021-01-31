import pygame
from misc import *
import random
import math

from PIL import Image
import requests



def sub_vec(veca, vecb):
    return pygame.Vector2((vecb.x - veca.x), (vecb.y - veca.y),)


def draw_text(screen, t_data, x, y, color,*,Left_justified=False,Right_justified=False,fill_back=False,Back_color=BLACK,Font_size=30):
    font = pygame.font.Font('./cour.ttf', Font_size)
    if fill_back:
        text = font.render(f"{t_data}", True, color,Back_color)
    else:
        text = font.render(f"{t_data}", True, color)

    textRect = text.get_rect()
    if Left_justified:
        textRect.midleft = (x,y)
    elif Right_justified:
        textRect.midright = (x, y)
    else:
        textRect.center = (x, y)


    screen.blit(text, textRect)


class Circle(pygame.sprite.Sprite):
    def __init__(self, username, x=WIDTH / 2, y=HEIGHT / 2,logo=None):
        pygame.sprite.Sprite.__init__(self)
        if logo != None:
            im = Image.open(requests.get(logo, stream=True).raw)
            self.image = pygame.image.fromstring(im.tobytes(), im.size, im.mode).convert()
        else:
            self.image = pygame.image.load('doomye.png')  # doomye.png'

        self.image = pygame.transform.scale(self.image, (45, 45))
        self.image_rect = self.image.get_rect()

        self.coord = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.radius = .04 * HEIGHT
        self.basecolor = WHITE
        self.color = self.basecolor
        self.username = username
        self.status = False
        self.is_bot = False
        self.is_dead = False
        self.mulitkill_flag = False
        self.kill_start = None
        self.direction = 0
        self.power = 0
        self.last_collided_with = None
        self.recent_kills = 0

    def bot_ai(self, hill):
        self.status = True
        temp = sub_vec(self.coord, hill.coord)
        e = 1
        error = pygame.Vector2(random.uniform(temp.x * -e, temp.x * e), random.uniform(temp.y * -e, temp.y * e))

        theta = math.atan2(temp.y + error.y, temp.x + error.x)
        self.direction = (theta)
        self.power = random.randint(0, abs(hill.radius // 13 + temp.length() // 20) + 1)

    def check_map_colision(self, other):
        if abs(self.coord.x - other.coord.x) < self.radius + other.radius:
            if abs(self.coord.y - other.coord.y) < self.radius + other.radius:
                if (math.sqrt((self.coord.x - other.coord.x) ** 2 + ( self.coord.y - other.coord.y) ** 2) <= self.radius + other.radius):
                    return False
        return True

    def check_colision(self, other):
        if abs(self.coord.x - other.coord.x) < self.radius + other.radius:
            if abs(self.coord.y - other.coord.y) < self.radius + other.radius:
                self.last_collided_with = other.username
                other.last_collided_with = self.username

                # I used this link as guide for writing this function;
                # https://stackoverflow.com/questions/345838/ball-to-ball-collision-detection-and-handling
                if (math.sqrt((self.coord.x - other.coord.x) ** 2 + (
                        self.coord.y - other.coord.y) ** 2) <= self.radius + other.radius):
                    if self == other:
                        return

                    collision = sub_vec(self.coord, other.coord)
                    distance = collision.length()
                    if distance == 0.0:
                        return
                    collision.x /= distance
                    collision.y /= distance
                    mtd = collision * (((self.radius + other.radius) - distance) / distance)
                    self.coord -= mtd * .51
                    other.coord += mtd * .51

                    self_initial_vel = self.vel.dot(collision)
                    other_initial_vel = other.vel.dot(collision)

                    self_final_vel = other_initial_vel
                    other_final_vel = self_initial_vel

                    self.vel += (self_final_vel - self_initial_vel) * collision
                    other.vel += (other_final_vel - other_initial_vel) * collision

    def impulse(self):
        # print(f'impulse called for {self.username}')

        if self.status == True:
            self.vel.x = math.cos(self.direction) * self.power
            self.vel.y = math.sin(self.direction) * self.power
            self.status = False

    def update(self):
        self.coord += self.vel
        self.vel *= .95
        if .1 > self.vel.x > -.1:
            self.vel.x = 0
        if .1 > self.vel.y > -.1:
            self.vel.y = 0





    def Hdraw(self, screen):

        if self.status:
            self.color = GREEN
        else:
            self.color = self.basecolor

            pygame.draw.circle(screen, self.color, self.coord, self.radius)

            if self.radius >= HEIGHT / 2:
                pygame.draw.circle(screen, WHITE, self.coord, (HEIGHT / 2), 4)

            x_nudge = 20
            y_nudge = 10
            if self.radius >= (HEIGHT / 4) + (HEIGHT / 4 / 2):
                pygame.draw.circle(screen, WHITE, self.coord, (HEIGHT / 4) + (HEIGHT / 4 / 2), 2)
                draw_text(screen, '15', self.coord.x - x_nudge,
                          self.coord.y - (HEIGHT / 4) - (HEIGHT / 4 / 2) - y_nudge, WHITE)

            if self.radius >= (HEIGHT / 4):
                pygame.draw.circle(screen, WHITE, self.coord, HEIGHT / 4, 2)
                draw_text(screen, '10', self.coord.x - x_nudge, self.coord.y - HEIGHT / 4 - y_nudge, WHITE)

            if self.radius >= (HEIGHT / 4 / 2):
                pygame.draw.circle(screen, WHITE, self.coord, HEIGHT / 4 / 2, 2)
                draw_text(screen, '5', self.coord.x - x_nudge, self.coord.y - HEIGHT / 4 / 2 - y_nudge, WHITE)

            draw_text(screen, '0', self.coord.x - x_nudge, self.coord.y - y_nudge, WHITE)

        pygame.draw.line(screen, WHITE, pygame.Vector2(self.coord.x - self.radius, self.coord.y),
                         pygame.Vector2(self.coord.x + self.radius, self.coord.y), 2)
        pygame.draw.line(screen, WHITE, pygame.Vector2(self.coord.x, self.coord.y - self.radius),
                         pygame.Vector2(self.coord.x, self.coord.y + self.radius), 2)

    def draw_sprite(self,screen):
        self.image_rect.center = (self.coord.x,self.coord.y)
        screen.blit(self.image,self.image_rect)

    def draw(self, screen):

        font = pygame.font.Font('./cour.ttf', 20)
        if self.status:
            self.color = GREEN
        else:
            self.color = self.basecolor

        pygame.draw.circle(screen, self.color, self.coord, self.radius)
        self.draw_sprite(screen)
        pygame.draw.circle(screen,self.color, self.coord, self.radius, 6)
        text = font.render(f"{self.username}", True, self.color)
        textRect = text.get_rect()
        textRect.center = (self.coord.x, self.coord.y - self.radius - 20)
        screen.blit(text, textRect)

