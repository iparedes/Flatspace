
import math
import pygame as pg

#test

# mass in kg
# radius in m
# orbit data in m

class Body:
    def __init__(self,mass=0):
        self.pos=pg.Vector2(0,0)
        self.mass=mass
        self.orbit=None



class Planet(Body):
    def __init__(self,mass=0,radius=0):
        Body.__init__(self,mass)
        self.radius=radius

class Sun(Body):
    def __init__(self,mass=0,radius=0):
        Body.__init__(self,mass)
        self.radius=radius
        self.planets=[]


class SSystem:
    def __init__(self):
        self.Sol=Sun()
        self.Planets=[]

class Orbit:

    def __init__(self,peri,apo,incl=0):

        if (peri>apo):
            (peri,apo)=(apo,peri)

        self.peri=peri
        self.apo=apo
        self.incl=incl

        # a: semi-major axis
        # b: semi-minor axis
        # c: distance from center to focus
        self.a=(self.peri+self.apo)/2
        self.c=self.a-self.apo
        self.b=math.sqrt((self.a**2)-(self.c**2))


