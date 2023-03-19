import os
from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler
from ament_index_python.packages import get_package_share_directory
from ament_index_python.packages import get_package_share_path
from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
     
     
    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!
    
    package_name='my_bot' #<--- CHANGE ME
    
    pkg_share = FindPackageShare(package='my_bot').find('my_bot')   
    
    default_rviz_config_path = os.path.join(pkg_share, 'rviz/snake.rviz')   
        
     #urdf_tutorial_path = get_package_share_path('my_bot')
    
    
    rviz_arg = DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
                                     description='Absolute path to rviz config file')
                                     
                                     

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
       ) 

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
             )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'snake_robot'],
                        output='screen')

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
     )
    
    
    
    #load_trajectory_controller = ExecuteProcess(
     #   cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
      #       'joint_trajectory_controller'],
       # output='screen'
    #)           

    # Launch them all!
    return LaunchDescription([
        rviz_arg,    
        rsp,
        gazebo,
        spawn_entity,
        rviz_node,
        #load_trajectory_controller,
              ])
