# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 13:40:15 2015

@author: Admin
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import *
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window
from math import atan
from random import randint
from math import degrees
from kivy.uix.image import AsyncImage 
import Player
import Rocket_Controll
import Main_menu
import Background


class RootWidget(BoxLayout):
    
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        
        self.hi_score = [0,0,0,0,0,0,0,0,0,0]

        self.get_save()
       

        # sets the window size
        """window_height = 960
        window_width = 540
        Window.size = (window_width,window_height)"""
        
        
        # creates the base layout of the screen
        layout = BoxLayout(orientation="vertical")
        
        
        #creates the main widget that is used to draw stuff on
        self.play_field_widget = Widget()              
                
        # adds the play_field_widget to the layout
        layout.add_widget(self.play_field_widget)        
        
        # add the layout to the window
        self.add_widget(layout)
        
        # create a boolean to hold the state of the game, pauses or unpaused
        self.paused = False
        
        # creates the variables that holds the amount of squares of the playfield
        self.board_size_x = 3
        self.board_size_y = 5
        
        # variable to hold the maximum size of the board
        self.max_board_size_x = 6
        self.max_board_size_y = 8         
        
        # creates the base varuables 
        self.setup_base_variables()
        
        
        
        # creates the timer value
        self.timer = 0.0
        
        self.seconds = 0
        self.minutes = 0
        
        self.timer_text = ""
        
        # creates the variables used for calculating the user input
        self.touch_down_x = 0
        self.touch_down_y = 0
        self.angle = 0   
        
        # main menu object
        self.menu = Main_menu.Main_menu(True)
        
        # creates the player object
        self.player = Player.Player(1,0, self.sq_w, self.sq_h, 
                                    self.board_size_x, self.board_size_y)
        
        self.player_movable = False
                                    
        
        # instansiate the Rocket_Controll class
        self.rocket_control = Rocket_Controll.Rocket_Controll(self.play_field_width, self.play_field_height,
                                                              self.board_size_x, self.board_size_y)

        self.rip = False       
        self.update_once = True
        self.grow_field = False
        
        # background stuff
        self.background = Background.Backgrounds(["img/background/background1.jpg","img/background/background2.jpg",\
                                            "img/background/background1.jpg","img/background/background2.jpg"],\
                                            self.width, self.height)
        
                                            
                                            
                                            

    def set_save(self):
        print(self.hi_score)
        highscore = float("%.1f" % self.timer)
        for num in range(10):
            if float(highscore) > float(self.hi_score[num]):
                
                for n in range(9, num, -1):
                    self.hi_score[n], self.hi_score[n-1] = self.hi_score[n-1], self.hi_score[n]
                
                self.hi_score[num] = highscore

                
                break
        print(self.hi_score)

        try:
            file = open("./save.txt", "w")
        except:
            print("Wrong when saving to file.")
        else:
            for n in self.hi_score:
                file.write(str(n) + "\n")
                
                
            file.close() 
            
    def get_save(self):
        try:        
            file = open("./save.txt", "r")
        except:
            print("Wrong when opening file.")
        else:
            n = 0
            for line in file:
                self.hi_score[n] = float(line)
                n += 1
                
            file.close()
            
            
    def setup_base_variables(self):
        """ this function creates some basic variables"""
        self.play_field_x = self.play_field_widget.width * 0.05
        self.play_field_y =self.play_field_widget.height * 0.05
        self.play_field_width = self.play_field_widget.width - self.play_field_x * 2
        self.play_field_height = self.play_field_widget.height - self.play_field_y * 1.7
        
        
        self.sq_w = self.play_field_width // self.board_size_x
        self.sq_h = self.play_field_height // self.board_size_y
        
        
                
    def draw(self):
        """ this function controlls the drawing"""
        # clears the canvas
        self.play_field_widget.canvas.clear()
        

        # starts the drawings
        with self.play_field_widget.canvas:
            # draw a background
            self.background.draw()
            
            # if the menu is true, print it out and not the game
            if(self.menu.get_status()):
                self.menu.draw(self.play_field_widget, self.play_field_width,\
                               self.play_field_height)
            else:   
                # if the menu is false, print the game out                
                
                # call the draw_grid function
                self.draw_grid(self.play_field_widget, self.board_size_x,self.board_size_y)
    
                # call the draw functon of the rocket_controll class            
                self.rocket_control.draw(self.play_field_widget, self.play_field_x, self.play_field_y, self.sq_w, self.sq_h)            
                
                # call the draw function of the player
                self.player.draw(self.play_field_widget, self.play_field_x, self.play_field_y,self.sq_w, self.sq_h)
                
    
                
                
                #Pausebutton
                Rectangle(source="img/pausebutton.png", pos=(self.play_field_width*0.99,self.play_field_height * 1.05), size=(self.sq_w*0.2, self.sq_w*0.2))
    
                #Deathscreen            
                if self.rip:
                    self.draw_death_screen()
                  
                  #Label(text=self.timer_text, font_size="20sp", pos=(self.play_field_x+self.sq_w*1, self.play_field_y+self.sq_h*1))
                
            #Timer    
            #Label(text=self.timer_text, pos=(self.play_field_width*0.15,self.play_field_height * 1.05), text_size=(200, 100))

    
    
    def draw_death_screen(self):
        number_images = ["img/numbers/zero.png",
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
        
        
        # gets the highest score
        highscore = self.get_highest_score()
                          
        # draw out the deathscreen
        Rectangle(source="img/ripscreen.png", pos=(self.play_field_x+0.5*self.sq_w, \
                  self.play_field_y+(self.sq_h*0.5)), size=(self.sq_w*(self.board_size_x-1), self.sq_h*(self.board_size_y-1)))
                  
        # gets the indexes of the correct imgaes that are going to draw out the time
        index_list = self.get_image_index(str(self.timer))
        
        # draw out the time on screen
        for m in range(len(index_list)):
            Rectangle(source=(number_images[index_list[m]]), pos=(4*self.play_field_width//20 + 0.5 * m*self.play_field_width//20,\
                                self.play_field_height//20 + self.play_field_height//40), size=(self.play_field_width//50,self.play_field_width//50))

        
        
        # gets the indexes of the correct imgaes that are going to draw out the time
        index_list = self.get_image_index(str(highscore))
        
        # draw out the highest score on screen
        for m in range(len(index_list)):
            Rectangle(source=(number_images[index_list[m]]), pos=(4*self.play_field_width//20 + 0.5 * m*self.play_field_width//20,\
                                self.play_field_height//20 * 2 + self.play_field_height//40), size=(self.play_field_width//50,self.play_field_width//50))
                  
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
                  
    def get_highest_score(self):
        try:        
            file = open("./save.txt", "r")
        except:
            print("Wrong when opening file.")
        else:
            for line in file:
                highscore = float(line)
                break

            file.close
            
            return highscore

    
    def draw_grid(self, widget, x_size, y_size):
        """ this function draws out the grid and the lines surounding the playfield"""
        dynamic_y = self.play_field_height // 20
        dynamic_x = self.play_field_width // 20
        
        # change the color of the lines
        Color(255/255, 255/255, 168/255, 75/255)
        
        #draw the outside lines
        Rectangle(pos=(self.play_field_x,self.play_field_y*0.975), size=(self.play_field_width, self.play_field_width * 0.01))
        Rectangle(pos=(self.play_field_x,self.play_field_height *1.035), size=(self.play_field_width, self.play_field_height * 0.01))
        
        Rectangle(pos=(self.play_field_x,self.play_field_y), size=(self.play_field_width * 0.01, self.play_field_height * 0.985))
        Rectangle(pos=(self.play_field_width * 1.045,self.play_field_y), size=(self.play_field_width * 0.01,self.play_field_height * 0.985))
        
        
        
        """# draw the grid
        for n in range(1,x_size):
            Rectangle(pos=(dynamic_x+ (self.play_field_width // x_size * n), self.play_field_y),\
                    size=(self.play_field_width * 0.01,self.play_field_height * 0.985))
        
        for n in range(1, y_size):
            Rectangle(pos=(self.play_field_x, dynamic_y+(self.play_field_height // y_size) * (n)),\
                    size=(self.play_field_width,self.play_field_height * 0.01))
          
        """
        
        # set the color back to white to prevent color bugs
        Color(1,1,1)
    
    def check_collision(self):
        """ this function is used to check collision"""
        
        
        ##### Checks if the rockets and the player collides #####
        
        # get the players position
        player_x = self.player.get_x() * self.sq_w + 1.25 * self.play_field_x
        player_y = self.player.get_y() * self.sq_h + 1.35 * self.play_field_y
        
        #get the horizontal rockets position
        rockets_x_xpos = self.rocket_control.get_rockets_x()[0]
        rockets_x_ypos = self.rocket_control.get_rockets_x()[1] 
        rockets_x_len = self.rocket_control.get_rockets_x()[2]
        
        # get the vertical rockets position
        rockets_y_xpos = self.rocket_control.get_rockets_y()[0]
        rockets_y_ypos = self.rocket_control.get_rockets_y()[1]
        rockets_y_len = self.rocket_control.get_rockets_y()[2]
        
        
        # check if the horizontal rockets collide with the player
        for n in range(rockets_x_len):
            
            # check if the rockets lower left corner collides with player
            if(rockets_x_xpos[n] * 1.15 + self.play_field_x >= player_x and 
               rockets_x_xpos[n] * 1.15 + self.play_field_x < player_x + self.sq_w * 0.925 - self.play_field_width * 0.01 and
               rockets_x_ypos[n] + 1.5 * self.play_field_y >= player_y and
               rockets_x_ypos[n] + 1.5 * self.play_field_y < player_y  + self.sq_h * 0.85 - self.play_field_height * 0.01):
                   self.death_screen()
            # check if the rockets upper right corner collides with the player
            elif(rockets_x_xpos[n] * 1.15 +self.play_field_x + self.sq_w * 0.6 >= player_x and 
               rockets_x_xpos[n] * 1.15 +self.play_field_x + self.sq_w * 0.7 < player_x + self.sq_w * 0.925 - self.play_field_width * 0.01 and
               rockets_x_ypos[n] + 1.5 * self.play_field_y + self.sq_h * 0.7 >= player_y and
               rockets_x_ypos[n] + 1.5 * self.play_field_y + self.sq_h * 0.7 < player_y  + self.sq_h * 0.85 - self.play_field_height * 0.01):
                   self.death_screen()
        
        
        # check if the vertical rockets collide with the player
        for n in range(rockets_y_len):
            
            #check if the rocekts lower left corner collides with the player
            if(rockets_y_xpos[n] + 2 * self.play_field_x >= player_x and 
                rockets_y_xpos[n] + 2 * self.play_field_x < player_x + self.sq_w * 0.925 - self.play_field_width * 0.01 and
                rockets_y_ypos[n] * 1.1 + self.play_field_y >= player_y and
                rockets_y_ypos[n] * 1.1 + self.play_field_y < player_y  + self.sq_h * 0.85 - self.play_field_height * 0.01):
                    self.death_screen()
                    
            # check if the rocekts upper right corner collides with the player
            elif(rockets_y_xpos[n] + 2 * self.play_field_x + self.sq_w * 0.7 >= player_x and 
                rockets_y_xpos[n] + 2 * self.play_field_x + self.sq_w * 0.7 < player_x + self.sq_w * 0.925 - self.play_field_width * 0.01 and
                rockets_y_ypos[n] * 1.1 + self.play_field_y + self.sq_h * 0.7 >= player_y and
                rockets_y_ypos[n] * 1.1 + self.play_field_y + self.sq_h * 0.7 < player_y + self.sq_h * 0.85 - self.play_field_height * 0.01):
                    self.death_screen()
            
    def death_screen(self):
      """Describes what happens when you lose."""
      self.paused = True
      self.rip = True
      self.set_save()
        


    
    def update_timer(self, dt):
        #update the timer and print out the new time on screen
        self.timer += 1.0/60.0
        self.seconds = 0
        self.minutes = 0

        # if the timer is more than 60 seconds, add a minute 
        if self.timer > 60:
            self.minutes = int(self.timer // 60)
            self.seconds = self.timer % 60
        
        # else add only seconds
        else:
            self.seconds = self.timer
          
        #round the seconds to one decimal
        self.seconds = "%.1f" % self.seconds
        
        #update the timer on screen
        self.timer_text = (str(self.minutes) +":"+ self.seconds)

    
    def update(self, dt):
        """ this function is the controller of everything
        everything piece of code that is going to be run more than once goes 
        through here"""
        
        # update the the base variables, 
        # do not know why this is needed, but it is
        self.setup_base_variables()        

        self.background.set_screen_size(self.width, self.height)

        if(self.menu.get_status()):
            self.menu.set_size(self.play_field_width, self.play_field_height)
            
            # calls the draw funcetion to draw 
            self.draw()
        
        else:
            # if the game            
            
            
            if(self.timer > 0.05):
                self.player_movable = True            
            
            if(self.paused == False):
                # call the fnk that updates the timer
                self.update_timer(dt)
                
                # calls the background.move method so the backgrounds move down
                self.background.move(dt)            

                
                
                # update the player image
                self.player.update_image(self.seconds)        
                
                # update the rocket_control class
                self.rocket_control.set_play_field_size(self.play_field_width, self.play_field_height)
                self.rocket_control.set_board_size(self.board_size_x, self.board_size_y)
                self.rocket_control.update(dt, self.seconds, self.sq_w, self.sq_h)
               
                    
                # check collision function 
                self.check_collision()
                
                if(float(self.seconds) % 30 == 0 and float(self.seconds) != 0 and self.update_once):
                    self.grow_field = True
                
                # when chosen amount of time has passed, grow the field
                if( self.grow_field and self.update_once 
                    and self.rocket_control.is_rockets_moving() == False
                    and self.board_size_x < self.max_board_size_x
                    and self.board_size_y < self.max_board_size_y):
                
                    # add one to the size in both x and y
                    self.board_size_x += 1
                    self.board_size_y += 1
                    
                    self.player.update_board_size(self.board_size_x, self.board_size_y)
                    
                    self.rocket_control.set_board_size(self.board_size_x, self.board_size_y)
                    self.rocket_control.add_new_rockets()
                
                
                    self.update_once = False
                    self.grow_field = False
                
                if(float(self.seconds) % 30 != 0):
                    self.update_once = True 
                    
                
                # calls the main draw function        
                self.draw()
                
                
                    
    
    def on_touch_down(self, touch):
        """ gets the position of the first screen touch"""
        
        # if the menu is on, call the touch_down method of the menu object
        if(self.menu.get_status()):
            self.menu.touch_down(touch)
        else: # if the menu is not on, the game is on
            # if the player is alive
            if self.rip == False:
                if(self.paused and touch.y > self.play_field_height * 0.985 and touch.x > self.play_field_width * 0.95):
                    self.paused = False
                else:
                    # if the touch is on the pausbutton, paus the game
                    if(touch.y > self.play_field_height * 0.985 and touch.x > self.play_field_width * 0.95):            
                        self.paused = True
                  
                    # if the touch is on the play_field
                    # take the x and y position of the touch
                    if(touch.y < self.play_field_height):
                        self.touch_down_x = touch.x
                        self.touch_down_y = touch.y
                      
               
    
            # if the player is dead          
            elif( self.rip and 
                touch.y < self.sq_h*3 and 
                touch.y > self.play_field_y+self.sq_h and 
                touch.x < self.sq_w*2 and 
                touch.x > self.play_field_x+0.5*self.sq_w):
              
              # restart rockets and player
              self.rocket_control.restart_rockets()
              self.player.restart_player()
              self.background.reset_bg()
              
              # resets the board_size
              self.board_size_x = 3
              self.board_size_y = 5
              
              #set timer to 0
              self.timer = 0.0
              
              #unables the player to move
              self.player_movable = False
              
              #unpause
              self.paused = False        
              #make the player alive
              self.rip = False
          

    def on_touch_up(self, touch):
         """ gets the position of the point where the usesr pulls upp the finger"""        
         
         if(self.menu.get_status()):
             pass
         else:
             if(self.paused == False and self.player_movable == True):      
                if(touch.y < self.play_field_height):
                    x = touch.x - self.touch_down_x
                    y = touch.y - self.touch_down_y
                    
                    # checks so the y/x != 0 and takes out the angle between the two positions
                    try:
                        self.angle = degrees(atan(y/x))
                    except ZeroDivisionError:
                        print("Dividera med 0, nedslag och uppslagsplats densamma")
                    
                    # checks which "square" of the screen the touch is in and corrects the 
                    # angle to the correct one
                    if(x > 0 and y < 0):
                        self.angle = 360 - self.angle * -1
                    elif(x < 0 and y > 0):
                        self.angle = 180 - self.angle * -1
                    elif(x < 0 and y < 0):
                        self.angle = self.angle + 180
                
                    # moves the player in the right direction 
                    if(self.angle < 45 or self.angle > 315):
                        self.player.move_right(1) # move right
                        
                    elif(self.angle > 135 and self.angle < 225):
                        self.player.move_right(-1) # move left
                        
                    elif(self.angle > 45 and self.angle < 135):
                        self.player.move_up(1) # move up
                        
                    elif(self.angle > 225 and self.angle < 315):
                        self.player.move_up(-1) # move down
            
        

class TestApp(App):
    
    def build(self):
        game = RootWidget()
        
        # calling the game.update function 60 times a second        
        Clock.schedule_interval(game.update, 1.0 / 60.0)

        return game


if __name__ == '__main__':
    TestApp().run()