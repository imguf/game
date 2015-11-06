from kivy.graphics import *

import highscore_window


class Main_menu:
    """ this class describes how the main menu works"""    
    
    def __init__(self, status):
        self._status = status
        self.width = 0
        self.height = 0
        
        self.highscore_window = highscore_window.Highscore_window()
        
    def draw(self, widget, width, height):
                
        # title image
        Rectangle(source="img/startmeny/testtitle.png", pos=(self.width//20,15 * self.height//20),\
                  size=(self.width,self.height - 14 * self.height //20))
        
        # start game button
        Rectangle(source="img/startmeny/testknappstart.png", pos=(4* self.width//20, 11 * self.height//20),\
                  size=(15*self.width // 20, 3* self.height //20))
                  
        # Highscore button
        Rectangle(source="img/startmeny/testknapphiscore.png", pos=(4 * width//20, 6 * height//20),\
                  size=(15*width // 20, 3*height//20))
        
        # options game button
        Rectangle(source="img/startmeny/testknappoptions.png", pos=(4* width//20, 1 * height//20), \
                  size=(15*width // 20, 3 * height //20))
                  
        self.highscore_window.draw(widget,width,height)
    
    def touch_down(self, touch):
        """ this method is called when the player touches the screen while in
        the main menu. It takes the touch-position as a argument and checks
        if the touch is on a button"""
        
        xpos = touch.x
        ypos = touch.y
        
        # if the startbutton is pressed
        if(xpos >= 4* self.width//20 and
            xpos < 4* self.width//20 + 15*self.width // 20 and
            ypos >= 11 * self.height // 20 and 
            ypos < 11 * self.height // 20 + 3 * self.height // 20):
                
                # set the menu to false                
                self._status = False
    
    
    def set_status(self, status):
        self._status = status
    
    def get_status(self):
        return(self._status)
        
    def set_size(self, width, height):
        self.width = width
        self.height = height