from kivy.graphics import *
from kivy.uix.label import Label



class Highscore_window:
    """ this class describes how the highscore window 
        will look like and function"""
    
    def __init__(self):
        """ constructor takes the width and height of the
            screen and sets the values to the arguments"""
       
        
        self._active = False
        
        # create highscore list
        self.highscore = [0,0,0,0,0,0,0,0,0,0]
        
        self.number_images = ["img/test numbers/one.png"]
        self.highscore_label_list = []
        
        
    def draw(self, widget, width, height):
        """ this method draws out the window on the screen"""
        Color(1,1,1)
        Rectangle(source=(""), pos=(width//20, height//20),\
                size=(20*width//20, 20*height//20))
                
        # prints out a temporary layout of the highscore list
        for n in range(10):
            Rectangle(source=(self.number_images[0]), pos=(2*width//20, height//20*(n*2+1) + height//40), size=(width//50,width//50))

        
    
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