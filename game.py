from fspace import *
from view import *

ZOOM_FACTOR = 10
MOVE_FACTOR = 20

class Game(object):
    def __init__(self):
        self.done = False
        self.SS = SSystem()

        self.max_apo=0
        self.load_data()
        self.V=View(self.SS, self.SS.Sol.pos, 4*self.max_apo)

        self.fps = 60
        self.clock = pg.time.Clock()
        self.spawn_timer = 0
        self.click_timer=0
        self.spawn_frequency = 3000  # milliseconds

    def load_data(self):
        file1 = open('data', 'r')
        Lines = file1.readlines()
        for l in Lines:
            l.strip()
            if l[0] != '#':
                l.rstrip()
                items = l.split(',')
                if items[0] == "Sun":
                    self.SS.Sol.mass = float(items[1])
                    self.SS.Sol.radius = float(items[2])
                    self.SS.Sol.pos = Pos(0, 0)
                else:
                    name=items[0]
                    mass=float(items[1])
                    radius = float(items[2])
                    peri = float(items[3])
                    apo = float(items[4])
                    incl = float(items[5])
                    pos = float(items[6])
                    if apo>self.max_apo:
                        self.max_apo=apo
                    self.SS.add_planet(name,mass,radius,peri,apo,incl,pos)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            if event.type == pg.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.V.display.zoomin_button:
                        self.V.zoom(ZOOM_FACTOR)
                    if event.ui_element == self.V.display.zoomout_button:
                        self.V.zoom(-ZOOM_FACTOR)
                    if event.ui_element == self.V.display.down_button:
                        self.V.move(0, -MOVE_FACTOR)
                    if event.ui_element == self.V.display.up_button:
                        self.V.move(0, MOVE_FACTOR)
                    if event.ui_element == self.V.display.left_button:
                        self.V.move(-MOVE_FACTOR, 0)
                    if event.ui_element == self.V.display.right_button:
                        self.V.move(MOVE_FACTOR, 0)
            else:
                if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    if self.click_timer == 0:  # First mouse click.
                                        print('click')
                                        self.click_timer = 1  # Start the timer.
                                    # Click again before 0.5 seconds to double click.
                                    elif self.click_timer < 250:
                                        print('double click')
                                        self.click_timer = 0
                                        mousex, mousey = pg.mouse.get_pos()
                                        x = self.V.area.left + (mousex * self.V.mperpixel)
                                        y = self.V.area.top - (mousey * self.V.mperpixel)
                                        self.V.area.center=Pos(x,y)
                                        self.V.zoom(ZOOM_FACTOR)
                # Increase timer after mouse was pressed the first time.
                if self.click_timer != 0:
                    self.click_timer += self.dt
                    # Reset after 0.5 seconds.
                    if self.click_timer >= 250:
                        print('too late')
                        self.click_timer = 0
            self.V.display.manager.process_events(event)
            self.interface()


    def update(self, dt):
        pass

    #     self.spawn_timer += dt
    #     if self.spawn_timer >= self.spawn_frequency:
    #         print "SPAWN"
    #         self.spawn_timer -= self.spawn_frequency
    #         Enemy(self.screen_rect.center, self.enemies)
    #     self.enemies.update(dt)

    def draw(self):
        #self.screen.fill(pg.Color("gray10"))
        #self.enemies.draw(self.screen)
        self.V.render()
        self.V.display.manager.update(self.dt)
        self.V.display.manager.draw_ui(self.V.display.screen)

    def interface(self):
        mousex, mousey = pg.mouse.get_pos()
        t = str(mousex) + ' , ' + str(mousey)
        self.V.display.draw_text(self.V.display.WIDTH - 200, 10, t)
        x = self.V.area.left + (mousex * self.V.mperpixel)
        y = self.V.area.top - (mousey * self.V.mperpixel)
        t = str(x) + ' , ' + str(y)
        self.V.display.draw_text(20, 20, t)


    def run(self):
        while not self.done:
            self.dt = self.clock.tick(self.fps)
            #print(self.dt)
            self.event_loop()
            self.update(self.dt)
            self.draw()
            pg.display.update()

# if __name__ == "__main__":
#     game = Game()
#     game.run()
#     pg.quit()
#     sys.exit()
