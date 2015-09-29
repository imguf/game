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


class RootWidget(BoxLayout):
    
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        
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
        
        # creates the player object
        self.player = Player.Player(1,1, self.sq_w, self.sq_h, 
                                    self.board_size_x, self.board_size_y)
        
        self.player_movable = False
                                    
        
        # instansiate the Rocket_Controll class
        self.rocket_control = Rocket_Controll.Rocket_Controll(self.play_field_width, self.play_field_height,
                                                              self.board_size_x, self.board_size_y)

        self.rip = False       
        self.update_once = True


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
            Rectangle(source="img/background-temp.png", pos=(0,0), 
                      size=(self.play_field_widget.width, self.height))            
            
            
            # call the draw_grid function
            self.draw_grid(self.play_field_widget, self.board_size_x,self.board_size_y)
            
            # call the draw function of the player
            self.player.draw(self.play_field_widget, self.play_field_x, self.play_field_y,self.sq_w, self.sq_h)
            
            self.rocket_control.draw(self.play_field_widget, self.play_field_x, self.play_field_y, self.sq_w, self.sq_h)

            #Timerlabel
            Label(text=self.timer_text, pos=(self.play_field_width*0.01,self.play_field_height * 1.025))
            
            #Pausebutton
            Rectangle(source="img/pausebutton.png", pos=(self.play_field_width*1,self.play_field_height * 1.1), size=(self.sq_w*0.19, self.sq_h*0.19))

            #Deathscreen            
            if self.rip:
              Rectangle(source="img/ripscreen.png", pos=(self.play_field_x+0.5*self.sq_w, \
              self.play_field_y+self.sq_h), size=(self.sq_w*2, self.sq_h*3))
              Label(text=self.timer_text, font_size="20sp", pos=(self.play_field_x+self.sq_w*1, self.play_field_y+self.sq_h*1))
            
        
            
    
    def draw_grid(self, widget, x_size, y_size):
        """ this function draws out the grid and the lines surounding the playfield"""
        dynamic_y = self.play_field_height // 20
        dynamic_x = self.play_field_width // 20
        
        #draw the outside lines
        Rectangle(pos=(self.play_field_x,self.play_field_y*0.975), size=(self.play_field_width, self.play_field_width * 0.01))
        Rectangle(pos=(self.play_field_x,self.play_field_height *1.035), size=(self.play_field_width, self.play_field_height * 0.01))
        
        Rectangle(pos=(self.play_field_x,self.play_field_y), size=(self.play_field_width * 0.01, self.play_field_height * 0.985))
        Rectangle(pos=(self.play_field_width * 1.045,self.play_field_y), size=(self.play_field_width * 0.01,self.play_field_height * 0.985))
        
        
        
        # draw the grid
        for n in range(1,x_size):
            Rectangle(pos=(dynamic_x+ (self.play_field_width // x_size * n), self.play_field_y),\
                    size=(self.play_field_width * 0.01,self.play_field_height * 0.985))
        
        for n in range(1, y_size):
            Rectangle(pos=(self.play_field_x, dynamic_y+(self.play_field_height // y_size) * (n)),\
                    size=(self.play_field_width,self.play_field_height * 0.01))
          
    
                
    
    def check_collision(self):
        """ this function is used to check collision"""
        
        
        ##### Checks if the rockets and the player collides #####
        
        # get the players position
        player_x = self.player.get_x() * self.sq_w + 10 + self.play_field_x
        player_y = self.player.get_y() * self.sq_h + 10 + self.play_field_y
        
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
            if(rockets_x_xpos[n] * 1.1 +self.play_field_x >= player_x and 
               rockets_x_xpos[n] * 1.1 + self.play_field_x < player_x + self.sq_w * 0.925 - self.play_field_width * 0.01 and
               rockets_x_ypos[n] + 1.5 * self.play_field_y >= player_y and
               rockets_x_ypos[n] + 1.5 * self.play_field_y < player_y  + self.sq_h * 0.85 - self.play_field_height * 0.01):
                   self.death_screen()
            # check if the rockets upper right corner collides with the player
            elif(rockets_x_xpos[n] * 1.1 +self.play_field_x + self.sq_w * 0.7 >= player_x and 
               rockets_x_xpos[n] * 1.1 +self.play_field_x + self.sq_w * 0.7 < player_x + self.sq_w * 0.925 - self.play_field_width * 0.01 and
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
        if(self.timer > 0.05):
            self.player_movable = True
        
        if(self.paused == False):
            # call the fnk that updates the timer
            self.update_timer(dt)
            
            
            # update the the base variables, 
            # do not know why this is needed, but it is
            self.setup_base_variables()        
            
            
            # update the player image
            self.player.update_image(self.seconds)        
            
            # update the rocket_control class
            self.rocket_control.set_play_field_size(self.play_field_width, self.play_field_height)
            self.rocket_control.set_board_size(self.board_size_x, self.board_size_y)
            self.rocket_control.update(dt, self.seconds, self.sq_w, self.sq_h)
           
                
            # check collision function 
            self.check_collision()
            
            
            # when chosen amount of time has passed, grow the field
            if(float(self.seconds) % 30 == 0 and float(self.seconds) != 0 and self.update_once):
            
                # add one to the size in both x and y
                self.board_size_x += 1
                self.board_size_y += 1
                
                self.player.update_board_size(self.board_size_x, self.board_size_y)
                
                self.rocket_control.set_board_size(self.board_size_x, self.board_size_y)
                self.rocket_control.add_new_rockets()
            
            
                self.update_once = False
            
            if(float(self.seconds) % 30 != 0):
                self.update_once = True     
            
            # calls the main draw function        
            self.draw()
                    
    
    def on_touch_down(self, touch):
        """ gets the position of the first screen touch"""
        
        # if the player is alive
        if self.rip == False:
            if(self.paused and touch.y > self.play_field_height + 50 and touch.x > self.play_field_width-200):
                self.paused = False
            else:
                # if the touch is on the pausbutton, paus the game
                if(touch.y > self.play_field_height + 50 and touch.x > self.play_field_width-200):            
                    self.paused = True
              
                # if the touch is on the play_field
                # take the x and y position of the touch
                if(touch.y < self.play_field_height):
                    self.touch_down_x = touch.x
                    self.touch_down_y = touch.y
                  
           

        # if the player is dead          
        elif self.rip and touch.y < self.sq_h*3 and touch.y > self.play_field_y+self.sq_h \
        and touch.x < self.sq_w*2 and touch.x > self.play_field_x+0.5*self.sq_w:
          
          # restart rockets and player
          self.rocket_control.restart_rockets()
          self.player.restart_player()
          
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