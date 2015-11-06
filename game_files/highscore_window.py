from kivy.graphics import *


class Highscore_window:
    """ this class describes how the highscore window 
        will look like and function"""
    
    def __init__(self):
        """ constructor takes the width and height of the
            screen and sets the values to the arguments"""
       
        
        self._active = False
        
        # create highscore list
        self.highscore = [0,0,0,0,0,0,0,0,0,0]
        
        
    def draw(self, widget, width, height):
        """ this method draws out the window on the screen"""
        Rectangle(source=(""), pos=(width//20, height//20),\
                size=(19*width//20, 19*height//20))
    

    def get_save(self):
        try:        
            file = open("./save.txt", "r")
        except:
            print("Wrong when opening file.")
        else:
            n = 0
            for line in file:
                self.highscore[n] = float(line)
                n += 1
                
            file.close()
    
    def set_active(self, active):
        """ this method takes a boolean as an arguments
            it then sets the variable _active to that value"""
        self._active = active
        
    def get_active(self):
        """ this method returns the value of _active"""
        return self._active