#!/usr/bin/env python3
import rclpy # One if the Dependencies that needs to also be added to the package.xml file

from rclpy.node import Node

from builtin_interfaces.msg import Duration
from std_msgs.msg import Float64MultiArray, String # One if the Dependencies that needs to also be added to the package.xml file
from sensor_msgs.msg import JointState
import math
import numpy as np



#j_angle_ta = np.empty(9,dtype=float) # Global variable that's used inside the sine-wave generating function


FeedBack = np.empty(9,dtype=float)   #Global variable that contains the effort value of the feedback from the /Joint_states topic
Vel_FeedBack = np.empty(9,dtype=float)
set_point = np.empty(9,dtype=float)  #Global variable that contains the setpoint I want the robot to follow, this will be equaled with
U_Value = np.empty(9,dtype=float)
Velocity = np.empty(9,dtype=float)
Acceleration = np.empty(9,dtype=float)





class 	EffortPublisher(Node): # The Publisher class is created, which inherits from (or is a subclass of) Node

    def __init__(self):                                       # Following is the definition of the class’s constructor 
        super().__init__('effort_Pub')                        # super().__init__ calls the Node class’s constructor and gives it your node name, in this case effort_Pub
                                                              # The super() function is used to give access to methods and properties of a parent or sibling class
        self.get_logger().set_level(rclpy.logging.LoggingSeverity.DEBUG)
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.Effort_publisher = self.create_publisher(Float64MultiArray,"/effort_controllers/commands", 10)
        self.subscription = self.create_subscription(JointState, 'joint_states', self.PID_callback, 10)
        self.params       = self.create_subscription(String, 'snake_robot_params', self.paramters_from_ui, 10)

        self.subscription
        self.timer_timer = 0 
        self.default_kp = 0.7
        self.default_kd = 0.01        
        #self.default_kp = 0.01 seems to be working without friction applied in ros2 control
        #self.default_kd = 0.01 seems to be working without friction applied in ros2 control
        #self.default_kp = 0.0001 working values
        #self.default_kd = 0.0001
        self.default_a = 72
        #self.default_a = 70 seems to be working without friction applied in ros2 control
        #self.default_a = 67.5 working values with ros2_control gazebo friction mu1 0.1 and mu2=1
        #self.default_w = 0.61  working values 
        self.default_w = 0.45
        self.default_d = 0.698132
        self.default_phi0 = 0
        self.default_phi1 = 0
        #self.default_w = 0.55 seems to be working without friction applied in ros2 control
        self.k_d = self.default_kp
        self.k_p = self.default_kd 
        self.var_a = self.default_a
        self.var_w = self.default_w
        self.var_d = self.default_d
        self.var_phi0 = self.default_phi0
        self.var_phi1 = self.default_phi1

    def paramters_from_ui(self, params):
        param_string = params.data.split(',')
        self.get_logger().debug(f'variable {param_string[0]} value {param_string[1]}')
        self.k_p = float(param_string[1]) if param_string[0] == 'k_p' else self.k_p # Update K_p
        self.k_d = float(param_string[1]) if param_string[0] == 'k_d' else self.k_d  # Update K_d
        self.var_a = float(param_string[1]) if param_string[0] == 'a' else self.var_a # Update a
        self.var_w = float(param_string[1]) if param_string[0] == 'w' else self.var_w # Update w
        self.var_d = float(param_string[1]) if param_string[0] == 'd' else self.var_d # Update d
        self.var_phi0 = float(param_string[1]) if param_string[0] == 'phi0' else self.var_phi0 # Update phi0
        self.var_phi1 = float(param_string[1]) if param_string[0] == 'phi1' else self.var_phi1 # Update phi1



    def PID_callback(self, msg): #j_angle_ta is the refrence value we want the joint to follow, the msg data is the feedback coming from the joint_states topic
       

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


    def phi_angle_generator_at_t(self, timer):
        #  global j_angle_ta
        
        N = 10
        a = self.var_a                            # Alpha value of the equation
        w = self.var_w                   # Freq_w of the equation of the angle
        d = self.var_d                       # Delta, which is the value of the phase shift in the equation of the angle 0.698132 
        phi0 = self.var_phi0                 # Offset angle in positive dir
        phi1 = self.var_phi1                 # Offset angle in negative dir
        
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
                
                temp_JA[i] = ( a * np.sin(w * timer + i * d) + phi0 - phi1)
                temp_JA_d[i] = ( a * w * np.cos(w * timer + i * d))
                temp_JA_dd[i] = ( -1 * a * w ** 2 * np.sin(w * timer + i * d))
                
                #print (temp_JA)
                
        temp_huge_arr= np.array([ temp_JA, temp_JA_d, temp_JA_dd])   
            #j_angle_ta[i] = temp_JA[i]


        return temp_huge_arr


    
    
    
    def timer_callback(self):
        
        global U_Value 
        #values_temp = j_angle_ta
        set_point, Velocity , Acceleration  = self.phi_angle_generator_at_t(self.timer_timer)
        
        for i in range(0,9):
           U_Value[i] = 1*((Acceleration[i] +    self.k_d * ( set_point[i] - FeedBack[i] ) + self.k_p * (Velocity[i] - Vel_FeedBack[i])))
        # creating an array of values to be sent to the joints
        
        
        
        value1 = U_Value[0] 
                                                 #[1.5708,0.0,0.0,0.0,-1.5708,0.0,0.0,0.0,1.5708]
        value2 = U_Value[1] 
       
        value3 = U_Value[2] 
       
        value4 = U_Value[3]
       
        value5 = U_Value[4]
        
        value6 = U_Value[5]
        
        value7 = U_Value[6]
        
        value8 = U_Value[7]
        
        value9 = U_Value[8]
        
        msg = Float64MultiArray()
        msg.data = [value1,value2,value3,value4,value5,value6,value7,value8,value9]
        
        self.Effort_publisher.publish(msg)
        print(set_point)
        
        self.timer_timer = self.timer_timer + 1
        
        if self.timer_timer >2000: 
        	self.timer_timer = 0
        	
      	
        
        

def main(args=None):
     
    rclpy.init(args=args)
    effort_Pub = EffortPublisher()

    rclpy.spin(effort_Pub)
    
    effort_Pub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
