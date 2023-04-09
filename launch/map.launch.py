# -*- coding: utf-8 -*-
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():

    # gazebo.launch.py package
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    # determine package where .world file is located
    pkg_dolly_gazebo = get_package_share_directory('my_bot')



    return LaunchDescription([
        DeclareLaunchArgument(
          'world',
          default_value=[os.path.join(pkg_dolly_gazebo, 'worlds', 'empty.world'), ''],
          description='SDF world file'),
    
    ])
