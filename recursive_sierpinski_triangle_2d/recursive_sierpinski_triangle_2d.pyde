#!/usr/bin/env python3

import time
import random

WIDTH, HEIGHT = 1200, 600

LEVEL = 0
MAX_LEVEL = 10
LENGTH = 1000

BLACK = color(0)
WHITE = color(255)
BACKGROUND = BLACK

randomRGB = lambda: (random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256))

def draw_text():
    fill(WHITE)
    textSize(40)
    text("Level: {}".format(LEVEL), 20, 60)

class Triangle:
    def __init__(self, p0, p1, p2, color=(200, 0, 5)):
        self.p0 = p0.copy()
        self.p1 = p1.copy()
        self.p2 = p2.copy()
        self.color = color

    def get_child_triangle_points(self):

        pA = self.mid_point2d(self.p0, self.p2)
        pB = self.mid_point2d(self.p0, self.p1)
        pC = self.mid_point2d(self.p1, self.p2)

        return pA, pB, pC

    @staticmethod
    def mid_point2d(p0, p1):
        return PVector((p0.x + p1.x) / 2, (p0.y + p1.y) / 2)
    
    @staticmethod
    def calculate_triangle_points(p0, length):
        """
                        p3
                       . .
                      . . .
            length   .  .  .  length
                    .   .   .
                   .    .    .
                  .     .     .
                p1. . .(p0). . .p2
                
                dist(p1, p2) = length
                dist(p1, p3) = length
                dist(p2, p3) = length
                
                Given p0 and length, the function returns p1, p2, p3.
        """
        
        l2 = length**2
        
        p1 = PVector(p0.x - length / 2, p0.y)
        p2 = PVector(p0.x + length / 2, p0.y)
        p3 = PVector(p0.x, p0.y - sqrt(l2 - 0.25 * l2))
    
        return p1, p2, p3
    

def draw_sierpinski_triangle(triangle_obj, level):
    """
            (p2)*
               ***
              *****
         (pA)*******(pC)
            *********
           ***********
      (p0)*************(p1)
              (pB)
    """        
    
    if level > 0:
        pA, pB, pC = triangle_obj.get_child_triangle_points()
        p0, p1, p2 = triangle_obj.p0, triangle_obj.p1, triangle_obj.p2

        if level == LEVEL:
            fill(*triangle_obj.color)
            triangle(p0.x, p0.y, p1.x, p1.y, p2.x, p2.y)
    
        r, g, b = triangle_obj.color

        c1 = (r + 23, g + 23, b + 20)
        c2 = (r + 23, g + 20, b + 23)
        c3 = (r + 20, g + 23, b + 23)

        fill(*c1)
        noStroke()
        triangle(pA.x, pA.y, pC.x, pC.y, pB.x, pB.y)

        t1 = Triangle(p0, pB, pA, c1)
        t2 = Triangle(pB, p1, pC, c2)
        t3 = Triangle(pA, pC, p2, c3)

        draw_sierpinski_triangle(t1, level - 1)
        draw_sierpinski_triangle(t2, level - 1)
        draw_sierpinski_triangle(t3, level - 1)

def setup():
    fullScreen()
    # size(WIDTH, HEIGHT)

    background(BACKGROUND)    
    draw_text()

def draw():
    global LEVEL
    
    p0 = PVector(width/2, height-10)
    p1, p2, p3 = Triangle.calculate_triangle_points(p0, LENGTH)
    
    # Uncomment this section and comment the one below to control the fractal using the keyboard
    # if keyPressed:
    #     background(BACKGROUND)
    #     draw_text()
    #     draw_sierpinski_triangle(Triangle(p1, p2, p3), LEVEL)


    background(BACKGROUND)
    draw_text()
    draw_sierpinski_triangle(Triangle(p1, p2, p3), LEVEL)
    LEVEL = (LEVEL+1)%MAX_LEVEL
    time.sleep(0.4)

def keyPressed():
    """
          Press l/L to increase/decrease the number of levels of the Sierpinski Triangle.
    """
    global LEVEL
    
    
    if key == 'l':
        LEVEL += 1

    elif key == 'L':
        LEVEL -= 1
