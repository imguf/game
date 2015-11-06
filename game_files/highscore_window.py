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
                
        
        Rectangle(source=(self.number_images[0]), pos=(100, 50*1), size=(16,16))
        Rectangle(source=(self.number_images[0]), pos=(100, 50*2), size=(16,16))
        Rectangle(source=(self.number_images[0]), pos=(100, 50*3), size=(16,16))
        Rectangle(source=(self.number_images[0]), pos=(100, 50*4), size=(16,16))
        Rectangle(source=(self.number_images[0]), pos=(100, 50*5), size=(16,16))
        Rectangle(source=(self.number_images[0]), pos=(100, 50*6), size=(16,16))
        Rectangle(source=(self.number_images[0]), pos=(100, 50*7), size=(16,16))
        Rectangle(source=(self.number_images[0]), pos=(100, 50*8), size=(16,16))
        Rectangle(source=(self.number_images[0]), pos=(100, 50*9), size=(16,16))
        Rectangle(source=(self.number_images[0]), pos=(100, 50*10), size=(16,16))
        
    
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