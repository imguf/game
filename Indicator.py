from kivy.graphics import *


class Indicator:
    
    def __init__(self, xpos, ypos, direc, border_w, border_h):
        self.xpos = xpos
        self.ypos = ypos
        self.direc = direc
        self.border_w = border_w
        self.border_h = border_h        
        
    def draw(self, widget, window_x, window_y, sq_w, sq_h):
        Color(0,1.,0)
        Rectangle(pos=(10+window_x + sq_w * self.xpos, 
                       10 + window_y + sq_h * self.ypos),\
                  size=(sq_w, sq_h))
                  
    def set_new_pos(self):
        if(self.direc == 1):
            self.xpos = self.border_w
        elif(self.direc == 2):
            self.xpos = -1
        elif(self.direc == 3):
            self.ypos = self.border_h
        elif(self.direc == 4):
            self.ypos = -1
    
    def get_x(self):
        return self.xpos
    
    def get_y(self):
        return self.ypos
        
    def set_x(self, xpos):
        self.xpos = xpos
        
    def set_y(self, ypos):
        self.ypos = ypos
        
    def set_border_size(self, x, y):
        self.border_w = x
        self.border_h = y
