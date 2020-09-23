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

time=0

S = SSystem()
S.Sol.mass = 1.989*10**30
S.Sol.radius = 1000
S.Sol.pos = Pos(0, 0)
P=S.add_planet("test", 200,2000,10000,100000,0,0)
V = View(S, pg.Vector2(0, 0), 250000)

P.name="xxx"
center=P.orbit.center
radius=P.orbit.a
C=Circle(center,radius)
V.objects.append(C)


done=False
nu=S.Planets[0].get_true_anomaly()
oldnu=nu
print(nu)
while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True

        V.render()
        pygame.display.flip()
        time+=3600
        #pos=S.Planets[0].set_pos(angle)
        S.Planets[0].set_pos_time(time)
        nu=S.Planets[0].get_true_anomaly()
        print(abs(nu-oldnu))
        oldnu=nu

        #S.Planets[0].pos=pos
        pg.time.wait(100)

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