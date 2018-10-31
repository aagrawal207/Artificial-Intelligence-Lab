import pygame, sys
from pygame.locals import *
from math import sin, cos, radians
from fuzzification import compute_current

pygame.init()

WINDOWSIZE = 800
TIMETICK = 1
BOBSIZE = 15
epsilon_theta = [3, 2, 5]
epsilon_omega = [2, 2, 4]
epsilon_curr = [1, 2, 4, 3, 5, 6]

window = pygame.display.set_mode((WINDOWSIZE, WINDOWSIZE))
pygame.display.set_caption("Inverted Pendulum Fuzzy Logic")

screen = pygame.display.get_surface()
screen.fill((255, 255, 255))

PIVOT = (WINDOWSIZE //2 , 9 * WINDOWSIZE // 10)
SWINGLENGTH = 320


class BobMass(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.theta = 1.2
        self.dtheta = -3
        # Rect(left, top, width, height)
        self.rect = pygame.Rect(int(PIVOT[0] - SWINGLENGTH * cos(self.theta)),
                                int(PIVOT[1] - SWINGLENGTH * sin(self.theta)),
                                1, 1)
        self.draw()

    def recomputeAngle(self):

        current = compute_current(
            self.theta, self.dtheta, epsilon_theta, epsilon_omega, epsilon_curr)
        t = TIMETICK / 1000
        theta_new = self.theta + self.dtheta * t + current * 0.5 * t * t
        omega_new = self.dtheta + current * t
        self.theta, self.dtheta = theta_new, omega_new
        print(theta_new, omega_new)

        # Rect(left, top, width, height)
        self.rect = pygame.Rect(PIVOT[0] -
                                SWINGLENGTH * sin(self.theta),
                                PIVOT[1] -
                                SWINGLENGTH * cos(self.theta), 1, 1)

    def draw(self):
        # pygame.draw.circle(Surface, color, pos, radius, width=0)
        # pos is a tuple of (x, y)
        pygame.draw.circle(screen, (0, 0, 0), PIVOT, 5, 0)
        pygame.draw.circle(screen, (0, 0, 0), self.rect.center, BOBSIZE, 0)
        # aaline(Surface, color, startpos, endpos, blend=1)
        pygame.draw.aaline(screen, (0, 0, 0), PIVOT, self.rect.center)
        # line(Surface, color, start_pos, end_pos, width=1)
        pygame.draw.line(screen, (0, 0, 0), (0, PIVOT[1]), (WINDOWSIZE, PIVOT[1]))

    def update(self):
        self.recomputeAngle()
        screen.fill((255, 255, 255))
        self.draw()


bob = BobMass()
clock = pygame.time.Clock()


TICK = USEREVENT
pygame.time.set_timer(TICK, TIMETICK)


def input(events):
    for event in events:
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == TICK:
            bob.update()
# flag = True
# while flag:
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             flag = False
#     pygame.display.flip()
#     clock.tick(60)
#     bob.update()
#
while True:
    # clock.tick(60)
    input(pygame.event.get())
    pygame.display.flip()
