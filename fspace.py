import math
import pygame as pg
from geometry import *


# mass in kg
# radius in m
# orbit data in m

G=6.673*10**(-11) # N•m2/kg2.

class Body:
    def __init__(self, mass=0):
        self.pos = Pos(0, 0) # True anomaly
        self.posE = Pos(0,0) # Eccentric anomaly
        self.mass = mass
        self.orbit = None
        self.parent = None
        self.name = ""
        self.T=0 # Orbital period

    def set_orbit(self, orbit, parent):
        self.orbit = orbit
        self.parent = parent
        self.orbit.focus = parent.pos
        self.T=(2*math.pi)*math.sqrt(self.orbit.a**3/G*self.parent.mass)
        # OjO
        self.T=864000

        #x=self.orbit.c
        #y=0
        #t=Pos(x,y)
        # sets the center of the orbit in relation to the focus to account for the inclination shift
        x = self.orbit.c * math.cos(math.radians(self.orbit.incl))
        y = self.orbit.c * math.sin(math.radians(self.orbit.incl))
        # **
        #t = Pos(self.orbit.focus.x + x, self.orbit.focus.y + y)
        t = Pos(self.orbit.focus.x - x, self.orbit.focus.y - y)
        self.orbit.center = t

    # places the body in the orbit at a given angle of the true anomaly
    def set_pos(self,angle):
        # angle is the alfa. True anomaly. 0 degrees is at periapsis
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

    # sets the pos of the body according to the time (in seconds) since the periapsis
    def set_pos_time(self,t):
        # E is the eccentric anomaly t seconds after the periapsis
        E=(t*2*math.pi)/self.T
        # calculate the position of E
        x=self.orbit.a*math.cos(E)
        y = self.orbit.a * math.sin(E)
        # calculate the position of the true anomaly
        x+=self.orbit.center.x
        y=y*(self.orbit.b/self.orbit.a)
        y+=self.orbit.center.y
        self.pos=Pos(x,y)


    def get_eccentric_anomaly_pos(self):
        # get the pos of eccentric anomaly
        y=self.pos.x*(self.orbit.a/self.orbit.b)
        E=Pos(x,y)
        return E

    # returns the angle of the true anomaly (in degrees=
    def get_true_anomaly(self):
        # calculates distance from the current position to the focus
        d=self.pos.distance(self.parent.pos)
        # the sin of the true anomaly is the y coord over the distance
        nu=math.asin(self.pos.y/d)
        return math.radians(nu)


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

    # def pos_planet(self,angle):
    #     # angle is the alfa. True anomaly. 0 degrees is at periapsis
    #     # orbit.incl is the theta
    #     alfa=angle
    #     sinalfa = math.sin(math.radians(alfa))
    #     cosalfa=math.cos(math.radians(alfa))
    #     a=self.orbit.a
    #     b=self.orbit.b
    #     sintheta=self.orbit._sintheta
    #     costheta=self.orbit._costheta
    #
    #     x=int((a*cosalfa*costheta)-(b*sinalfa*sintheta))
    #     y=int((a*cosalfa*sintheta)+(b*sinalfa*costheta))
    #
    #     Q=Pos(x,y)
    #     pos=Q+self.orbit.center
    #     return pos


class Sun(Body):
    def __init__(self, mass=0, radius=0):
        Body.__init__(self, mass)
        self.radius = radius

class Circle(Body):
    def __init__(self,pos,radius):
        Body.__init__(self,0)
        self.radius=radius
        self.pos=pos


class SSystem:
    def __init__(self):
        self.Sol = Sun()
        self.Planets = []

    # init_pos is the angle relative to the orbit, with 0 at the apoapsis
    def add_planet(self, name, mass, radius, peri, apo, incl=0, init_pos=0):
        P = Planet(name=name, mass=mass, radius=radius)
        O = Orbit(peri, apo, incl)
        P.set_orbit(O, self.Sol)

        P.pos = P.set_pos(init_pos)
        self.Planets.append(P)
        return P


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
