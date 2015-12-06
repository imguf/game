from kivy.graphics import *


class Indicator:
    """ This is the indicator class"""
    
    def __init__(self, xpos, ypos, direc, board_w, board_h):
        self.xpos = xpos
        self.ypos = ypos
        self.direc = direc
        self.board_w = board_w
        self.board_h = board_h
        self.current_image = "img/indicators/LindicatorV2.png"
        self.images = ["img/indicators/LindicatorV2.png",\
                       "img/indicators/RindicatorV2.png",\
                       "img/indicators/DindicatorV2.png",\
                       "img/indicators/UindicatorV2.png"]
        
    def draw(self, widget, window_x, window_y, sq_w, sq_h):
        """ This function controlls the drawing of the indicator"""
        Color(1,1,1)
        Rectangle(source=self.current_image, pos=(1.5*window_x + sq_w * self.xpos,
                       1.5*window_y + sq_h * self.ypos),\
                  size=(sq_w * 0.8, sq_h*0.75))
                  
    def set_new_pos(self, direc):
        """ This function gives the indicator a new position depending on wich 
        direction that the rocket are coming from"""
        if(direc == 1):
            self.xpos = self.board_w*0.98
        elif(direc == 2):
            self.xpos = -1*0.9
        elif(direc == 3):
            self.ypos = self.board_h*0.97
        elif(direc == 4):
            self.ypos = -1
            
        self.current_image = self.images[direc - 1]

    
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
        self.board_w = x
        self.board_h = y
