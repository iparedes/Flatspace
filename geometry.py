import math

class Pos:

    def __init__(self,x,y):
        self.x=x
        self.y=y

    def __add__(self, other):
        return Pos(self.x+other.x,self.y+other.y)

    def __sub__(self, other):
        return Pos(self.x-other.x,self.y-other.y)

    def coords(self):
        return (self.x,self.y)

    def distance(self,other):
        return math.sqrt(((self.x-other.x)**2)+((self.y-other.y)**2))


# the reference frame for the rectangle is Cartesian
class Rectangle:

    def __init__(self,left,top,width,height):
        self._top=top
        self._left=left
        self._width=width
        self._height=height
        self._center=Pos(int(left+(width/2)),int(top-(height/2)))
        self._bottom=self._top-self._height
        self._right=self._left+self._width

    def intersects(self,other):
        res= self.left > other.right or self.right < other.left or \
            self.top<other.bottom or self.bottom > other.top
        return not res


    @property
    def center(self):
        return self._center
    @center.setter
    # p: tupla (x,y)
    def center(self,p):
        x=p[0]
        y=p[1]
        self._center=Pos(x,y)
        self.left=int(x-(self.width/2))
        self.top = int(y - (self.height / 2))

    @property
    def left(self):
        return self._left
    @left.setter
    def left(self,v):
        self._left=v
        xc=v+int(self.width/2)
        self._right=v+self.width
        self._center.x=xc

    @property
    def right(self):
        return self._right
    @right.setter
    def right(self,v):
        self._right=v
        xc=v-int(self.width/2)
        self._left=v-self.width
        self._center.x=xc


    @property
    def top(self):
        return self._top
    @top.setter
    def top(self, v):
        self._top = v
        yc = v - int(self._height / 2)
        self._center.y = yc
        self._bottom=v-self._height

    @property
    def bottom(self):
        return self._bottom
    @bottom.setter
    def bottom(self,v):
        self._bottom=v
        yc=v+int(self._height/2)
        self._center.y=yc
        self._top=v+self._height

    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, v):
        self._width = v
        self.left = self._center.x - int(v / 2)


    @property
    def height(self):
        return self._height
    @height.setter
    def height(self, v):
        self._height = v
        self.top=self._center.y + int(v / 2)


# ****** CHECK THE OVERLAP FUNCTION ********
    # True if there is overlap between self and r
    def overlap(self,r):
        dx=min(self.left+self.width,r.left+r.width)-max(self.left,r.left)
        dy = min(self.top + self.height, r.top + r.height) - max(self.top, r.top)
        if (dx>=0) and (dy>=0):
            return True
        else:
            return False

# class Rectangle:
#
#     def __init__(self,left,top,width,height):
#         self.top=top
#         self.left=left
#         self.width=width
#         self.height=height
#         self.center=Pos(int(left+(width/2)),int(top+(height/2)))
#
#     # pos: Pos
#     def set_center(self,x,y):
#         self.center=Pos(x,y)
#         self.left=int(x-(self.width/2))
#         self.top = int(y - (self.height / 2))
#
#     # True if there is overlap between self and r
#     def overlap(self,r):
#         dx=min(self.left+self.width,r.left+r.width)-max(self.left,r.left)
#         dy = min(self.top + self.height, r.top + r.height) - max(self.top, r.top)
#         if (dx>=0) and (dy>=0):
#             return True
#         else:
#             return False

