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
import Player
import Rocket
import Indicator


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
        upper_layout.add_widget(self.paus_label)           
        
        layout.add_widget(upper_layout)        
        
        # adds the play_field_widget to the layout
        layout.add_widget(self.play_field_widget)        
        
        # add the layout to the window
        self.add_widget(layout)
        
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
        
        rockets_rand_pos =[randint(0,self.board_size_x-1),
                           randint(0,self.board_size_y-1),
                            randint(0,self.board_size_y-1),
                            randint(0,self.board_size_y-1),
                            randint(0,self.board_size_x-1),
                            randint(0,self.board_size_y-1),
                            randint(0,self.board_size_y-1),
                            randint(0,self.board_size_y-1)]
        
        # creates the rocket objects in a list
        self.rockets = [Rocket.Rocket(rockets_rand_pos[0],self.play_field_height,3),
                        Rocket.Rocket(self.play_field_width,rockets_rand_pos[1],1),
                        Rocket.Rocket(self.play_field_width,rockets_rand_pos[2],1),
                        Rocket.Rocket(self.play_field_width,rockets_rand_pos[3],1),
                        Rocket.Rocket(rockets_rand_pos[4],self.play_field_height,3),
                        Rocket.Rocket(self.play_field_width,rockets_rand_pos[5],1),
                        Rocket.Rocket(self.play_field_width,rockets_rand_pos[6],1),
                        Rocket.Rocket(self.play_field_width,rockets_rand_pos[7],1)]
                        
        self.moving_rockets = [False, False, False, False,
                               False, False, False, False]
        self.next_rocket_ready = True
        self.wich_rocket = 0
        
                
        # creates the indicator objects in a list
        self.indicators = [Indicator.Indicator(rockets_rand_pos[0],self.board_size_y,3, self.board_size_x, self.board_size_y),
                           Indicator.Indicator(self.board_size_x,rockets_rand_pos[1],1, self.board_size_x, self.board_size_y),
                           Indicator.Indicator(self.board_size_x,rockets_rand_pos[2],1, self.board_size_x, self.board_size_y),
                           Indicator.Indicator(self.board_size_x,rockets_rand_pos[3],1, self.board_size_x, self.board_size_y),
                           Indicator.Indicator(rockets_rand_pos[4],self.board_size_y,3, self.board_size_x, self.board_size_y),
                           Indicator.Indicator(self.board_size_x,rockets_rand_pos[5],1, self.board_size_x, self.board_size_y),
                           Indicator.Indicator(self.board_size_x,rockets_rand_pos[6],1, self.board_size_x, self.board_size_y),
                           Indicator.Indicator(self.board_size_x,rockets_rand_pos[7],1, self.board_size_x, self.board_size_y)]
                           
        self.draw_indicators = [False,False,False,False,
                                False,False,False,False]
                                
        # variables which controlls the border growth and the growth in speed
        self.rocket_time = 1.0
        self.rocket_time_lowest = 0.5
        self.upgrade_time_size = 15.0
        
        self.upgrade_ready_size = True


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
            # call the draw_grid function
            self.draw_grid(widget, self.board_size_x,self.board_size_y)
            
            # call the draw function of the player
            self.player.draw(widget, self.play_field_x, self.play_field_y,self.sq_w, self.sq_h)
            
            # call the draw function of the rocket
            for n in range(len(self.rockets)):
                self.rockets[n].draw(widget, self.play_field_x, self.play_field_y,self.sq_w, self.sq_h)
                
                if(self.draw_indicators[n]):
                    self.indicators[n].draw(widget, self.play_field_x, self.play_field_y,self.sq_w, self.sq_h)
            
            
    
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
                   
    def set_rocket_start_position(self,n, direc):
        """ this function updates the rockets startingpositions
        and the position of the indicators"""
        if(direc == 1):
            self.rockets[n].set_x(self.play_field_width)
            self.indicators[n].set_x(self.board_size_x)
        elif(direc == 2):
            self.rockets[n].set_x(self.play_field_x - 350)
            self.indicators[n].set_x(-1)
        elif(direc == 3):
            self.rockets[n].set_y(self.play_field_height)
            self.indicators[n].set_y(self.board_size_y)
        elif(direc == 4):
            self.rockets[n].set_y(self.play_field_y-350)
            self.indicators[n].set_y(-1)
            
    def check_collision(self):
        """ this function is used to check collision with different things"""        
        
        
        for n in range(len(self.rockets)):
            
            #checks if the rockets goes outside of the playfield
            # for the horizontal rockets
            if(self.rockets[n].get_x() < self.play_field_x - 400 or
               self.rockets[n].get_x() > self.play_field_width):
                
                # generates a new direction for the rockets
                new_direc = randint(1,4)
                
                if(new_direc == 1):                    
                    self.set_rocket_start_position(n,1)
                elif(new_direc == 2):
                    self.set_rocket_start_position(n, 2)
                elif(new_direc == 3):
                    self.set_rocket_start_position(n, 3)
                elif(new_direc == 4):
                    self.set_rocket_start_position(n, 4)

                self.rockets[n].set_direc(new_direc)
                
                # sets the new y position and stops the rocket from moving
                new_y = randint(0,self.board_size_y-1)                
                self.indicators[n].set_y(new_y)
                self.rockets[n].set_y(new_y)
                self.moving_rockets[n] = False
            
            #for the vertical rockets
            elif(self.rockets[n].get_y() > self.play_field_height or
                self.rockets[n].get_y() < self.play_field_y - 400):
                
                # generates a new direction for the rocket
                new_direc = randint(1,4)
                    
                # set the new starting position depending on wich direction
                if(new_direc == 1):                    
                    self.set_rocket_start_position(n,1)
                elif(new_direc == 2):
                    self.set_rocket_start_position(n, 2)
                elif(new_direc == 3):
                    self.set_rocket_start_position(n,3)
                elif(new_direc == 4):
                    self.set_rocket_start_position(n,4)
                    
                # set the new direction
                self.rockets[n].set_direc(new_direc)
                
                #set the new x position and stops the rocket from moving
                new_x = randint(0,self.board_size_x-1)
                self.indicators[n].set_x(new_x)
                self.rockets[n].set_x(new_x)
                self.moving_rockets[n] = False
            
    def update_timer(self):
        #update the timer and print out the new time on screen
        self.timer += 1.0/60.0
        self.seconds = 0
        self.minutes = 0

        if self.timer > 60:
          self.minutes = int(self.timer // 60)
          self.seconds = self.timer % 60
        else:
          self.seconds = self.timer
          
        self.seconds = "%.1f" % self.seconds
        self.timer_label.text = (str(self.minutes) +":"+ self.seconds)
        
    def rocket_controll(self, dt):
        
        
        
        """ this function controlls the rockets and their movement"""
        #sets the correct startpossition for the rockets
        if(self.timer < 1):
            for n in range(len(self.rockets)):
                if(self.rockets[n].get_direc() == 1):
                    self.set_rocket_start_position(n,1)
                elif(self.rockets[n].get_direc == 2):
                    self.set_rocket_start_position(n,2)
                elif(self.rockets[n].get_direc() == 3):
                    self.set_rocket_start_position(n,3)
                elif(self.rockets[n].get_direc == 4):
                    self.set_rocket_start_position(n,4)
        

        
        # every 1 seconds start a new rocket
        if((float(self.seconds))% self.rocket_time == 0.0 and float(self.seconds) != 0.0 and self.next_rocket_ready):
            for n in range(len(self.rockets)):
                if(self.draw_indicators[n]):
                    self.moving_rockets[n] = True
                    self.draw_indicators[n] = False
            
            self.draw_indicators[self.wich_rocket] = True
            
            # dissable so the next rocket does not come directly
            self.next_rocket_ready = False
            print("next rocket not ready")
           
            self.wich_rocket += 1
            if(self.wich_rocket == len(self.rockets)):
                self.wich_rocket = 0
        
        # Enable the next rocket
        if(float(self.seconds) % self.rocket_time != 0.0):
            self.next_rocket_ready = True
            
        # moves all the rockets that are supposed to move
        for n in range(len(self.rockets)):
            if(self.moving_rockets[n]):
                self.rockets[n].move(dt)
                
                
        

    
    def update(self, dt):
        """ this function is the controller of everything
        everything piece of code that is going to be run more than once goes 
        through here"""
        
        # call the fnk that updates the timer
        self.update_timer()
        
        # update the the base variables, 
        # do not know why this is needed, but it is
        self.setup_base_variables()
        
        # call the rocket controll fnk
        self.rocket_controll(dt)
        
        # check collision function 
        self.check_collision()
            
        
        # calls the main draw function        
        self.draw(self.play_field_widget)
        
    
    def on_touch_down(self, touch):
        """ gets the position of the first screen touch"""
        
        if(touch.y < self.play_field_height):
            self.touch_down_x = touch.x
            self.touch_down_y = touch.y
        
    def on_touch_up(self, touch):
        """ gets the position of the point where the usesr pulls upp the finger"""        
        if(touch.y < self.play_field_height):
            x = touch.x - self.touch_down_x
            y = touch.y - self.touch_down_y
            
            # checks so the y/x != 0 and takes out the angle between the two positions
            try:
                self.angle = degrees(atan(y/x))
            except ZeroDivisionError:
                print("Dividera med 0, nedskag ich uptagningsplats densamma")
            
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