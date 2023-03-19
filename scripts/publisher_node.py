#!/usr/bin/env python3
import rclpy

from rclpy.node import Node

from builtin_interfaces.msg import Duration
from std_msgs.msg import Float64MultiArray 
import math
import numpy as np

timer_timer = 0
j_angle_ta = np.empty(9,dtype=float)

def phi_angle_generator_at_t(timer):
        global j_angle_ta
        
        N = 10
        a = 0.8                              # Alpha value of the equation
        w = 0.872665                         # Freq_w of the equation of the angle
        d = 0.698132                         # Delta, which is the value of the phase shift in the equation of the angle
        phi0 = 0                             # Offset angle
        
        temp_JA = np.empty(9,dtype=float)
        
        #print(timer_timer)
        
        for i in range(0,N - 1):
           
        	
            if 20 <= timer <= 30:
                phi0 = np.deg2rad(5)
                temp_JA[i] = ( a * np.sin(w * timer + i * d) + phi0)
  
            elif 50 <= timer <= 60:
                phi0 = np.deg2rad(-10)
                temp_JA[i] = ( a * np.sin(w * timer + i * d) + phi0)

            else:
                phi0 = 0
                temp_JA[i] = ( a * np.sin(w * timer + i * d) + phi0)
                print (temp_JA)
             
         
            j_angle_ta[i] = temp_JA[i]


        return j_angle_ta


class 	PositionPublisher(Node):

    def __init__(self):
        super().__init__('position_Pub')
        
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.Position_publisher = self.create_publisher(Float64MultiArray,"/joints_position_controllers/commands", 10)


    def timer_callback(self):
        
        global timer_timer
        
        values_temp = phi_angle_generator_at_t(timer_timer) 
        # creating an array of values to be sent to the joints
        
        
        
        value1 = values_temp[0]
                                                 #[1.5708,0.0,0.0,0.0,-1.5708,0.0,0.0,0.0,1.5708]
        value2 = values_temp[1]
       
        value3 = values_temp[2]
       
        value4 = values_temp[3]
       
        value5 = values_temp[4]
        value6 = values_temp[5]
        value7 = values_temp[6]
        value8 = values_temp[7]
        value9 = values_temp[8]
        
        msg = Float64MultiArray()
        msg.data = [value1,value2,value3,value4,value5,value6,value7,value8,value9]
        
        self.Position_publisher.publish(msg)
        
        timer_timer = timer_timer + 1
        
        if timer_timer >60: 
        	timer_timer = 0
        	
      	
        
        

def main(args=None):
     
    rclpy.init(args=args)
    position_Pub = PositionPublisher()

    rclpy.spin(position_Pub)
    
    position_Pub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
