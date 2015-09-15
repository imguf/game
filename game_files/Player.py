from kivy.graphics import *


class Player:
    """ This is the player class"""
    
    def __init__(self, xpos, ypos, size_x, size_y, board_width, board_height):
        # sets the position of the player        
        self.xpos = xpos
        self.ypos = ypos
        
        self.board_width = board_width
        self.board_height = board_height
        
        # these are not used right now
        self.size_x = size_x
        self.size_y = size_y

        
    def draw(self, widget, window_x, window_y, sq_w, sq_h):
        """ draw out the player"""
        Rectangle(pos=(10+window_x + sq_w * self.xpos, 
                       10 + window_y + sq_h * self.ypos),\
                  size=(sq_w, sq_h))

        
    def move_up(self, direc):
        """ move the player up or down"""
        if(self.ypos != self.board_height-1 and direc == 1 or self.ypos != 0 and direc == -1):
            self.ypos += direc
        
    def move_right(self, direc):
        """ move the player left or right"""
        if(self.xpos != self.board_width-1 and direc == 1 or self.xpos != 0 and direc == -1):
            self.xpos += direc

    def set_x(self, xpos):
        """ sets the xpos variable"""
        self.xpos = xpos
        
    def set_y(self, ypos):
        """ sets the ypos variable"""
        self.ypos = ypos

    def get_x(self):
        """ returns the xpos variable"""
        return self.xpos
            
    def get_y(self):
        """ returns the ypos variable"""
        return self.ypos