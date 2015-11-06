from kivy.graphics import *

import highscore_window


class Main_menu:
    """ this class describes how the main menu works"""    
    
    def __init__(self, status):
        self._status = status        
        self.highscore_window = highscore_window.Highscore_window()
        
    def draw(self, widget, width, height):
                
        # title image
        Rectangle(source="img/startmeny/testtitle.png", pos=(self.width//20,15 * self.height//20),\
                  size=(self.width,self.height - 14 * self.height //20))
        
        if(self.highscore_window.get_active() == False):
            # start game button
            Rectangle(source="img/startmeny/startbtn.png", pos=(4* self.width//20, 11 * self.height//20),\
                      size=(15*self.width // 20, 3* self.height //20))
                      
            # Highscore button
            Rectangle(source="img/startmeny/hiscorebtn.png", pos=(4 * width//20, 6 * height//20),\
                      size=(15*width // 20, 3*height//20))
            
            # options game button
            Rectangle(source="img/startmeny/optionsbtn.png", pos=(4* width//20, 1 * height//20), \
                      size=(15*width // 20, 3 * height //20))
                  
        # if the highscore window is active, draw it out
        elif(self.highscore_window.get_active()):
            self.highscore_window.draw(widget,width,height)
    
    
    
    def touch_down(self, touch):
        """ this method is called when the player touches the screen while in
        the main menu. It takes the touch-position as a argument and checks
        if the touch is on a button"""
        
        xpos = touch.x
        ypos = touch.y

        # checks if the highscore window is not open
        if(self.highscore_window.get_active() == False):
            # if the startbutton is pressed
            if(xpos >= 4* self.width//20 and
                xpos < 4* self.width//20 + 15*self.width // 20 and
                ypos >= 11 * self.height // 20 and 
                ypos < 11 * self.height // 20 + 3 * self.height // 20):
                    
                    # set the menu to false                
                    self._status = False
                    
            # if the highscore button is pressed
            if(xpos >= 4* self.width//20 and
                xpos < 4* self.width//20 + 15*self.width // 20 and
                ypos >= 6 * self.height // 20 and 
                ypos < 6 * self.height // 20 + 3 * self.height // 20):
                
                # set the highscore_window to active
                self.highscore_window.set_active(True)
                
        # if the highscore window is open, check for 
        # touches that want to quit the highscore window
        elif(self.highscore_window.get_active()): 
            if(xpos >= self.width//20 and
                xpos < 19*self.width//20 and
                ypos >= self.height//20 and
                ypos < 19*self.height//20):
                
                self.highscore_window.get_save()
                self.highscore_window.set_active(False)
    
    def set_status(self, status):
        self._status = status
    
    def get_status(self):
        return(self._status)
        
    def set_size(self, width, height):
        self.width = width
        self.height = height