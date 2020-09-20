import math
import pygame as pg
from geometry import *


# mass in kg
# radius in m
# orbit data in m

class Body:
    def __init__(self, mass=0):
        self.pos = pg.Vector2(0, 0)
        self.mass = mass
        self.orbit = None
        self.parent = None
        self.name = ""

    def set_orbit(self, orbit, parent):
        self.orbit = orbit
        self.parent = parent
        self.orbit.focus = parent.pos

        x = self.orbit.c * math.cos(math.radians(self.orbit.incl))
        y = self.orbit.c * math.sin(math.radians(self.orbit.incl))
        t = Pos(self.orbit.focus.x + x, self.orbit.focus.y + y)
        self.orbit.center = t


class Planet(Body):
    def __init__(self, name="", mass=0, radius=0):
        Body.__init__(self, mass)
        self.name = name
        self.radius = radius

    # Returns the position of a planet at a given angle of the orbit
    # angle is the angle relative to the orbit, with 0 at the apoapsis
    # the position takes into account the angle relative to the orbit and the inclination of the orbit
    # def pos_planet(self, angle):
    #     # Let's calculate the position for the orbit with 0 incl
    #     a = self.orbit.a
    #     b = self.orbit.b
    #
    #     oneovera2 = 1 / a ** 2
    #     tan2overb2 = ((math.tan(math.radians(angle))) ** 2) / (b ** 2)
    #     x = math.sqrt(1 / (oneovera2 + tan2overb2))
    #     y = math.tan(math.radians(angle)) * x
    #     # x and y are relative to the center of the orbit
    #     Q = Pos(x, y)
    #     # distance to the center
    #     d = Q.distance(Pos(0,0))
    #
    #     # Now we rotate the Position the angle of inclination of the orbit
    #     x = d * math.cos(math.radians(angle + self.orbit.incl))
    #     y = d * math.sin(math.radians(angle + self.orbit.incl))
    #     Q=Pos(x,y)
    #     pos = Q + self.orbit.center
    #     return pos

    def pos_planet(self,angle):
        # angle is the alfa
        # orbit.incl is the theta
        alfa=angle
        sinalfa = math.sin(math.radians(alfa))
        cosalfa=math.cos(math.radians(alfa))
        a=self.orbit.a
        b=self.orbit.b
        sintheta=self.orbit._sintheta
        costheta=self.orbit._costheta

        x=int((a*cosalfa*costheta)-(b*sinalfa*sintheta))
        y=int((a*cosalfa*sintheta)+(b*sinalfa*costheta))

        Q=Pos(x,y)
        pos=Q+self.orbit.center
        return pos


class Sun(Body):
    def __init__(self, mass=0, radius=0):
        Body.__init__(self, mass)
        self.radius = radius


class SSystem:
    def __init__(self):
        self.Sol = Sun()
        self.Planets = []

    # init_pos is the angle relative to the orbit, with 0 at the apoapsis
    def add_planet(self, name, mass, radius, peri, apo, incl=0, init_pos=0):
        P = Planet(name=name, mass=mass, radius=radius)
        O = Orbit(peri, apo, incl)
        P.set_orbit(O, self.Sol)

        P.pos = P.pos_planet(init_pos)
        self.Planets.append(P)


class Orbit:

    def __init__(self, peri, apo, incl=0):
        if (peri > apo):
            (peri, apo) = (apo, peri)

        self.peri = peri
        self.apo = apo
        self.incl = incl

        # a: semi-major axis
        # b: semi-minor axis
        # c: distance from center to focus
        self.a = (self.peri + self.apo) / 2
        self.c = self.a - self.peri
        self.b = int(math.sqrt((self.a ** 2) - (self.c ** 2)))
        self.focus = None
        self.center = None  # position

        # to accelerate calculations
        self._costheta=math.cos(math.radians(incl))
        self._sintheta = math.sin(math.radians(incl))
