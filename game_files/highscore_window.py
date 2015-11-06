from kivy.graphics import *


class Highscore_window:
    """ this class describes how the highscore window 
        will look like and function"""
    
    def __init__(self):
        """ constructor takes the width and height of the
            screen and sets the values to the arguments"""
       
        
        self._active = False
        
        
    def draw(self, widget, width, height):
        """ this method draws out the window on the screen"""
        Rectangle(source=(""), pos=(width//20, height//20),\
                size=(19*width//20, 19*height//20))