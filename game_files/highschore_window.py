from kivy.graphics import *


class Highscore_window:
    """ this class describes how the highscore window 
        will look like and function"""
    
    def __init__(self, s_width, s_height):
        """ constructor takes the width and height of the
            screen and sets teh values to the arguments"""
        self._screen_width = s_width
        self._screen_height = s_height
        
        self._active = False
        
        
        