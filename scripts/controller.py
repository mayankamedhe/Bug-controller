#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from quat2euler import quat2euler

import numpy
import math

## Define global variables
pose = [-5, 0, 100]
range_data = [100, 100, 100]
follow_obs = 0
goal = [5, 0]
velo = 0.
ang_velo = 0
align = 0
start_linear = 0
fac = 0.6
align_obs = 0
start_linear1 = 0

def callback(data):
    global pose
    x  = data.pose.pose.orientation.x;
    y  = data.pose.pose.orientation.y;
    z = data.pose.pose.orientation.z;
    w = data.pose.pose.orientation.w;
    pose = [data.pose.pose.position.x, data.pose.pose.position.y, quat2euler(x,y,z,w)[2]]
    
def laser_callback(msg):
    global range_data
    data=msg.ranges    
    range_data=[min(data[480:719]),min(data[240:479]),min(data[0:239])]
    

## This is where we will calculate error and apply the proportional control to 
##  compute linear velocity and angular velocity for the turtlebot 
def control_loop():
    global pose, range_data, velo, ang_velo, follow_obs, goal, start_linear, align, fac, start_linear1, align_obs
    
    position = open("position.txt", "w")

    rospy.init_node('differential_bot_con')
    pub = rospy.Publisher('/bot_0/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/bot_0/odom', Odometry, callback)
    sub=rospy.Subscriber('/bot_0/laser/scan',LaserScan,laser_callback)
    
    rate = rospy.Rate(3) 
        
    while not rospy.is_shutdown():
        velocity_msg = Twist()
        velocity_msg.linear.x = velo
        velocity_msg.angular.z = ang_velo
    
        print("State= " + str(follow_obs) + " range= " + str(range_data[1]) + " pose= " + str(pose[0]))     

        if math.sqrt((pose[0] - goal[0])**2 + (pose[1] - goal[1])**2) <= 0.4:
            velo = 0
            ang_velo = 0

        try:
            if range_data[1] <= 0.4 and align_obs == 0:
                follow_obs = 1
            elif align_obs == 1 and range_data[0] >= 100:
                follow_obs = 0

            if follow_obs == 0:
                if start_linear == 1:
                    e_pos = math.sqrt((goal[0] - pose[0])**2 + (goal[1] - pose[1])**2)
                    e_theta = math.atan2((goal[1] - pose[1]), (goal[0] - pose[0])) - pose[2]
                    velo = 0.01 * e_pos
                    ang_velo = fac * e_theta
                if abs(pose[2]) <= 0.05:
                    align = 1
                    start_linear = 1
                elif align == 0:
                    ang_velo = -0.06
                    velo = 0             
            else:
                if range_data[1] > 10:
                    align_obs = 1
                    ang_velo = 0
                    velo = 0.07
                    start_linear = 1
                elif align_obs == 0:
                    ang_velo = -0.2
                    velo = 0
                fac = 0.1
            position.write(str(pose[0]) + "," + str(pose[1]) + "\n")

        except:
            pass

        pub.publish(velocity_msg)
        rate.sleep()
    position.close()

if __name__ == '__main__':
    try:
        control_loop()
    except rospy.ROSInterruptException:
        pass
