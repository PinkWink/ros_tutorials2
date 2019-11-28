#!/usr/bin/env python

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list


if __name__ == "__main__":
    # First initialize `moveit_commander`_ and a `rospy`_ node:
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('t1_get_basic_info', anonymous=True)

    ## Instantiate a `RobotCommander`_ object
    robot = moveit_commander.RobotCommander()

    # Instantiate a `PlanningSceneInterface`_ object.
    scene = moveit_commander.PlanningSceneInterface()

    ## Instantiate a `MoveGroupCommander`_ object.
    group_name = "arm"
    move_group = moveit_commander.MoveGroupCommander(group_name)

    # Create a `DisplayTrajectory`_ ROS publisher
    display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                                   moveit_msgs.msg.DisplayTrajectory,
                                                   queue_size=20)

    # Getting Basic Information
    planning_frame = move_group.get_planning_frame()
    print "============ Planning frame: %s" % planning_frame

    eef_link = move_group.get_end_effector_link()
    print "============ End effector link: %s" % eef_link

    group_names = robot.get_group_names()
    print "============ Available Planning Groups:", robot.get_group_names()

    # Wait some times for get initialized scene
    rospy.sleep(1)


    # Attatch the box
    scene.attach_box("tip_link", "box", touch_links="tip_link")
    quit()