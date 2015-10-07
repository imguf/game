from kivy.graphics import *


class Main_menu:
    """ this class describes how the main menu works"""    
    
    def __init__(self, status):
        self._status = status
        
        
    def draw(self, widget, width, height):
                
        # title image
        Rectangle(pos=(width//20,15 * height//20),\
                  size=(width,height - 14 * height //20))
        
        # start game button
        Rectangle(pos=(4* width//20, 11 * height//20),\
                  size=(15*width // 20, 3* height //20))
                  
        # Highscore button
        Rectangle(pos=(4 * width//20, 6 * height//20),\
                  size=(15*width // 20, 3*height//20))
        
        # options game button
        Rectangle(pos=(4* width//20, 1 * height//20), \
                  size=(15*width // 20, 3 * height //20))
    
    def touch_down(self, touch):
        """ this method is called when the player touches the screen while in
        the main menu. It takes the touch-position as a argument and checks
        if the touch is on a button"""
        
        xpos = touch.x
        ypos = touch.y
        
        
    
    
    def set_status(self, status):
        self._status = status
    
    def get_status(self):
        return(self._status)