import pygame
import math
from display import *
from view import *
from fspace import *


def draw_ellipse(screen,pos,w,h,rot):
    surface = pygame.Surface((w,h))
    surface.fill((255,0,0))
    surface = surface.convert_alpha()
    size = (0, 0, w,h)
    ellipse = pygame.draw.ellipse(surface, (255,255,255), size,2)
    blit_rect=screen.blit(surface,pos)
    org_center=blit_rect.center
    surface2 = pygame.transform.rotate(surface, rot)
    rot_rect=surface2.get_rect()
    #screen.blit(surface2,rot_rect)
    rot_rect.center=org_center
    #surface2.fill((0,255,0))
    screen.blit(surface2,rot_rect)


pygame.init()
pygame.display.set_caption("Test")
screen = pygame.display.set_mode((800,600))

S = SSystem()
S.Sol.mass = 1000
S.Sol.radius = 1000
S.Sol.pos = Pos(0, 0)
S.add_planet("test", 10,100,10000,50000,30)
V = View(S, pg.Vector2(0, 0), 160000)

# beta=30
# h=0
# k=0
#
# a=100
# b=30
#
# sinbeta=math.sin(math.radians(-beta))
# cosbeta=math.cos(math.radians(-beta))
#
#
# for alfa in range(0,360,5):
#     sinalfa=math.sin(math.radians(alfa))
#     cosalfa = math.cos(math.radians(alfa))
#
#     x=int((a*cosalfa*cosbeta)-(b*sinalfa*sinbeta))
#     y=int((a*cosalfa*sinbeta)+(b*sinalfa*cosbeta))
#
#     x+=100
#     y+=100
#
#     print((x,y))
#     screen.set_at((x,y),(250,250,250))

done=False
while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True

        V.render()
        pygame.display.flip()

# screen.fill((0, 0, 0))
# #pygame.draw.circle(screen, (255,255,255), (50,50),50, 1)
# draw_ellipse(screen,(50,50),100,25,30)
#
# done = False
#
#
# while not done:
#         for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                         done = True
#
#         pygame.display.flip()