from kivy.graphics import *


class Backgrounds:
    """this class descibes how the background will work"""

    # constructor    
    def __init__(self, backgrounds, width, height):
        
        # a list to hold all the backgrounds
        self.backgrounds = backgrounds
        
        # a list to hold all the current backgrounds
        self.current_backgrounds = [self.backgrounds[0], self.backgrounds[1]]
        
        self.next_background = 2

        
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
        
        # if the y position is more than the negative hight, move the background down
        # else set the ypos to 0
        if(self.ypos > self.play_field_height * -1):        
            self.ypos -= self.play_field_height // 20 * dt * self.speed
        else:
            self.change_current_bg()
            self.ypos = 0
    
    
    def change_current_bg(self):
        """ this method changes the current backgrounds when one is not visible"""
        self.current_backgrounds.pop(0)
        self.current_backgrounds.append(self.backgrounds[self.next_background])
        self.next_background += 1
    