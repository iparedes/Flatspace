import pygame as pg

pg.init()
pg.display.set_caption("Test")
screen = pg.display.set_mode((800,600))

while True:
    screen.fill((0, 0, 0))
    pg.draw.circle(screen, (200,200,200), (50,50),50, 1)
    pg.display.update()
    pg.time.delay(1000)