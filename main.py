import pygame as pg
import pygame_gui
from fspace import *
from display import *
from view import *
from geometry import *

ZOOM_FACTOR = 10
MOVE_FACTOR = 20
W=400
H=300

# def rect_to_screen(rectangle):
#     sc_top=H/2-rectangle.top
#     sc_left=rectangle.left+W/2
#     r=pg.Rect(sc_left,sc_top,rectangle.width,rectangle.height)
#     return r


def main():
    # pg.init()
    # screen = pg.display.set_mode((W, H))
    # done = False
    # #
    # a=Rectangle(0,0,100,50)
    # b=Rectangle(10,-10,10,5)
    #
    # r=rect_to_screen(a)
    # s=rect_to_screen(b)
    #
    # x=a.overlap(b)
    # print(x)
    #
    #
    # x=50
    # while not done:
    #     screen.fill((0,0,0))
    #     for event in pg.event.get():
    #         if event.type == pg.QUIT:
    #             done = True
    #     x+=1
    #
    #     pg.draw.rect(screen,(200,200,200),r,1)
    #     pg.draw.rect(screen,(0,200,0), s,1)
    #     #pg.draw.circle(screen,(200,200,200),(x,50),20)
    #     pg.display.flip()
    #     pg.time.delay(100)
    # exit()

    # S=SSystem()
    # S.Sol.mass=2*10**30
    # S.Sol.radius=696000*10**6
    #
    # S.Sol.mass=2*10**30
    # S.Sol.radius=7*10**9
    # S.Sol.pos=Pos(500000000000,10000)
    #
    # S.add_planet("Earth",6*10**24,1*10**6,1*10**10,1*10**11,0,0)
    #
    #
    # V=View(S,pg.Vector2(0,0),0.2*10**13)

    S = SSystem()
    S.Sol.mass = 1.989*10**30
    S.Sol.radius = 696*10**6

    S.Sol.pos = Pos(0, 0)

    # name, mass, radius, peri, apo, incl=0, init_pos=0
    S.add_planet("Mercury", 0.33*10**24, 2.44*10**6, 4.6*10**10, 6.98*10**10, 7, 0)
    S.add_planet("Venus", 4.87 * 10 ** 24, 6.05 * 10 ** 6, 1.08 * 10 ** 11, 1.09 * 10 ** 11, 0, 30)
    S.add_planet("Earth", 5.97*10**24, 6.38*10**6, 1.47*10**11, 1.52*10**11, 0, 60)
    S.add_planet("Mars", 0.642 * 10 ** 24, 3.40 * 10 ** 6, 2.07 * 10 ** 11, 2.49 * 10 ** 11, 0, 60)
    S.add_planet("Jupiter", 1898 * 10 ** 24, 7.15 * 10 ** 7, 7.41 * 10 ** 11, 8.17 * 10 ** 11, 3, 90)
    S.add_planet("Saturn", 568 * 10 ** 24, 6.03 * 10 ** 7, 1.35 * 10 ** 12, 1.51 * 10 ** 12, 3, 120)
    S.add_planet("Uranus", 86.8 * 10 ** 24, 2.56 * 10 ** 7, 2.74 * 10 ** 12, 3.00 * 10 ** 12, 1, 150)
    S.add_planet("Neptune", 102 * 10 ** 24, 2.48 * 10 ** 7, 4.44 * 10 ** 12, 4.55 * 10 ** 12, 2, 180)
    V = View(S, pg.Vector2(0, 0), 4.6*10**12)

    print(V.area.__dict__)
    print(V.area.center.__dict__)
    # rot=0
    # while rot<720:
    #     V.display.draw_ellipse(Pos(200,200),100,50,rot)
    #     rot+=10
    # V.display.draw()

    timer=0
    time_delta=0
    is_running = True
    while is_running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_running = False

            if event.type == pg.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == V.display.zoomin_button:
                        V.zoom(ZOOM_FACTOR)
                    if event.ui_element == V.display.zoomout_button:
                        V.zoom(-ZOOM_FACTOR)
                    if event.ui_element == V.display.down_button:
                        V.move(0, -MOVE_FACTOR)
                    if event.ui_element == V.display.up_button:
                        V.move(0, MOVE_FACTOR)
                    if event.ui_element == V.display.left_button:
                        V.move(-MOVE_FACTOR, 0)
                    if event.ui_element == V.display.right_button:
                        V.move(MOVE_FACTOR, 0)

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if timer == 0:  # First mouse click.
                        print('click')
                        timer = 0.001  # Start the timer.
                    # Click again before 0.5 seconds to double click.
                    elif timer < 0.2:
                        print('double click')
                        timer = 0
                        mousex, mousey = pg.mouse.get_pos()
                        x = V.area.left + (mousex * V.mperpixel)
                        y = V.area.top - (mousey * V.mperpixel)
                        V.area.center=Pos(x,y)
                        V.zoom(ZOOM_FACTOR)

            # Increase timer after mouse was pressed the first time.
            if timer != 0:
                timer += time_delta
                # Reset after 0.5 seconds.
                if timer >= 0.2:
                    print('too late')
                    timer = 0


            V.display.manager.process_events(event)
            mousex, mousey = pg.mouse.get_pos()
            t = str(mousex) + ' , ' + str(mousey)
            V.display.draw_text(V.display.WIDTH - 200, 10, t)
            x = V.area.left + (mousex * V.mperpixel)
            y = V.area.top - (mousey * V.mperpixel)
            t = str(x) + ' , ' + str(y)
            V.display.draw_text(20, 20, t)

        time_delta = V.display.clock.tick(60) / 1000.0

        V.render()
        V.display.manager.update(time_delta)
        V.display.manager.draw_ui(V.display.screen)
        pg.display.flip()


if __name__ == "__main__":
    main()
