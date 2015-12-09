import Rocket
import Indicator
from random import randint

class Rocket_Controll:
    """ This class controlls the rockets movement and actions"""
    
    def __init__(self, play_field_width, play_field_height, board_width, board_height):
        self.play_field_width = play_field_width
        self.play_field_height = play_field_height
        self.board_width = board_width
        self.board_height = board_height
        self.sq_w = 0
        self.sq_h = 0
        
        self.timer = 0
        
        self.rocket_spawn_time = 0.0
        self.rocket_spawn_delay = 0.0
        
        
        
        # creates the rockets
        self.rockets_x = [Rocket.Rocket(-400,2,1), Rocket.Rocket(-10000,1,1),
                          Rocket.Rocket(-10000,4,1), Rocket.Rocket(-10000,3,1)]
                          
        self.rockets_y = [Rocket.Rocket(0,-10000,3), Rocket.Rocket(2,-10000,3)]
        
        self.rockets_moving = False
        
        
        # holding the new ypos of the horizontal rockets
        self.rocket_x_ypos = [-1,-1,-1,-1]
        self.next_rocket_x = 0
        
        
        # creates the indicators in the x axis
        self.indicator_x = [Indicator.Indicator(-1,-1, 1, 3, 5),Indicator.Indicator(-1,-1, 1, 3, 5),
                            Indicator.Indicator(-1,-1, 1, 3, 5),Indicator.Indicator(-1,-1, 1, 3, 5)]
                            
                            
        # creates the indicators in the y axis
        self.indicator_y = [Indicator.Indicator(-1, -1, 3, 3, 5), Indicator.Indicator(-1, -1, 3, 3, 5)]
        
        self.rocket_y_xpos = [-1,-1]
        self.next_rocket_y = 0

        self.show_indicator = False
        self.rocket_ready = True
        
        
        self.update_once = True
        
        
    def draw(self, widget, play_field_x, play_field_y, sq_w, sq_h, is_paused):
        
        #draw the x rockets
        for n in range(len(self.rockets_x)):         
            self.rockets_x[n].draw(widget, play_field_x, play_field_y,self.sq_w, self.sq_h)
                
        # draw the y rockets
        for n in range(len(self.rockets_y)):
            self.rockets_y[n].draw(widget, play_field_x, play_field_y,self.sq_w, self.sq_h)

            
        # draw the indicators of the show_indicator is true
        if(self.show_indicator and self.rockets_moving == False and not is_paused):
            for n in range(len(self.indicator_x)):
                self.indicator_x[n].draw(widget, play_field_x, play_field_y,self.sq_w, self.sq_h)
            
            for n in range(len(self.indicator_y)):
                self.indicator_y[n].draw(widget, play_field_x, play_field_y,self.sq_w, self.sq_h)

        
    def control(self, dt):
        """this fnction controll the movements of the rockets"""
        
        
        # start the rockets movement firstly with the indicators
        if((self.rocket_spawn_delay == 1.5 or self.rocket_spawn_delay == 3.0) and self.rocket_ready):
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
                self.rockets_x[n].move(dt)
            
            for n in range(len(self.rockets_y)):
                self.rockets_y[n].move(dt)
                
        
        if(self.rocket_spawn_delay != 1.5 and self.rocket_spawn_delay != 3.0):
            self.rocket_ready = True
        
        
        
        
        
        
    def add_new_rockets(self):
            
        # gives the new bordersize to the indicators
        for n in range(len(self.indicator_x)):
            self.indicator_x[n].set_border_size(self.board_width, self.board_height)
        for n in range(len(self.indicator_y)):
            self.indicator_y[n].set_border_size(self.board_width, self.board_height)
        
        #create a new rocket
        self.rockets_x.append(Rocket.Rocket(self.play_field_width,self.board_height-1,1, 
                                            self.play_field_width, self.play_field_height, 
                                            self.rockets_x[0].get_update_round()))
        self.rockets_y.append(Rocket.Rocket(self.play_field_height, self.board_width-1,3,
                                            self.play_field_width, self.play_field_height,
                                            self.rockets_x[0].get_update_round()))
        
        # create a new indicatorss            
        self.indicator_x.append(Indicator.Indicator(self.board_width, self.board_height-1, 1, self.board_width, self.board_height))
        self.indicator_y.append(Indicator.Indicator(self.board_width-1, self.board_height, 3, self.board_width, self.board_height))            
        
        #             
        self.rocket_x_ypos.append(-1)
        self.rocket_y_xpos.append(-1)
        
        
        for n in range(len(self.rockets_x)):
            self.rockets_x[n].set_speed(self.board_height-5)
        for n in range(len(self.rockets_y)):
            self.rockets_y[n].set_speed(self.board_width-3)
               
    
    
    
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
                ypos = randint(0, self.board_height-1)
                  
                
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
                    
                    return ypos
                    
            # new xpos for rockets moving up and down
            elif(direc == 3 or direc == 4):
                
                xpos = randint(0, self.board_width-1)
                
                for n in self.rocket_y_xpos:
                    
                    #check if the new xpos collides with a allready used one
                    if(xpos == n):
                        clear_pos = 0
                        break
                    # if no, add 1 to clear_pos
                    else:
                        clear_pos += 1
                
                if(clear_pos == len(self.rocket_y_xpos)):
                    # if the new position does not interfere with another one
                    # return the xpos
                    self.rocket_y_xpos[self.next_rocket_y] = xpos
                    self.next_rocket_y += 1
                    check_clear_position = False

                    return xpos


    def check_inbounds(self):
        """ this function is used to check collision with different things"""        
        
        
        """ start of code that checks if the rockets are out of bounds"""        
        
        # check if the rockets are out of bounds 
        # if yes stop them from mobing and return them to a new starting position
        if(self.rockets_x[0].get_x() < self.sq_w * -2 or self.rockets_x[0].get_x() > self.sq_w * (self.board_width + 1)):
            print("\n\n\n")
            
            for n in range(len(self.rockets_x)):
            
                if(self.rockets_x[n].get_direc() == 2):
                    print("start X: " , self.rockets_x[n].get_start_x())
                    print("Current X: " , self.rockets_x[n].get_x())
                    print("Direc: ", self.rockets_x[n].get_direc())
                    print("left: " , self.sq_w * -2)
                    print("Right: " , self.sq_w * (self.board_width + 1))
                    print()
            
            self.rockets_moving = False
            self.rocket_spawn_time = 0.0
            self.rocket_spawn_delay = 0.0
            
            for n in range(len(self.rockets_x)):
                # gives a new direction
                new_direc = randint(1,2)
                
                # sets a new start_x position depening on direction
                if(new_direc == 1):    
                    self.rockets_x[n].set_direc(1)
                    self.rockets_x[n].set_start_x(self.sq_w * (self.board_width + 1))
                    self.rockets_x[n].set_x(self.sq_w * (self.board_width + 1))
                elif(new_direc == 2):
                    self.rockets_x[n].set_direc(2)
                    self.rockets_x[n].set_start_x(self.sq_w * -2)
                    self.rockets_x[n].set_x(self.sq_w * -2)
                    
                    
                


                # sets the new direction and sets the xpos to the new position
                #self.rockets_x[n].set_x(self.rockets_x[n].get_start_x())
                self.rockets_x[0].set_direc(1)
                self.rockets_x[0].set_x(self.sq_w * (self.board_width + 1))
                self.rockets_x[0].set_start_x(self.sq_w * (self.board_width + 1))

                """if(n == 0):
                    print("direc: ", new_direc)
                """
                
                
                    
                # set the new ypos by using the function new_rocket_position
                self.rockets_x[n].set_y(self.new_rocket_position(self.rockets_x[n].get_direc()))
                
                #gives the indicators a new position
                for m in range(len(self.indicator_x)):
                    self.indicator_x[m].set_new_pos(self.rockets_x[m].get_direc())
                    self.indicator_x[m].set_y(self.rockets_x[m].get_y())
                
            
            # resets the variables used in new_rocket_position so it can be used again
            for n in range(len(self.rocket_x_ypos)):
                self.rocket_x_ypos[n] = -1
            self.next_rocket_x = 0
            
            
            # gives the vertical rocekts a new x-position
            for n in range(len(self.rockets_y)):
                # gives a new direction
                new_direc = randint(3,4)
                
                # sets a new start_y position depening on direction
                if(new_direc == 3):    
                    self.rockets_y[n].set_start_y(self.play_field_height+2*self.sq_h)
                elif(new_direc == 4):
                    self.rockets_y[n].set_start_y(self.sq_h * -3)


                # sets the new direction and sets the ypos to the new position
                self.rockets_y[n].set_direc(new_direc)
                self.rockets_y[n].set_y(self.rockets_y[n].get_start_y())
                
                # set the new xpos by using the function new_rocket_position
                self.rockets_y[n].set_x(self.new_rocket_position(self.rockets_y[n].get_direc()))
                
                #gives the indicators a new position
                for n in range(len(self.indicator_y)):
                    self.indicator_y[n].set_new_pos(self.rockets_y[n].get_direc())
                    self.indicator_y[n].set_x(self.rockets_y[n].get_x())
                
            
            # resets the variables used in new_rocket_position so it can be used again
            for n in range(len(self.rocket_y_xpos)):
                self.rocket_y_xpos[n] = -1
            self.next_rocket_y = 0
    
        """ end of code that checks if the rockets are out of bounds and restarting the rockets"""
        
    def update(self, dt, timer, sq_w, sq_h):
        # update the timer and the squaresizes"
        self.timer = timer
        self.sq_w = sq_w
        self.sq_h = sq_h
        self.rocket_spawn_time += 1.0/60.0
        self.rocket_spawn_delay = float("%.1f" % self.rocket_spawn_time)
        #print(self.rocket_spawn_delay)

    
        # set up the rockets and indicators so they have the right starting position        
        if(float(timer) < 0.1 and self.update_once):   
            self.update_once = False
            # gives the x rockets a new position
            for n in range(len(self.rockets_x)):
                self.rockets_x[n].set_start_x(self.play_field_width)
                self.rockets_x[n].set_x(self.play_field_width)
                self.rockets_x[n].set_screen_size(self.play_field_width, self.play_field_height)
                
             #gives the x indicators a new position
            for n in range(len(self.indicator_x)):
                self.indicator_x[n].set_new_pos(self.rockets_x[n].get_direc())
                self.indicator_x[n].set_y(self.rockets_x[n].get_y())


            # gives the y rockets a new position
            for n in range(len(self.rockets_y)):
                self.rockets_y[n].set_start_y(self.play_field_height)
                self.rockets_y[n].set_y(self.play_field_height)
                self.rockets_y[n].set_screen_size(self.play_field_width, self.play_field_height)
                
             #gives the y indicators a new position
            for n in range(len(self.indicator_y)):
                self.indicator_y[n].set_new_pos(self.rockets_y[n].get_direc())
                self.indicator_y[n].set_x(self.rockets_y[n].get_x())    
                
                
        
        
        for n in range(len(self.rockets_x)):
            self.rockets_x[n].update_image(timer)
            
        for n in range(len(self.rockets_y)):
            self.rockets_y[n].update_image(timer)
        
        #call the control funktion
        self.control(dt)
    
        # call the check collision funktion
        self.check_inbounds()
    
    
    def restart_rockets(self):
        rockets_x_start_y = [1,2,3,4]
        rockets_y_start_x = [0,2]
        
        self.board_width = 3
        self.board_height = 5
        
        self.rocket_spawn_time = 0.0
        self.rocket_spawn_delay = 0.0
        
        for n in range(len(self.rockets_x)-1,3, -1):
            # delete all the elements in the list except the first 4
            del self.rockets_x[-1]
            del self.indicator_x[-1]
            del self.rocket_x_ypos[-1]
            
        for n in range(4):
            # set the rockets to their start value
            self.rockets_x[n].set_x(-400)
            self.rockets_x[n].set_y(rockets_x_start_y[n])
            self.rockets_x[n].set_start_y(rockets_x_start_y[n])
            self.rockets_x[n].set_direc(1)
            
            self.rockets_x[n].set_speed(self.board_height-5)
            
            self.rockets_x[n].set_update_round(0)

            
            # set the indicators to their start value
            self.indicator_x[n].set_border_size(self.board_width, self.board_height)
            self.indicator_x[n].set_new_pos(1)
            
            
            
        for n in range(len(self.rockets_y)-1,1,-1):
            # delete all the elements in the list except the first 2
            del self.rockets_y[-1]
            del self.indicator_y[-1]
            del self.rocket_y_xpos[-1]
            
        for n in range(2):
            # set the rockets to their start value
            self.rockets_y[n].set_x(rockets_y_start_x[n])
            self.rockets_y[n].set_start_x(rockets_y_start_x[n])
            self.rockets_y[n].set_y(-400)
            self.rockets_y[n].set_direc(3)
            self.rockets_y[n].set_speed(self.board_width-3)
            
            self.rockets_y[n].set_update_round(0)
            
            # set hte indidicators to their start value
            self.indicator_y[n].set_border_size(self.board_width, self.board_height)
            self.indicator_y[n].set_new_pos(3)
            
        
        # stop the rockets from moving
        self.rockets_moving = False
        self.update_once = True
        
        
    def set_play_field_size(self, w,h):
        """ sets the playfield width and height"""
        self.play_field_width = w
        self.play_field_height = h
        
    def set_board_size(self, w, h):
        """ sets the board size"""        
        self.board_width = w
        self.board_height = h
        
    def get_rockets_x(self):
        """ this function returns the x_positions of the rockets in a list"""
        xpos = []
        ypos = []        
        
        for n in range(len(self.rockets_x)):
            # add all the position values to two different lists
            xpos.append(self.rockets_x[n].get_x())
            ypos.append(self.rockets_x[n].get_y()* self.sq_h)
            
        return xpos, ypos, len(self.rockets_x)
        
    def get_rockets_y(self):
        """ Thid function returns the ypos of the rocekts in a list"""
        xpos = []
        ypos = []
        for n in range(len(self.rockets_y)):
            # add all the position values to two different lists
            xpos.append(self.rockets_y[n].get_x()*self.sq_w)           
            ypos.append(self.rockets_y[n].get_y())
            
        return xpos, ypos, len(self.rockets_y)
        
    def is_rockets_moving(self):
        """ this method returns the boolean value of the rockets, if they move or not"""
        return self.rockets_moving
        
    def reset_update_round(self):
        for n in range(len(self.rockets_x)):
            self.rockets_x[n].set_update_round(0)
    
        for n in range(len(self.rockets_y)):
            self.rockets_y[n].set_update_round(0)