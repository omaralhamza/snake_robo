#!/usr/bin/env python3
import rclpy # One if the Dependencies that needs to also be added to the package.xml file

from rclpy.node import Node

from builtin_interfaces.msg import Duration
from std_msgs.msg import Float64MultiArray # One if the Dependencies that needs to also be added to the package.xml file
from sensor_msgs.msg import JointState
import math
import numpy as np

timer_timer = 0
k_d = 0.001 
k_p = 0.01
#j_angle_ta = np.empty(9,dtype=float) # Global variable that's used inside the sine-wave generating function


FeedBack = np.empty(9,dtype=float)   #Global variable that contains the effort value of the feedback from the /Joint_states topic
Vel_FeedBack = np.empty(9,dtype=float)
set_point = np.empty(9,dtype=float)  #Global variable that contains the setpoint I want the robot to follow, this will be equaled with
U_Value = np.empty(9,dtype=float)
Velocity = np.empty(9,dtype=float)
Acceleration = np.empty(9,dtype=float)


def phi_angle_generator_at_t(timer):
      #  global j_angle_ta
        
        N = 10
        a = 23.6                   # Alpha value of the equation
        w = 0.872665 *0.46            # Freq_w of the equation of the angle
        d = 0.698132                        # Delta, which is the value of the phase shift in the equation of the angle
        phi0 = 0                             # Offset angle
        
        temp_JA = np.empty(9,dtype=float)
        temp_JA_d = np.empty(9,dtype=float)
        temp_JA_dd = np.empty(9,dtype=float)
        temp_huge_arr = np.array([])
        for i in range(0,N - 1):
           
        	

            
               # phi0 = np.deg2rad(0)
              #  temp_JA[i] = ( a * np.sin(w * timer + i * d) + phi0)
               # temp_JA_d[i] = ( a * w * np.cos(w * timer + i * d))
               # temp_JA_dd[i] = ( -1 * a * w ** 2 * np.sin(w * timer + i * d))
  
            #elif 50 <= timer <= 70:
             #   phi0 = np.deg2rad(0)
              #  temp_JA[i] = ( a * np.sin(w * timer + i * d) + phi0)
             #   temp_JA_d[i] = ( a * w * np.cos(w * timer + i * d))
              #  temp_JA_dd[i] = ( -1 * a * w ** 2 * np.sin(w * timer + i * d))
           # else:
                phi0 = 0
                temp_JA[i] = ( a * np.sin(w * timer + i * d) + phi0)
                temp_JA_d[i] = ( a * w * np.cos(w * timer + i * d))
                temp_JA_dd[i] = ( -1 * a * w ** 2 * np.sin(w * timer + i * d))
                
                #print (temp_JA)
             
        temp_huge_arr= np.array([ temp_JA, temp_JA_d, temp_JA_dd])   
            #j_angle_ta[i] = temp_JA[i]


        return temp_huge_arr


class 	EffortPublisher(Node): # The Publisher class is created, which inherits from (or is a subclass of) Node

    def __init__(self):                                       # Following is the definition of the class’s constructor 
        super().__init__('effort_Pub')                        # super().__init__ calls the Node class’s constructor and gives it your node name, in this case effort_Pub
                                                              # The super() function is used to give access to methods and properties of a parent or sibling class
        
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.Effort_publisher = self.create_publisher(Float64MultiArray,"/effort_controllers/commands", 10)
        
        
        self.subscription = self.create_subscription(
            JointState,
            'joint_states',
            self.PID_callback,
            10)
        self.subscription


    def PID_callback(self, msg): #j_angle_ta is the refrence value we want the joint to follow, the msg data is the feedback coming from the joint_states topic
       
       global timer_timer 
       global k_p
       global k_d 
     
       
       #local_timer += 1 
       
       #if local_timer == timer_timer:
       #j_angle_ta = phi_angle_generator_at_t(local_timer) 
       
       feedback_temp = np.empty(9,dtype=float)
       velocity_temp = np.empty(9,dtype=float)   
       for i in range(0,9):
    	  
            #msg.position[i] ---- msg.velocity[i] ----  msg.effort[i]
            
             feedback_temp[i] = msg.effort[i] # u_bar is the  PID control value       
             velocity_temp[i] = msg.velocity[i]
             
             FeedBack[i] = feedback_temp[i]
             Vel_FeedBack[i] = velocity_temp[i]
       
       #print(u_temp)  
      # timer_timer = timer_timer + 1
        
      # if timer_timer >60: 
      #    timer_timer = 0




    
    
    
    def timer_callback(self):
        
        global timer_timer
        global k_d
        global U_Value 
        #values_temp = j_angle_ta
        set_point, Velocity , Acceleration  = phi_angle_generator_at_t(timer_timer)
        
        for i in range(0,9):
           U_Value[i] = (Acceleration[i] + k_d * ( set_point[i] - FeedBack[i] ) + k_p * (Velocity[i] - Vel_FeedBack[i]))
        # creating an array of values to be sent to the joints
        
        
        
        
        value1 = U_Value[8] 
                                                 #[1.5708,0.0,0.0,0.0,-1.5708,0.0,0.0,0.0,1.5708]
        value2 = U_Value[7] 
       
        value3 = U_Value[6] 
       
        value4 = U_Value[5]
       
        value5 = U_Value[4]
        
        value6 = U_Value[3]
        
        value7 = U_Value[2]
        
        value8 = U_Value[1]
        
        value9 = U_Value[0]
        
        msg = Float64MultiArray()
        msg.data = [value9,value8,value7,value6,value5,value4,value3,value2,value1]
        
        self.Effort_publisher.publish(msg)
        print(set_point)
        
        timer_timer = timer_timer + 1
        
        if timer_timer >1000: 
        	timer_timer = 0
        	
      	
        
        

def main(args=None):
     
    rclpy.init(args=args)
    effort_Pub = EffortPublisher()

    rclpy.spin(effort_Pub)
    
    effort_Pub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
