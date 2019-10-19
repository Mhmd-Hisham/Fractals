#!/usr/bin/env python3

import time
import random
import subprocess

WIDTH, HEIGHT = 800, 400

XSHIFT = -500
YSHIFT = 0

MIN_X, MAX_Y = -1.2, 1.2
MIN_X, MAX_X = -2.4, 2.4

STEP = 10

BOUND = 600
TEST_ITERATIONS = 10
MAX_ITERATIONS = 100

WHITE = color(255)
randomRGB = lambda: (random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256))

mandlebrot_set = None

def draw_text():
    fill(WHITE)
    textSize(30)
    text("Bound: {}".format(BOUND), 20, 40)
    text("Test iterations: {}".format(TEST_ITERATIONS), 20, 70)

class MandlebrotSet():
    """ https://en.wikipedia.org/wiki/Mandelbrot_set """
    def __init__(self, 
                 screen_width, 
                 screen_height, 
                 min_x, 
                 max_x, 
                 min_y, 
                 max_y,
                 absolute_bound,
                 test_iterations, 
                 xshift=XSHIFT, 
                 yshift=YSHIFT):
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.min_x = min_x
        self.max_x = max_x
        
        self.min_y = min_y
        self.max_y = max_y
        
        self.absolute_bound = absolute_bound
        self.test_iterations = test_iterations

        self.xshift = xshift
        self.yshift = yshift
        

    def draw(self):
        loadPixels()
        pixelDensity(1)
        
        for x in range(self.screen_width):
            for y in range(self.screen_height):
            
                a = map(x, 0, self.screen_width, self.min_x, self.max_x) + \
                    map(self.xshift, -self.screen_width, self.screen_width, self.min_x, self.max_x)

                b = map(y, 0, self.screen_height, self.min_y, self.max_y) + \
                    map(self.yshift, -self.screen_height, self.screen_height, self.min_y, self.max_y)
    
                n = self.test((a, b))
                
                v = max(map(n, 0, self.test_iterations, 0, 256), 20)
                pixel_color = color(0) if n == self.test_iterations else color(v, 0, 0)
    
                index = x + y * width
                pixels[index] = pixel_color
    
        updatePixels()

    def test(self, c):
        """
            Checks whether the given complex number (a+bi) does not diverge 
            when iterated from z = 0, for f(z) = z^2 + c
    
            f(z) = z^2 + c
            f(f(z)) = c^2 + c
    
            c is a complex number (a + bi) where i = sqrt(-1)
            c^2 = (a+bi)*(a+bi) = a^2 + 2abi + b^2 * i^2
    
            c^2 = a^2 - b^2 + 2abi
    
        """
    
        c0 = tuple(c)
    
        a, b = c
        for i in range(self.test_iterations):
            aa = a * a
            bb = b * b
    
            ab2 = 2 * a * b
    
            a = aa - bb + c0[0]
            b = ab2 + c0[1]
    
            if abs(a + b) > self.absolute_bound:
                return i
    
        return self.test_iterations

def setup():
    global mandlebrot_set
    global MAX_Y, MIN_Y
    global MAX_X, MIN_X

    # size(WIDTH, HEIGHT)
    fullScreen()
    
    ratio = width/float(height)
    
    MIN_Y, MAX_Y = -1.2, 1.2
    MIN_X, MAX_X = MIN_Y*ratio, MAX_Y*ratio
    
    mandlebrot_set = MandlebrotSet(width, 
                                   height, 
                                   MIN_X,
                                   MAX_X, 
                                   MIN_Y, 
                                   MAX_Y, 
                                   absolute_bound=BOUND,
                                   test_iterations=TEST_ITERATIONS, 
                                   xshift=XSHIFT, 
                                   yshift=YSHIFT)
    mandlebrot_set.draw()
    draw_text()

def draw():
    global STEP, TEST_ITERATIONS
    
    mandlebrot_set.test_iterations = TEST_ITERATIONS
    
    # Uncomment this section and comment the one below to control the fractal using the keyboard
    # if keyPressed:
    #     mandlebrot_set.absolute_bound = BOUND
    #     mandlebrot_set.draw()
    #     draw_text()
    

    time.sleep(0.5)
    mandlebrot_set.draw()
    draw_text()
    TEST_ITERATIONS += STEP
    if TEST_ITERATIONS >= MAX_ITERATIONS or TEST_ITERATIONS <= 0:
        STEP *= -1

def keyPressed():
    """
        Press i/I to increase/decrease the number of test iterations by (STEP).
        Press b/B to increase/decrease the absolute bound value by (10).
    """
    global TEST_ITERATIONS, BOUND
    
    if key == 'i':
        TEST_ITERATIONS += STEP
    
    elif key == 'I':
        TEST_ITERATIONS -= STEP
    
    elif key == 'b':
        BOUND += 10

    elif key == 'B':
        BOUND -= 10
