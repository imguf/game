from kivy.graphics import *


class Rocket:
    """ This is the Rocket-class"""
    def __init__(self, xpos, ypos, direc, play_field_width = 0, play_field_height = 0):
        self.xpos = xpos
        self.ypos = ypos
        self.start_x = xpos
        self.start_y = ypos
        self.play_field_width = play_field_width
        self.play_field_height = play_field_height
        self.speed = [75,85,95,105]
        self.which_speed = 0
        self.max_speed = 1000
        
        self.direc = direc
        
        self.which_image = -1
        self.able_to_change_image = True
        self.current_image = ""
        self.update_round = 0
        
        self.right_rockets_images = ["img/enemyrockets/right/enemyrocketv1fire.gif",\
                                     "img/enemyrockets/right/enemyrocketv1fire2.gif",\
                                     "img/enemyrockets/right/enemyrocketv1fire3.gif",\
                                     "img/enemyrockets/right/enemyrocketv1fire4.gif"]
                                     
        self.left_rockets_images = ["img/enemyrockets/left/enemyrocketv1fire.gif",\
                                     "img/enemyrockets/left/enemyrocketv1fire2.gif",\
                                     "img/enemyrockets/left/enemyrocketv1fire3.gif",\
                                     "img/enemyrockets/left/enemyrocketv1fire4.gif"]
                                     
        self.up_rockets_images = ["img/enemyrockets/up/enemyrocketv1fire.gif",\
                                     "img/enemyrockets/up/enemyrocketv1fire2.gif",\
                                     "img/enemyrockets/up/enemyrocketv1fire3.gif",\
                                     "img/enemyrockets/up/enemyrocketv1fire4.gif"]
                                     
        self.down_rockets_images = ["img/enemyrockets/down/enemyrocketv1fire.gif",\
                                     "img/enemyrockets/down/enemyrocketv1fire2.gif",\
                                     "img/enemyrockets/down/enemyrocketv1fire3.gif",\
                                     "img/enemyrockets/down/enemyrocketv1fire4.gif"]
        
    def draw(self, widget, window_x, window_y, sq_w, sq_h):
        """ draws the rocket"""
        Color(1.,1.0,1.0)        
        
        if(self.direc == 1):
            Rectangle(source=self.current_image, pos=(window_x + self.xpos * 1.1, window_y * 1.5 + self.ypos * sq_h),\
                      size=(sq_w *0.7, sq_h *0.7))
        elif self.direc == 2:
            Rectangle(source=self.current_image, pos=(window_x + self.xpos * 1.1, window_y * 1.5 + self.ypos * sq_h),\
                      size=(sq_w *0.7, sq_h *0.7))
        elif(self.direc == 3):
            Rectangle(source=self.current_image, pos=(2 *window_x + self.xpos * sq_w, window_y + self.ypos * 1.1),\
                      size=(sq_w * 0.7, sq_h * 0.7))
        elif self.direc == 4:
            Rectangle(source=self.current_image, pos=(2 *window_x + self.xpos * sq_w, window_y + self.ypos * 1.1),\
                      size=(sq_w * 0.7, sq_h * 0.7))
    
    def update_image(self, seconds):
        """ this method updates the current image of the rockets"""
        
        if(float(seconds) // 0.1 != self.update_round):
            self.able_to_change_image = True
        
        # if the timer is dividable by 0.05
        if(float(seconds) //  0.1 == self.update_round and self.able_to_change_image == True):
            
            # add one to the round and image
            self.update_round += 1
            self.which_image += 1
            
            # if the image number is higher then the highest index
            # put it to 0
            if(self.which_image == len(self.right_rockets_images)):
                self.which_image = 0
            
            # make the image change only work once
            self.able_to_change_image = False
        
        # update tbe image to the correct image chosen by the directon
        if(self.direc == 1):
            self.current_image = self.right_rockets_images[self.which_image]
        if(self.direc == 2):
            self.current_image = self.left_rockets_images[self.which_image]
        if(self.direc == 3):
            self.current_image = self.up_rockets_images[self.which_image]
        if(self.direc == 4):
            self.current_image = self.down_rockets_images[self.which_image]
    
    def move(self, dt):
        """ moves the rocket depending on the direction"""
        if(self.direc == 1):
            self.xpos -= self.speed[self.which_speed] * dt * (self.play_field_width/100)
        elif(self.direc == 2):
            self.xpos += self.speed[self.which_speed] * dt * (self.play_field_width/100)
        elif(self.direc == 3):
            self.ypos -= self.speed[self.which_speed] * dt * (self.play_field_height/100)
        elif(self.direc == 4):
            self.ypos += self.speed[self.which_speed] * dt * (self.play_field_height/100)
        
    def get_x(self):
        """ return the xpos"""
        return self.xpos
    
    def get_y(self):
        """ return the ypos"""
        return self.ypos
        
    def get_direc(self):
        """ returns the direction of the rocket"""
        return self.direc
        
    def get_start_x(self):
        """ returns the start x position"""
        return self.start_x
        
    def get_start_y(self):
        """ returns the start y position"""
        return self.start_y
    

    def set_start_x(self, xpos):
        """ sets the start x position"""
        self.start_x = xpos
        
    def set_start_y(self, ypos):
        """ sets the start y position"""
        self.start_y = ypos
    
    def set_direc(self, direc):
        """ sets the new direction"""
        self.direc = direc
        
    def set_x(self, xpos):
        """ set the xpos"""
        self.xpos = xpos
        
    def set_y(self, ypos): 
        """ set the ypos"""
        self.ypos = ypos
        
    def set_update_round(self, update_round):
        self.update_round = update_round
        
        
    def set_screen_size(self, w,h):
        """ gives teh rocket the correct screensize"""
        self.play_field_width = w
        self.play_field_height = h
        
        
    def set_speed(self, speed):
        self.which_speed = speed




        
        