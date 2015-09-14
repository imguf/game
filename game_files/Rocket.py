from kivy.graphics import *


class Rocket:
    def __init__(self, xpos, ypos, direc):
        self.xpos = xpos
        self.ypos = ypos
        self.start_x = xpos
        self.start_y = ypos
        self.speed = 350
        self.max_speed = 1000
        
        self.direc = direc
        
    def draw(self, widget, window_x, window_y, sq_w, sq_h):
        """ draws the rocket"""
        Color(1.,0,0)        
        
        if(self.direc == 1 or self.direc == 2):
            Rectangle(pos=(80 + window_x + self.xpos, 20 + window_y + self.ypos * sq_h),\
                      size=(sq_w - 30, sq_h - 30))
        elif(self.direc == 3 or self.direc == 4):
            Rectangle(pos=( 20 + window_x + self.xpos * sq_w, 80 + window_y + self.ypos),\
                      size=(sq_w-30, sq_h-30))
    
    def move(self, dt):
        if(self.direc == 1):
            self.xpos -= self.speed *dt
        elif(self.direc == 2):
            self.xpos += self.speed *dt
        elif(self.direc == 3):
            self.ypos -= self.speed *dt
        elif(self.direc == 4):
            self.ypos += self.speed *dt
        
    def get_x(self):
        """ return the xpos"""
        return self.xpos
    
    def get_y(self):
        """ return the ypos"""
        return self.ypos
        
    def get_direc(self):
        
        return self.direc
        
    def get_start_x(self):
        return self.start_x
        
    def get_start_y(self):
        return self.start_y
    
    def change_speed(self):
        """
        if(self.speed * 1.1 < self.max_speed):        
            self.speed *= 1.1
        else:
            self.speed = self.max_speed
            """
        self.speed = 1000
    def set_start_x(self, xpos):
        self.start_x = xpos
        
    def set_start_y(self, ypos):
        self.start_y = ypos
    
    def set_direc(self, direc):
        self.direc = direc
        
    def set_x(self, xpos):
        """ set the xpos"""
        self.xpos = xpos
        
    def set_y(self, ypos): 
        """ set the ypos"""
        self.ypos = ypos