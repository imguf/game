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
        
        self.number_images = ["img/numbers/zero.png",
                              "img/numbers/one.png",
                              "img/numbers/two.png",
                              "img/numbers/three.png",
                              "img/numbers/four.png",
                              "img/numbers/five.png",
                              "img/numbers/six.png",
                              "img/numbers/seven.png",
                              "img/numbers/eight.png",
                              "img/numbers/nine.png",
                              "img/numbers/colon.png",
                              "img/numbers/dot.png"]
        self.highscore_label_list = []
        
        
    def draw(self, widget, width, height):
        """ this method draws out the window on the screen"""
        Color(1,1,1)
        
                
        # Reset highscore button
        Rectangle(source=("img/startmeny/reset_btn.png"), pos=(16*width//20, 1*height//20), size=(5*width//20, 2*height//20))
        
                
        Color(0,0,0)

        # exit highscore window button
        Rectangle(source=(""), pos=(18*width//20, 19*height//20), size=(2*width//20, height//20))
        

        Color(1,1,1)

        # prints the highscore list
        for n in range(10):
            if(n == 0):
                Rectangle(source=(self.number_images[1]), pos=(1.5*width//20, height//20*(n*2+1) + height//40), size=(width//50,width//50))
                Rectangle(source=(self.number_images[0]), pos=(2*width//20, height//20*(n*2+1) + height//40), size=(width//50,width//50))
            else:
                Rectangle(source=(self.number_images[10-n]), pos=(2*width//20, height//20*(n*2+1) + height//40), size=(width//50,width//50))
            
            Rectangle(source=(self.number_images[10]), pos=(2.5*width//20, height//20*(n*2+1) + height//40), size=(width//50,width//50))
            
            # gets which index of the images that are going to be printed out
            index_list = self.get_image_index(str(self.highscore[n]))
            
            # print out the time on the screen
            for m in range(len(index_list)):
                Rectangle(source=(self.number_images[index_list[m]]), pos=(4*width//20 + 0.5 * m*width//20, height//20*((9-n)*2+1) + height//40), size=(width//50,width//50))
                
            
    def get_image_index(self, time):
        """ this method takes a string as an argument 
            and returns the index of the images that is 
            going to be used"""
        
        seconds = 0.0
        minutes = 0
        
        # if the timer is more than 60 seconds, add a minute 
        if float(time) > 60:
            minutes = int(float(time) // 60)
            seconds = float(time) % 60
        
        # else add only seconds
        else:
            seconds = float(time)
          
        #round the seconds to one decimal
        seconds = "%.1f" % seconds
        
        time = str(minutes) + ":" + str(seconds)
        
        index_list = []
        
        for n in time:
            if(n == ":"):
                index_list.append(10)
            elif(n == "."):
                index_list.append(11)
            else:
                index_list.append(int(n))
        
        return index_list
        
    
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
            
            
            
    def reset_save(self):

        try:
            file = open("./save.txt", "w")
        except:
            print("Wrong when saving to file.")
        else:
            for n in self.highscore:
                file.write("0" + "\n")
            
            self.highscore = [0,0,0,0,0,0,0,0,0,0]
                
            file.close() 
            
    
    def set_active(self, active):
        """ this method takes a boolean as an arguments
            it then sets the variable _active to that value"""
        self._active = active
        
    def get_active(self):
        """ this method returns the value of _active"""
        return self._active