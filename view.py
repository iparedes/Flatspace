import pygame as pg
from display import *
from geometry import *
import math


class View:

    # w: width in meters of the view
    # pos: center point of the view rectangle
    def __init__(self, System, pos=Pos(0, 0), width=0):
        height = int(width * 0.75)
        self.area = Rectangle(int(pos.x - width / 2), int(pos.y + height / 2), width, height)

        self.scale = 100
        self.system = System

        self.objects = []
        self.display = Display(1024)
        self.mperpixel = int(self.area.width / self.display.WIDTH)
        pass

    def set_center(self, pos):
        self.area.center = pos

    # factor: percentage of zoom increase (positive level) or decrease (negative level) of the current vi
    def zoom(self, level):

        self.scale -= level
        factor = (100 - level) / 100
        self.area.width *= factor
        self.area.height *= factor
        # x=self.area.center.x
        # y=self.area.center.y
        # self.area = Rectangle(int(x - self.area.width / 2), int(y - self.area.height / 2), self.area.width, self.area.height)
        self.mperpixel = int(self.area.width / self.display.WIDTH)

    # moves the display (x,y) units
    def move(self, x, y):
        if y == 0:
            vert_step = 0
        else:
            vert_step = self.area.height / y
        if x == 0:
            hori_step = 0
        else:
            hori_step = self.area.width / x
        p = Pos(self.area.center.x + hori_step, self.area.center.y + vert_step)
        self.area.center = p
        # print(self.area.__dict__)
        # print(self.area.center.__dict__)

    def in_view(self, body):
        try:
            a = body.area
        except:
            r = body.radius
            a = Rectangle(body.pos.x - r, body.pos.y + r, 2 * r, 2 * r)

        return self.area.overlap(a)

    # translates a position from the view to the display
    def trans(self, pos):
        # xp=int(self.display.WIDTH*(pos.x-self.area.left)/self.area.width)
        # yp=int(self.display.HEIGHT*(pos.y-self.area.top)/self.area.height)
        # xp=(self.display.WIDTH/self.area.width)*(pos.x+self.area.left)+self.display.WIDTH/2
        # yp = (self.display.HEIGHT/2)-((self.display.HEIGHT/self.area.height)*pos.y)

        xp = int((self.display.WIDTH/self.area.width)*(pos.x-self.area.left))
        yp = int((self.display.HEIGHT/self.area.height)*(self.area.top-pos.y))

        return Pos(xp, yp)

    def render(self):
        if self.in_view(self.system.Sol):
            pos = self.trans(self.system.Sol.pos)
            rad = int(self.system.Sol.radius / self.mperpixel)
            # when the scale is too big, radius can be 0, fix it
            if rad<1:
                rad=1
            self.display.draw_circle(pos, rad)
        for p in self.system.Planets:
            #t="Rendering "+p.name
            #print(t)
            if self.in_view(p):
                pos = self.trans(p.pos)
                rad = int(p.radius / self.mperpixel)
                if rad == 0:
                    rad = 1
                self.display.draw_circle(pos, rad)
                # draw orbit
                pos = self.trans(p.orbit.focus)
                pos.x -= p.orbit.peri / self.mperpixel
                pos.y -= p.orbit.b / self.mperpixel
                width = 2 * p.orbit.a / self.mperpixel
                height = 2 * p.orbit.b / self.mperpixel
                self.display.draw_ellipse(pos, width, height, p.orbit.incl, (80, 80, 80))
        for o in self.objects:
            if self.in_view(o):
                pos=self.trans(o.pos)
                # OjO if we add more things than circles we need to manage the non-existence of the radius
                rad = int(o.radius / self.mperpixel)
                self.display.draw_circle(pos,rad)

            pass


        # t=str(self.area.center.x)+' , '+str(self.area.center.y)
        # self.display.draw_text(20,20,t)
        self.display.draw()
