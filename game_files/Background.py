from kivy.graphics import *


class Backgrounds:
    """this class descibes how the background will work"""

    # constructor    
    def __init__(self, backgrounds, width, height):
        
        # a list to hold all the backgrounds
        self.backgrounds = backgrounds
        
        # a list to hold all the current backgrounds
        self.current_backgrounds = [self.backgrounds[0], self.backgrounds[1]]
        
        
        # y position of the backgrounds
        self.ypos = 0        
        
        # screensize
        self.play_field_height = height
        self.play_field_width = width
        
        #moving speed
        self.speed = 0
        
    def draw(self):
        """ this method draws the backgrounds on the screan"""
        for n in range(len(self.current_backgrounds)):
            # draw all the backgrounds            
            
            Rectangle(source=self.current_backgrounds[n], pos=(0,self.ypos + self.play_field_height * n), 
                      size=(self.play_field_width, self.play_field_height))
    
    def move(self, dt):
        """ this method moves the backgrounds down on the screen"""
        
    
    
    def change_current_bg(self):
        """ this method changes the current backgrounds when one is not visible"""
    
    