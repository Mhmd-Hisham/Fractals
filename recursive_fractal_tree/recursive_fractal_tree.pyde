#!/usr/bin/env python3

import time
import math
import random

WIDTH, HEIGHT = 1300, 800

LEVELS = 1
MAX_LEVEL = 13

LENGTH = 150

RIGHT_BRANCH_RATIO = 0.84
LEFT_BRANCH_RATIO = 0.84

RIGHT_ROTATION_ANGLE = 0.389
LEFT_ROTATION_ANGLE = 0.389

BACKGROUND = color(20)

class Line:
    def __init__(self, p0, p1, c=(150, 0, 0)):
        self.p0 = p0.copy()
        self.p1 = p1.copy()
        self.color = c

def calculate_points(p0, 
                    p1, 
                    right_rotation_angle=RIGHT_ROTATION_ANGLE, 
                    left_rotation_angle=LEFT_ROTATION_ANGLE,
                    right_branch_ratio=RIGHT_BRANCH_RATIO,
                    left_branch_ratio=LEFT_BRANCH_RATIO):
    """
        Given the two points, p0, p1, the function returns three points
        (pA, pB, pC) to draw a fractal tree.


        (pC)           (pB)
           .           .
            .         .
             .       .
              .     .
               .   . 
                (p1) 
                 .
                 .
                 .
                 p0

    """

    dx = p1.x - p0.x
    dy = p1.y - p0.y
    
    distance = dist(p1.x, p1.y, p0.x, p0.y)
    angle = math.atan2(dy, dx)
    
    right_branch_len = distance * right_branch_ratio
    left_branch_len = distance * left_branch_ratio

    pB = PVector()
    pB.x = p1.x + math.cos(angle + right_rotation_angle) * right_branch_len
    pB.y = p1.y + math.sin(angle + right_rotation_angle) * right_branch_len

    pC = PVector()
    pC.x = p1.x + math.cos(angle - left_rotation_angle) * left_branch_len
    pC.y = p1.y + math.sin(angle - left_rotation_angle) * left_branch_len

    return pB, pC

def fractalTree(line_obj, level):
        
    # Base Condition
    if level > 0:
        p0 = line_obj.p0
        p1 = line_obj.p1
        c = line_obj.color
        
        pB, pC = calculate_points(p0, p1,
                            right_rotation_angle=RIGHT_ROTATION_ANGLE, 
                            left_rotation_angle=LEFT_ROTATION_ANGLE,
                            right_branch_ratio=RIGHT_BRANCH_RATIO,
                            left_branch_ratio=LEFT_BRANCH_RATIO)

        stroke(*c)
        line(p0.x, p0.y, p1.x, p1.y)
        
        r, g, b = c
        c1 = (r+10, g, b+20)
        c2 = (r+10, g+20, b)
        
        l1 = Line(p1, pB, c1)
        l2 = Line(p1, pC, c2)

        # Recurse right and left
        fractalTree(l1, level - 1)
        fractalTree(l2, level - 1)

def show_values():
    # Draw values on the screen

    noStroke()
    textSize(20)
    text("Levels: {}".format(LEVELS), 20, 50)
    text("Right Branch Ratio: {}".format(RIGHT_BRANCH_RATIO), 20, 70)
    text("Left  Branch Ratio: {}".format(LEFT_BRANCH_RATIO), 20, 90)
    text("Right Rotation Angle: {}".format(RIGHT_ROTATION_ANGLE), 20, 110)
    text("Left  Rotation Angle: {}".format(LEFT_ROTATION_ANGLE), 20, 130)

def setup():
    fullScreen()
    # size(WIDTH, HEIGHT)
    background(BACKGROUND)

    LEVELS = 1
    
def draw():
    global LEVELS

    p0 = PVector(width / 2, height)
    p1 = PVector(width / 2, height - LENGTH)

    # Uncomment this section and comment the one below to control the fractal using the keyboard
    # if keyPressed:
    #     background(BACKGROUND)
    #     fractalTree(Line(p0, p1), LEVELS)

    #     show_values()

    background(BACKGROUND)
    fractalTree(Line(p0, p1), LEVELS)
    show_values()
    time.sleep(0.3)
    LEVELS = (LEVELS+1)%MAX_LEVEL+1

def keyPressed():
    """
       Press r/R to increase/decrease the right rotation angle.
       Press l/L to increase/decrease the left rotation angle.

       Press a/A to increase/decrease the right branch ratio.
       Press b/B to increase/decrease the left branch ratio.

       Press g/G to increase/decrease the number of levels of the Fractal Tree.
    """
    global LEFT_ROTATION_ANGLE, RIGHT_ROTATION_ANGLE
    global RIGHT_BRANCH_RATIO, LEFT_BRANCH_RATIO
    global LEVELS

    if key == 'r':
        RIGHT_ROTATION_ANGLE = (RIGHT_ROTATION_ANGLE + .05) % TWO_PI

    elif key == 'R':
        RIGHT_ROTATION_ANGLE = (RIGHT_ROTATION_ANGLE - .05) % TWO_PI
    
    elif key == 'l':
        LEFT_ROTATION_ANGLE = (LEFT_ROTATION_ANGLE + .05) % TWO_PI

    elif key == 'L':
        LEFT_ROTATION_ANGLE = (LEFT_ROTATION_ANGLE - .05) % TWO_PI

    elif key == 'a':
        RIGHT_BRANCH_RATIO = (RIGHT_BRANCH_RATIO + .01)

    elif key == 'A':
        RIGHT_BRANCH_RATIO = (RIGHT_BRANCH_RATIO - .01)

    elif key == 'b':
        LEFT_BRANCH_RATIO = (LEFT_BRANCH_RATIO + .01)

    elif key == 'B':
        LEFT_BRANCH_RATIO = (LEFT_BRANCH_RATIO - .01)

    elif key == 'g':
        LEVELS += 1

    elif key == 'G':
        LEVELS -= 1
