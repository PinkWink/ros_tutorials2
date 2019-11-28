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

    print "============ Printing robot state"
    print robot.get_current_state()
    print ""

    # First move robot to point.
    pose_goal = geometry_msgs.msg.Pose()
    pose_goal.orientation.w = 1.0
    pose_goal.position.x = 0.6
    pose_goal.position.y = 0.0
    pose_goal.position.z = 0.6

    move_group.set_pose_target(pose_goal)

    plan = move_group.go(wait=True)
    move_group.stop()
    move_group.clear_pose_targets()

    # Move using cartesian path
    waypoints = []

    wpose = move_group.get_current_pose().pose
    wpose.position.y -= 0.3
    waypoints.append(copy.deepcopy(wpose))

    wpose.position.z += 0.3
    waypoints.append(copy.deepcopy(wpose))

    wpose.position.y += 0.3
    waypoints.append(copy.deepcopy(wpose))

    wpose.position.z -= 0.3
    waypoints.append(copy.deepcopy(wpose))

    (plan, fraction) = move_group.compute_cartesian_path(waypoints, 0.01, 0.0)


    # Display trajectory
    display_trajectory = moveit_msgs.msg.DisplayTrajectory()
    display_trajectory.trajectory_start = robot.get_current_state()
    display_trajectory.trajectory.append(plan)
    display_trajectory_publisher.publish(display_trajectory)


    # Move!
    move_group.execute(plan, wait=True)

    quit()