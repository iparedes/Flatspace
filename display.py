import pygame as pg
import pygame_gui
import sys
from geometry import *
import random
import math


SCREEN_RATIO=0.75 # 4:3

WHITE = (200, 200, 200)
LINE_WIDTH=2

class Display:
    def __init__(self,width):

        pg.init()

        self.WIDTH=width
        self.HEIGHT=int(width*SCREEN_RATIO)
        pg.display.set_caption("Test")
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))

        # self.blank=pg.Surface((self.WIDTH, self.HEIGHT),flags=pg.SRCALPHA)
        # self.blank.fill((0,0,0))
        # self.blank.set_alpha(255)

        self.running = True
        # Holds surfaces that will be blitted
        # each element is a dictionary with keys 'surface' and 'pos'
        self.surfaces=[]

        #
        self.manager=pygame_gui.UIManager((self.WIDTH,self.HEIGHT))
        self.clock=pg.time.Clock()

        self.interface()

    def interface(self):
        margin=10
        from_bottom=80
        start_pos=(margin,self.HEIGHT-from_bottom)
        button_width=20
        button_sep=5

        pos=start_pos
        self.zoomin_button=pygame_gui.elements.UIButton(relative_rect=pg.Rect(pos, (button_width, button_width)),
                                                        text='+',
                                                        manager=self.manager)
        pos=(pos[0],pos[1]+button_width+button_sep)
        self.zoomout_button=pygame_gui.elements.UIButton(relative_rect=pg.Rect(pos, (button_width, button_width)),
                                                         text='-',
                                                         manager=self.manager)

        pos=(start_pos[0]+(1*button_sep)+button_width,start_pos[1]+button_width/2)
        self.left_button=pygame_gui.elements.UIButton(relative_rect=pg.Rect(pos, (button_width, button_width)),
                                                         text='<',
                                                         manager=self.manager)


        pos=(pos[0]+button_width+ button_sep,pos[1])
        self.right_button=pygame_gui.elements.UIButton(relative_rect=pg.Rect(pos, (button_width, button_width)),
                                                         text='>',
                                                         manager=self.manager)

        pos=(pos[0]-(button_width/2)-button_sep/2,pos[1]-button_width)
        self.up_button=pygame_gui.elements.UIButton(relative_rect=pg.Rect(pos, (button_width, button_width)),
                                                         text='^',
                                                         manager=self.manager)
        pos=(pos[0],pos[1]+button_sep+2*button_width-button_sep)
        self.down_button=pygame_gui.elements.UIButton(relative_rect=pg.Rect(pos, (button_width, button_width)),
                                                         text='v',
                                                         manager=self.manager)




    def draw(self):
        self.screen.fill((0,0,0))
        for s in self.surfaces:
            self.screen.blit(s['surface'], s['pos'])
        self.surfaces=[]


    def test_circle(self):
        #pg.draw.circle(self.main_surface,(255,0,0),(100,100),50)
        pg.draw.ellipse(self.screen,(0,0,255),pg.Rect(200,200,50,100))

    # pos is a Vector2
    def draw_circle(self,pos,r):
        #surface=pg.Surface((2*r,2*r))
        surface = pg.Surface((2 * r, 2 * r), pg.SRCALPHA, 32)
        surface = surface.convert_alpha()
        pg.draw.circle(surface,WHITE,(r,r),r,1)
        s={}
        p=pos+Pos(-r,-r)
        s['pos']=p.coords()
        s['surface']=surface
        self.surfaces.append(s)

    def draw_rectangle(self,pos,rect):
        pass

    # Adds a ellipse to the surfaces to be blitted
    # pos is a Pos, the center of the ellipse
    def draw_ellipse(self,pos,w,h,rot,color=WHITE):

        # draws the ellipse alligned to the XY axis as if rot=0
        surface = pg.Surface((w,h),pg.SRCALPHA, 32)
        surface = surface.convert_alpha()
        size = (0, 0, w,h)
        ellipse = pg.draw.ellipse(surface, color, size,LINE_WIDTH)
        # saves the center of the ellipse for later
        orig_center=ellipse.center

        # Draw the focus (the one in the left side)
        # r is the distance from the center to the focus

        r = int(math.sqrt((w / 2) ** 2 - (h / 2) ** 2))

        # **
        #pg.draw.circle(surface,WHITE,(int(w/2)-r,int(h/2)),1)
        pg.draw.circle(surface,WHITE,(int(w/2)+r,int(h/2)),1)


        # Creates a new rotated surface. Beware that it is not really a rotated suface, but a bigger new one that
        # has the rotated original surface inside
        surface2 = pg.transform.rotate(surface, rot)

        # moves the rotated surface to match the center of the original one
        rot_rect=surface2.get_rect()
        new_center=rot_rect.center
        deltax=orig_center[0]-new_center[0]
        deltay=orig_center[1]-new_center[1]
        pos+=Pos(deltax,deltay)
        # so at this point, we have the original ellipse rotated from the center
        # but we need it rotated from the focus, so we need to move it again

        # moves to match the focus
        # calculates the new position of the focus
        orig_focus=Pos(-r,0)
        # **
        #newx = -r * math.cos(math.radians(rot))
        #newy = -r * math.sin(math.radians(rot))
        newx = r * math.cos(math.radians(rot))
        newy = r * math.sin(math.radians(rot))
        # calculates the delta between the old and new focus
        #
        deltax=(orig_focus.x-newx)
        deltay=(newy-orig_focus.y)
        pos += Pos(deltax, deltay)

        #surface2.fill((255,0,0))

        s={}
        s['pos']=pos.coords()
        s['surface']=surface2
        self.surfaces.append(s)


    def draw_text(self,x,y,text):
        pygame_gui.elements.UIButton(relative_rect=pg.Rect((x,y), (200,20)),
                                                         text=text,
                                                         manager=self.manager)

        

# #let's create a surface to hold our ellipse:
# surface = pg.Surface((320, 240))
#
# red = (180, 50, 50)
# size = (0, 0, 300, 200)
#
# #drawing an ellipse onto the
# ellipse = pg.draw.ellipse(surface, red, size)
#
# #new surface variable for clarity (could use our existing though)
# #we use the pg.transform module to rotate the original surface by 45°
# surface2 = pg.transform.rotate(surface, 45)
#
# while running:
#     screen.fill((255, 250, 200))
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             pg.quit()
#             sys.exit()
#     screen.blit(surface2, (100, 100))
#     pg.display.update()