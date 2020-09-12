import pygame as pg
import pygame_gui
from fspace import *
from display import *
from view import *
from geometry import *

ZOOM_FACTOR=10
MOVE_FACTOR=20

def main():
    # pg.init()
    # screen = pg.display.set_mode((400, 300))
    # done = False
    #
    # x=50
    # while not done:
    #     screen.fill((0,0,0))
    #     for event in pg.event.get():
    #         if event.type == pg.QUIT:
    #             done = True
    #     x+=1
    #     pg.draw.circle(screen,(200,200,200),(x,50),20)
    #     pg.display.flip()
    #     pg.time.delay(100)

    S=SSystem()
#    S.Sol.mass=2*10**30
#    S.Sol.radius=696000*10**6

    # S.Sol.mass=2*10**30
    # S.Sol.radius=7*10**9
    #
    # P=Planet(mass=6*10**24,radius=1*10**6)
    # O=Orbit(1*10**10,1*10**11,30)
    # P.set_orbit(O,S.Sol)
    # P.pos.xy=1*10**11,0
    # S.Planets.append(P)


    V=View(S,pg.Vector2(0,0),0.2*10**13)

    V.display.draw_ellipse(Pos(50,50),100,50,45)
    V.display.draw()

    is_running=True
    while is_running:
        time_delta=V.display.clock.tick(60)/1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_running = False

            if event.type == pg.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == V.display.zoomin_button:
                        V.zoom(ZOOM_FACTOR)
                    if event.ui_element == V.display.zoomout_button:
                        V.zoom(-ZOOM_FACTOR)
                    if event.ui_element == V.display.up_button:
                        V.move(0,-MOVE_FACTOR)
                    if event.ui_element == V.display.down_button:
                        V.move(0,MOVE_FACTOR)
                    if event.ui_element == V.display.left_button:
                        V.move(-MOVE_FACTOR,0)
                    if event.ui_element == V.display.right_button:
                        V.move(MOVE_FACTOR,0)

            V.display.manager.process_events(event)
            mousex, mousey = pg.mouse.get_pos()
            t=str(mousex)+' , '+str(mousey)
            V.display.draw_text(V.display.WIDTH-200,10,t)

        #V.render()
        V.display.manager.update(time_delta)
        V.display.manager.draw_ui(V.display.screen)
        pg.display.flip()



if __name__ == "__main__":
    main()

