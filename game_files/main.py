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
        upper_layout = BoxLayout(orientation="horizontal", size_hint=(1,0.02))        
        
        
        self.timer_label = Label(text=("kakor"),pos=(0, upper_layout.top))
        self.empty_label = Label()
        self.paus_label = Label(text=("paus, temp"))
        
        #creates the main widget that is used to draw stuff on
        self.play_field_widget = Widget()              
        
        upper_layout.add_widget(self.timer_label)        
        upper_layout.add_widget(self.empty_label)        
        upper_layout.add_widget(AsyncImage(source ="img/pause.png", size_hint= (1, 2), pos_hint={'center_x':.5, 'center_y':-.5}))           
        
        layout.add_widget(upper_layout)        
        
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
        
        # creates the variables used for calculating the user input
        self.touch_down_x = 0
        self.touch_down_y = 0
        self.angle = 0        
        
        # creates the player object
        self.player = Player.Player(1,1, self.sq_w, self.sq_h, 
                                    self.board_size_x, self.board_size_y)
                                    
        
        # instansiate the Rocket_Controll class
        self.rocket_control = Rocket_Controll.Rocket_Controll(self.play_field_width, self.play_field_height,
                                                              self.board_size_x, self.board_size_y)
       
       
        self.update_once = True


    def setup_base_variables(self):
        """ this function creates some basic variables"""
        self.play_field_x = self.play_field_widget.x + 30
        self.play_field_y = self.play_field_widget.y + 40
        self.play_field_width = self.play_field_widget.right - 75
        self.play_field_height = self.play_field_widget.top - 80
        
        
        self.sq_w = self.play_field_width // self.board_size_x
        self.sq_h = self.play_field_height // self.board_size_y
        
        
                
    def draw(self, widget):
        """ this function controlls the drawing"""
        # clears the canvas
        self.play_field_widget.canvas.clear()
        

        # starts the drawings
        with widget.canvas:
            # draw a background
            Rectangle(source="img/background-temp.png", pos=(0,0), 
                      size=(self.play_field_widget.width, self.height))            
            
            # call the draw_grid function
            self.draw_grid(widget, self.board_size_x,self.board_size_y)
            
            # call the draw function of the player
            self.player.draw(widget, self.play_field_x, self.play_field_y,self.sq_w, self.sq_h)
            
            self.rocket_control.draw(widget, self.play_field_x, self.play_field_y)
            
            
            
            
    
    def draw_grid(self, widget, x_size, y_size):
        """ this function draws out the grid and the lines surounding the playfield"""
        
        #draw the outside lines
        Rectangle(pos=(self.play_field_x,self.play_field_y), size=(self.play_field_width,10))
        Rectangle(pos=(self.play_field_x,self.play_field_height+40), size=(self.play_field_width+10,10))
        Rectangle(pos=(self.play_field_x,self.play_field_y), size=(10,self.play_field_height))
        Rectangle(pos=(self.play_field_width+30,self.play_field_y), size=(10,self.play_field_height))
        
        
        # draw the grid
        for n in range(1,x_size):
            Rectangle(pos=(30 + (self.play_field_width // x_size * n), self.play_field_y), size=(10,self.play_field_height))
        for n in range(1, y_size):
            Rectangle(pos=(self.play_field_x, 40+(self.play_field_height // y_size) * (n)), size=(self.play_field_width,10))
            
    
                
    
    def check_collision(self):
        """ this function is used to check collision"""
        
        # calls the rocket controls check_collision funktion
        self.rocket_control.check_collision()
            
           
            
    def update_timer(self):
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
        self.timer_label.text = (str(self.minutes) +":"+ self.seconds)
        

    
    def update(self, dt):
        """ this function is the controller of everything
        everything piece of code that is going to be run more than once goes 
        through here"""
        
        
        
        if(self.paused == False):
            # call the fnk that updates the timer
            self.update_timer()
            
            
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
                
                self.rocket_control.add_new_rockets()
            
            
                self.update_once = False
            
            if(float(self.seconds) % 30 != 0):
                self.update_once = True     
            
            # calls the main draw function        
            self.draw(self.play_field_widget)
                    
    
    def on_touch_down(self, touch):
        """ gets the position of the first screen touch"""
        
        
            
        if(self.paused and touch.y > self.play_field_height + 50 and touch.x > self.play_field_width-200):
            self.paused = False
        else:
            if(touch.y > self.play_field_height + 50 and touch.x > self.play_field_width-200):            
                self.paused = True
            
            
            if(touch.y < self.play_field_height):
                self.touch_down_x = touch.x
                self.touch_down_y = touch.y
        
    def on_touch_up(self, touch):
        """ gets the position of the point where the usesr pulls upp the finger"""        
        if(self.paused == False):      
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