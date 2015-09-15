from kivy.graphics import *


class Indicator:
    """ This is the indicator class"""
    
    def __init__(self, xpos, ypos, direc, bord_w, bord_h):
        self.xpos = xpos
        self.ypos = ypos
        self.direc = direc
        self.bord_w = bord_w
        self.bord_h = bord_h        
        
    def draw(self, widget, window_x, window_y, sq_w, sq_h):
        """ This function controlls the drawing of the indicator"""
        Color(0,1.,0)
        Rectangle(pos=(10+window_x + sq_w * self.xpos, 
                       10 + window_y + sq_h * self.ypos),\
                  size=(sq_w, sq_h))
                  
    def set_new_pos(self):
        """ This function gives the indicator a new position depending on wich 
        direction that the rocket are coming from"""
        if(self.direc == 1):
            self.xpos = self.bord_w
        elif(self.direc == 2):
            self.xpos = -1
        elif(self.direc == 3):
            self.ypos = self.bord_h
        elif(self.direc == 4):
            self.ypos = -1
    
    def get_x(self):
        """returns the x position"""
        return self.xpos
    
    def get_y(self):
        """ returns the y position"""
        return self.ypos
        
    def set_x(self, xpos):
        """ sets the x position"""
        self.xpos = xpos
        
    def set_y(self, ypos):
        """ sets the y position"""
        self.ypos = ypos
        
    def set_border_size(self, x, y):
        """ Updates the border size"""
        self.bord_w = x
        self.bord_h = y
