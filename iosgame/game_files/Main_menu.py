from kivy.graphics import *

import highscore_window


class Main_menu:
    """ this class describes how the main menu works"""    
    
    def __init__(self, status):
        self._status = status        
        self.highscore_window = highscore_window.Highscore_window()
        
    def draw(self, widget, width, height):
                
        
        
        if(self.highscore_window.get_active() == False):
            # title image
            Rectangle(source="img/startmeny/superdodgerocketlogo.png", pos=(self.width//20,12 * self.height//20),\
                  size=(self.width,self.height - 11 * self.height //20))
        
            # start game button
            Rectangle(source="img/startmeny/startbtn.png", pos=(4* self.width//20, 6 * self.height//20),\
                      size=(15*self.width // 20, 2.5* self.height //20))
                      
            # Highscore button
            Rectangle(source="img/startmeny/hiscorebtn.png", pos=(4 * width//20, 2 * height//20),\
                      size=(15*width // 20, 2.5*height//20))
            
            
            """ # dont draw the option button for the moment because it doesn't do a thing
            # options game button
            Rectangle(source="img/startmeny/optionsbtn.png", pos=(4* width//20, 1 * height//20), \
                      size=(15*width // 20, 2.5 * height //20))
            """
                  
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
                ypos >= 6 * self.height // 20 and 
                ypos < 6 * self.height // 20 + 2.5 * self.height // 20):
                    
                    # set the menu to false                
                    self._status = False
                    
            # if the highscore button is pressed
            if(xpos >= 4* self.width//20 and
                xpos < 4* self.width//20 + 15*self.width // 20 and
                ypos >= 2 * self.height // 20 and 
                ypos < 2 * self.height // 20 + 2.5 * self.height // 20):
                
                self.highscore_window.get_save()

                # set the highscore_window to active
                self.highscore_window.set_active(True)
                
        # if the highscore window is open, 
        elif(self.highscore_window.get_active()): 
        
            #check for touches that want to quit the highscore window
            if(xpos >= 19*self.width//20 and
                xpos < 21*self.width//20 and
                ypos >= 19*self.height/20 and
                ypos < 19*self.height//20 + 2*self.width//20):
                
                self.highscore_window.set_active(False)
                
            # check for touches that wants to restet the highscore
            if(xpos >= 14*self.width//20 and
                xpos < 21*self.width//20 and
                ypos >= 1*self.height//20 and
                ypos < 1*self.height//20 + 3*self.width//20):
                    print("reset highscore")
                    self.highscore_window.reset_save()
        
        
    
    def set_status(self, status):
        self._status = status
    
    def get_status(self):
        return(self._status)
        
    def set_size(self, width, height):
        self.width = width
        self.height = height