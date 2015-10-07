from kivy.graphics import *


class Main_menu:
    """ this class describes how the main menu works"""    
    
    def __init__(self, status):
        self._status = status
        
        
    def draw(self, widget, width, height):
        Rectangle(pos=(100,100),size=(100,100))
        
        
    
    def set_status(self, status):
        self._status = status
    
    def get_status(self):
        return(self._status)