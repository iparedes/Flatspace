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

def rect_to_screen(rectangle):
    sc_top=H/2-rectangle.top
    sc_left=rectangle.left+W/2
    r=pg.Rect(sc_left,sc_top,rectangle.width,rectangle.height)
    return r
    #screenX = cartX + screen_width / 2
    #screenY = screen_height / 2 - cartY

def main():
    pg.init()
    screen = pg.display.set_mode((W, H))
    done = False
    #
    a=Rectangle(0,0,100,50)
    b=Rectangle(10,10,10,5)

    r=rect_to_screen(a)
    s=rect_to_screen(b)

    x=a.intersects(b)
    print(x)


    x=50
    while not done:
        screen.fill((0,0,0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
        x+=1

        pg.draw.rect(screen,(200,200,200),r,1)
        pg.draw.rect(screen,(0,200,0), s,1)
        #pg.draw.circle(screen,(200,200,200),(x,50),20)
        pg.display.flip()
        pg.time.delay(100)
    exit()

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
    S.Sol.mass = 1000
    S.Sol.radius = 10000

    S.Sol.pos = Pos(1000, 1000)

    S.add_planet("Earth", 10, 5000, 50000, 200000, 45, 0)
    V = View(S, pg.Vector2(0, 0), 1000000)

    # rot=0
    # while rot<720:
    #     V.display.draw_ellipse(Pos(200,200),100,50,rot)
    #     rot+=10
    # V.display.draw()

    is_running = True
    while is_running:
        time_delta = V.display.clock.tick(60) / 1000.0
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
                        V.move(0, -MOVE_FACTOR)
                    if event.ui_element == V.display.down_button:
                        V.move(0, MOVE_FACTOR)
                    if event.ui_element == V.display.left_button:
                        V.move(-MOVE_FACTOR, 0)
                    if event.ui_element == V.display.right_button:
                        V.move(MOVE_FACTOR, 0)

            V.display.manager.process_events(event)
            mousex, mousey = pg.mouse.get_pos()
            t = str(mousex) + ' , ' + str(mousey)
            V.display.draw_text(V.display.WIDTH - 200, 10, t)
            x = V.area.left + (mousex * V.mperpixel)
            y = V.area.top - (mousey * V.mperpixel)
            t = str(x) + ' , ' + str(y)
            V.display.draw_text(20, 20, t)

        V.render()
        V.display.manager.update(time_delta)
        V.display.manager.draw_ui(V.display.screen)
        pg.display.flip()


if __name__ == "__main__":
    main()
