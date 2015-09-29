from kivy.graphics import *


class Rocket:
    """ This is the Rocket-class"""
    def __init__(self, xpos, ypos, direc, play_field_width = 0, play_field_height = 0):
        self.xpos = xpos
        self.ypos = ypos
        self.start_x = xpos
        self.start_y = ypos
        self.play_field_width = play_field_width
        self.play_field_height = play_field_height
        self.speed = 75
        self.max_speed = 1000
        
        self.direc = direc
        
    def draw(self, widget, window_x, window_y, sq_w, sq_h):
        """ draws the rocket"""
        Color(1.,0,0)        
        
        if(self.direc == 1 or self.direc == 2):
            Rectangle(pos=(window_x + self.xpos * 1.1, window_y * 1.5 + self.ypos * sq_h),\
                      size=(sq_w *0.7, sq_h *0.7))
        elif(self.direc == 3 or self.direc == 4):
            Rectangle(pos=(2 *window_x + self.xpos * sq_w, window_y + self.ypos * 1.1),\
                      size=(sq_w * 0.7, sq_h * 0.7))
    
    def move(self, dt):
        """ moves the rocket depending on the direction"""
        if(self.direc == 1):
            self.xpos -= self.speed * dt * (self.play_field_width/100)
        elif(self.direc == 2):
            self.xpos += self.speed * dt * (self.play_field_width/100)
        elif(self.direc == 3):
            self.ypos -= self.speed * dt * (self.play_field_height/100)
        elif(self.direc == 4):
            self.ypos += self.speed * dt * (self.play_field_height/100)
        
    def get_x(self):
        """ return the xpos"""
        return self.xpos
    
    def get_y(self):
        """ return the ypos"""
        return self.ypos
        
    def get_direc(self):
        """ returns the direction of the rocket"""
        return self.direc
        
    def get_start_x(self):
        """ returns the start x position"""
        return self.start_x
        
    def get_start_y(self):
        """ returns the start y position"""
        return self.start_y
    

    def set_start_x(self, xpos):
        """ sets the start x position"""
        self.start_x = xpos
        
    def set_start_y(self, ypos):
        """ sets the start y position"""
        self.start_y = ypos
    
    def set_direc(self, direc):
        """ sets the new direction"""
        self.direc = direc
        
    def set_x(self, xpos):
        """ set the xpos"""
        self.xpos = xpos
        
    def set_y(self, ypos): 
        """ set the ypos"""
        self.ypos = ypos
        
        
    def set_screen_size(self, w,h):
        """ gives teh rocket the correct screensize"""
        self.play_field_width = w
        self.play_field_height = h




        
        