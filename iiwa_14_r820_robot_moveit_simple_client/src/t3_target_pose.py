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

    # Getting Basic Information
    planning_frame = move_group.get_planning_frame()
    print "============ Planning frame: %s" % planning_frame

    eef_link = move_group.get_end_effector_link()
    print "============ End effector link: %s" % eef_link

    group_names = robot.get_group_names()
    print "============ Available Planning Groups:", robot.get_group_names()

    print "============ Printing robot state"
    print robot.get_current_state()
    print ""

    # Move using target_pose
    pose_goal = geometry_msgs.msg.Pose()
    pose_goal.orientation.w = 1.0
    pose_goal.position.x = 0.4
    pose_goal.position.y = 0.1
    pose_goal.position.z = 0.4

    move_group.set_pose_target(pose_goal)

    plan = move_group.go(wait=True)
    move_group.stop()
    move_group.clear_pose_targets()

    quit()