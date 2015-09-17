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
                                    
        
        self.rockets_x = [Rocket.Rocket(-10000,2,1), Rocket.Rocket(-10000,0,1),
                          Rocket.Rocket(-10000,4,1), Rocket.Rocket(-10000,3,1)]
        self.rockets_y = [Rocket.Rocket(0,-10000,3), Rocket.Rocket(2,-10000,3)]
        
        self.rockets_moving = False
        
        
        # holding the new ypos of the horizontal rockets
        self.rocket_x_ypos = [-1,-1,-1,-1]
        self.next_rocket_x = 0
        
        self.indicator_x = [Indicator.Indicator(-1,-1, 1, 3, 5),Indicator.Indicator(-1,-1, 1, 3, 5),
                            Indicator.Indicator(-1,-1, 1, 3, 5),Indicator.Indicator(-1,-1, 1, 3, 5)]
                            
        self.indicator_y = [Indicator.Indicator(-1, -1, 3, 3, 5), Indicator.Indicator(-1, -1, 3, 3, 5)]
        
        self.rocket_y_xpos = [-1,-1]
        self.next_rocket_y = 0

        self.show_indicator = False
        self.rocket_ready = True
       
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
            # call the draw_grid function
            self.draw_grid(widget, self.board_size_x,self.board_size_y)
            
            # call the draw function of the player
            self.player.draw(widget, self.play_field_x, self.play_field_y,self.sq_w, self.sq_h)
            
            for n in range(len(self.rockets_x)):         
                self.rockets_x[n-1].draw(widget, self.play_field_x, self.play_field_y,self.sq_w, self.sq_h)
                
            for n in range(len(self.rockets_y)):
                self.rockets_y[n-1].draw(widget, self.play_field_x, self.play_field_y,self.sq_w, self.sq_h)

                
            if(self.show_indicator and self.rockets_moving == False):
                for n in range(len(self.indicator_x)):
                    self.indicator_x[n-1].draw(widget, self.play_field_x, self.play_field_y,self.sq_w, self.sq_h)
                
                for n in range(len(self.indicator_y)):
                    self.indicator_y[n-1].draw(widget, self.play_field_x, self.play_field_y,self.sq_w, self.sq_h)

            
            
            
    
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
            
           
    def rocket_control(self, dt):
        """this fnction controll the movements of the rockets"""
        
        
        # start the rockets movement firstly with the indicators
        if(float(self.seconds) % 0.5 == 0 and float(self.seconds) != 0.0 and self.rocket_ready):
            if(self.show_indicator):
                # make the rockets able to move
                self.rockets_moving = True
                # make the rocekts inable to spawn again
                self.rocket_ready = False
                # dissable the indicators
                self.show_indicator = False

            else:
                
                
                # show the indicators
                self.show_indicator = True
                # dissable the rockets
                self.rocket_ready = False
            
        # move the rockets
        if(self.rockets_moving):
            for n in range(len(self.rockets_x)):
                self.rockets_x[n-1].move(dt)
            
            for n in range(len(self.rockets_y)):
                self.rockets_y[n-1].move(dt)
        
        # make the rockets ready to spawn
        if(float(self.seconds) % 0.5 != 0):
            self.rocket_ready = True
        
        
        
        # when chosen amount of time has passed, grow the field
        if(float(self.seconds) % 30 == 0 and float(self.seconds) != 0 and self.update_once):
            
            # add one to the size in both x and y
            self.board_size_x += 1
            self.board_size_y += 1
            
            # gives the new bordersize to the indicators
            for n in range(len(self.indicator_x)):
                self.indicator_x[n-1].set_border_size(self.board_size_x, self.board_size_y)
            for n in range(len(self.indicator_y)):
                self.indicator_y[n-1].set_border_size(self.board_size_x, self.board_size_y)
            
            #create a new rocket
            self.rockets_x.append(Rocket.Rocket(self.play_field_width,self.board_size_y-1,1))
            self.rockets_y.append(Rocket.Rocket(self.play_field_height, self.board_size_x-1,3))
            
            # create a new indicatorss            
            self.indicator_x.append(Indicator.Indicator(self.board_size_x, self.board_size_y-1, 1, self.board_size_x, self.board_size_y))
            self.indicator_y.append(Indicator.Indicator(self.board_size_x-1, self.board_size_y, 3, self.board_size_x, self.board_size_y))            
            
            #             
            self.rocket_x_ypos.append(-1)
            self.rocket_y_xpos.append(-1)
            
            self.player.update_board_size(self.board_size_x, self.board_size_y)
            
            
            self.update_once = False
            print(len((self.rockets_x)))
            
        if(float(self.seconds) % 30 != 0):
            self.update_once = True
        

                
    def new_rocket_position(self, direc):
        """ This function returns a new position for the rockets and it makes
            sure that that position is not already taken by another rocket"""
            
        # creates a variable to controll the while loop and one to check so 
        # it loops the right amount of time
        check_clear_position = True  
        clear_pos = 0


        #starts the while loop
        while(check_clear_position):
            if(direc == 1 or direc == 2):
            
                #generate a new y position
                ypos = randint(0, self.board_size_y-1)
    
    
                print(self.rocket_x_ypos)
                  
                
                for n in self.rocket_x_ypos:
                    
                    #checks if the new ypos collides with a allready used one
                    if(ypos == n):
                        clear_pos = 0
                        break
                    #if no add 1 to clear_pos
                    else:
                        clear_pos += 1
                    
                # if the new position does not collide with another
                    # set that as the new position and return the value
                if(clear_pos == len(self.rocket_x_ypos)):
                    
                    self.rocket_x_ypos[self.next_rocket_x] = ypos
                    self.next_rocket_x += 1
                    check_clear_position = False
                    print(ypos)
                    return ypos
                    
            # new xpos for rockets moving up and down
            elif(direc == 3 or direc == 4):
                
                xpos = randint(0, self.board_size_x-1)
                
                for n in self.rocket_y_xpos:
                    
                    #check if the new xpos collides with a allready used one
                    if(xpos == n):
                        clear_pos = 0
                        break
                    # if no, add 1 to clear_pos
                    else:
                        clear_pos += 1
                
                if(clear_pos == len(self.rocket_y_xpos)):
                    
                    self.rocket_y_xpos[self.next_rocket_y] = xpos
                    self.next_rocket_y += 1
                    check_clear_position = False
                    print(xpos)
                    return xpos
                
    
    def check_collision(self):
        """ this function is used to check collision with different things"""        
        
        
        """ start of code that checks if the rockets are out of bounds"""        
        
        # check if the rockets are out of bounds 
        # if yes stop them from mobing and return them to a new starting position
        if(self.rockets_x[0].get_x() < -500 or self.rockets_x[0].get_x() > self.play_field_width+500):
            self.rockets_moving = False
            
            for n in range(len(self.rockets_x)):
                # gives a new direction
                new_direc = randint(1,2)
                
                # sets a new start_x position depening on direction
                if(new_direc == 1):    
                    self.rockets_x[n-1].set_start_x(self.play_field_width)
                elif(new_direc == 2):
                    self.rockets_x[n-1].set_start_x(self.sq_w * -2)


                # sets the new direction and sets the xpos to the new position
                self.rockets_x[n-1].set_direc(new_direc)
                self.rockets_x[n-1].set_x(self.rockets_x[n-1].get_start_x())
                
                # set the new ypos by using the function new_rocket_position
                self.rockets_x[n-1].set_y(self.new_rocket_position(self.rockets_x[n-1].get_direc()))
                
                #gives the indicators a new position
                for n in range(len(self.indicator_x)):
                    self.indicator_x[n-1].set_new_pos(self.rockets_x[n-1].get_direc())
                    self.indicator_x[n-1].set_y(self.rockets_x[n-1].get_y())
                
            
            # resets the variables used in new_rocket_position so it can be used again
            for n in range(len(self.rocket_x_ypos)):
                self.rocket_x_ypos[n-1] = -1
            self.next_rocket_x = 0
            
            
            # gives the vertical rocekts a new x-position
            for n in range(len(self.rockets_y)):
                # gives a new direction
                new_direc = randint(3,4)
                
                # sets a new start_y position depening on direction
                if(new_direc == 3):    
                    self.rockets_y[n-1].set_start_y(self.play_field_height)
                elif(new_direc == 4):
                    self.rockets_y[n-1].set_start_y(self.sq_h * -2)


                # sets the new direction and sets the ypos to the new position
                self.rockets_y[n-1].set_direc(new_direc)
                self.rockets_y[n-1].set_y(self.rockets_y[n-1].get_start_y())
                
                # set the new xpos by using the function new_rocket_position
                self.rockets_y[n-1].set_x(self.new_rocket_position(self.rockets_y[n-1].get_direc()))
                
                #gives the indicators a new position
                for n in range(len(self.indicator_y)):
                    self.indicator_y[n-1].set_new_pos(self.rockets_y[n-1].get_direc())
                    self.indicator_y[n-1].set_x(self.rockets_y[n-1].get_x())
                
            
            # resets the variables used in new_rocket_position so it can be used again
            for n in range(len(self.rocket_y_xpos)):
                self.rocket_y_xpos[n-1] = -1
            self.next_rocket_y = 0
    
        """ end of code that checks if the rockets are out of bounds"""
        
            
           
            
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
            
            if(float(self.timer) < 0.1):   
                
                # gives the x rockets a new position
                for n in range(len(self.rockets_x)):
                    self.rockets_x[n-1].set_start_x(self.play_field_width)
                    self.rockets_x[n-1].set_x(self.play_field_width)
                    
                 #gives the x indicators a new position
                for n in range(len(self.indicator_x)):
                    self.indicator_x[n-1].set_new_pos(self.rockets_x[n-1].get_direc())
                    self.indicator_x[n-1].set_y(self.rockets_x[n-1].get_y())
    
    
                # gives the y rockets a new position
                for n in range(len(self.rockets_y)):
                    self.rockets_y[n-1].set_start_y(self.play_field_height)
                    self.rockets_y[n-1].set_y(self.play_field_height)
                    
                 #gives the y indicators a new position
                for n in range(len(self.indicator_y)):
                    self.indicator_y[n-1].set_new_pos(self.rockets_y[n-1].get_direc())
                    self.indicator_y[n-1].set_x(self.rockets_y[n-1].get_x())    
    
            self.player.update_image(self.seconds)        
            
            #rocket controller
            self.rocket_control(dt)
    
            # check collision function 
            self.check_collision()
                
            
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