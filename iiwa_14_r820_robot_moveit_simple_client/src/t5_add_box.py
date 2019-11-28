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


    # Add box
    box_pose = geometry_msgs.msg.PoseStamped()
    box_pose.header.frame_id = "tip_link"
    box_pose.pose.orientation.w = 1.0
    box_pose.pose.position.z = 0.055 # slightly above the end effector
    box_name = "box"
    scene.add_box(box_name, box_pose, size=(0.1, 0.1, 0.1))

    timeout = 4
    start = rospy.get_time()
    seconds = rospy.get_time()
    while (seconds - start < timeout) and not rospy.is_shutdown():
        # Test if the box is in the scene.
        # Note that attaching the box will remove it from known_objects
        is_known = box_name in scene.get_known_object_names()

        if is_known:
            print "Success"
            quit()

        # Sleep so that we give other threads time on the processor
        rospy.sleep(0.1)
        seconds = rospy.get_time()

    print "False"
    quit()