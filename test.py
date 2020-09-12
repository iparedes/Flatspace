import pygame


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

screen.fill((0, 0, 0))
#pygame.draw.circle(screen, (255,255,255), (50,50),50, 1)
draw_ellipse(screen,(50,50),100,25,30)

done = False

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        
        pygame.display.flip()
