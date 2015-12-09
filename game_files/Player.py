from kivy.graphics import *


class Player:
    """ This is the player class"""
    
    def __init__(self, xpos, ypos, size_x, size_y, board_width, board_height):
        # sets the position of the player        
        self.xpos = xpos
        self.ypos = ypos
        self.image = ["img/mainrocket/testing/1_png.png", "img/mainrocket/testing/2_png.png", "img/mainrocket/testing/3_png.png", "img/mainrocket/testing/4_png.png"]
        self.image_move_right = ["img/mainrocket/right/1right.png",
                                 "img/mainrocket/right/2right.png",
                                 "img/mainrocket/right/3right.png",
                                 "img/mainrocket/right/4right.png"]
                                 
        self.image_move_left = ["img/mainrocket/left/1right.png",
                                 "img/mainrocket/left/2right.png",
                                 "img/mainrocket/left/3right.png",
                                 "img/mainrocket/left/4right.png"]
                                 
        self.current_image = ""
        self.num = -1
        self.board_width = board_width
        self.board_height = board_height
        self.value_for_image = True
        # these are not used right now
        self.size_x = size_x
        self.size_y = size_y
        self.update_round = 0
        
        
    def update_image(self, function):
        if(float(function) // 0.1 != self.update_round):
            self.value_for_image = True
        if float(function) // 0.1 == self.update_round and self.value_for_image == True:
            self.update_round += 1
            self.num += 1
            if self.num == (len(self.image)):
                self.num = 0
                self.value_for_image = False
        self.current_image = self.image[self.num]
        
        print("sutffsfasfasf")
    
    def update_image_move_right(self, function):
        if(float(function) // 0.1 != self.update_round):
            self.value_for_image = True
        if float(function) // 0.1 == self.update_round and self.value_for_image == True:
            self.update_round += 1
            self.num += 1
            if self.num == (len(self.image_move_right)):
                self.num = 0
                self.value_for_image = False
        self.current_image = self.image_move_right[self.num]
        
    def update_image_move_left(self, function):
        if(float(function) // 0.1 != self.update_round):
            self.value_for_image = True
        if float(function) // 0.1 == self.update_round and self.value_for_image == True:
            self.update_round += 1
            self.num += 1
            if self.num == (len(self.image_move_left)):
                self.num = 0
                self.value_for_image = False
        self.current_image = self.image_move_left[self.num]
        
    def draw(self, widget, window_x, window_y, sq_w, sq_h):
        """ draw out the player"""
        Color(1.,1.,1.)        
        
        
        Rectangle(source =self.current_image,\
                pos=( 1.25 * window_x + sq_w * self.xpos, 1.35 * window_y + sq_h * self.ypos),\
                size=(sq_w * 0.925 - widget.width * 0.01, sq_h* 0.85 - widget.height * 0.01))
                

        
    def move_up(self, direc, dt):
        """ move the player up or down"""
        
        self.ypos += direc * dt * 7
        
    def move_right(self, direc, dt):
        """ move the player left or right"""
        self.xpos += direc * dt * 5

    def set_x(self, xpos):
        """ sets the xpos variable"""
        self.xpos = xpos
        
    def set_y(self, ypos):
        """ sets the ypos variable"""
        self.ypos = ypos

    def get_x(self):
        """ returns the xpos variable"""
        return self.xpos
            
    def get_y(self):
        """ returns the ypos variable"""
        return self.ypos
        
        
    def restart_player(self):
        """ restart the players position"""
        self.xpos = 1
        self.ypos = 0
        self.board_width = 3
        self.board_height = 5
        self.update_round = 0
        
    def reset_update_round(self):
        self.update_round = 0
    
    def update_board_size(self, x, y):
        """ takes two arguments and sets the board width and height to the values"""
        self.board_width = x
        self.board_height = y