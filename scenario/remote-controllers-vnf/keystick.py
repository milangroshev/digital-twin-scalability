#!/usr/bin/env python

import time
import datetime

import rospy
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

from niryo_one_python_api.niryo_one_api import *

from moveit_ros_planning_interface import _moveit_move_group_interface
from moveit_commander import MoveGroupCommander

import sys
import termios
import tty

import csv

import numpy as np

usage = """
Reading from the keyboard and publishing to Niryo One!
---------------------------
Movements:
  w : up (+y)
  s : down (-y)
  a : left (+x)
  d : right (-x)
  2 : up_2 (+y2)
  x : down_2 (-y2)
  q : rotate left (+z)
  e : rotate right (-z)

  CTRL-C to quit
"""

jointsBindings = {
  'a':(1,0,0,0,0,0),
  'd':(-1,0,0,0,0,0),
  'w':(0,1,0,0,0,0),
  's':(0,-1,0,0,0,0),
  '2':(0,0,1,0,0,0),
  'x':(0,0,-1,0,0,0),
  'q':(0,0,0,1,0,0),
  'e':(0,0,0,-1,0,0),
}

modeBindings = {
  '1':"control",
  '2':"moveit",
  '3':"interface",
}

last_position = [0, 0, 0, 0, 0, 0]
moving = True
init_time = 0.0

f = open(__file__[:__file__.find('.')] + '.csv', 'w')
log = csv.writer(f)

def logging(event, hw_timestamp, position):
  log.writerow([int(round(time.time() * 1000000000)),
               event,
               hw_timestamp,
               "{:.3f}".format(position[0]),
               "{:.3f}".format(position[1]),
               "{:.3f}".format(position[2]),
               "{:.3f}".format(position[3]),
               "{:.3f}".format(position[4]),
               "{:.3f}".format(position[5])])

def callback_joint_states(joint_states):
  global moving, last_position, init_time

  rtime = rospy.Time.now()
  print(joint_states.position)

  diff = [abs(x1 - x2) for (x1, x2) in zip(last_position, joint_states.position)]
  if all(x < 0.0001 for x in diff) == True:
    if moving == True:
      moving = False
      elapsed_time = (rtime.secs * 1000000000 + rtime.nsecs) - init_time
      print("Execution time: ", elapsed_time / 1000000, "ms")

def getKey():
  tty.setraw(sys.stdin.fileno())
  key = sys.stdin.read(1)
  termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
  return key

# TODO: Split each mode into different functions
def move_to_position(p, n, a, pos, cmd_speed, mode):
  global moving, last_position, init_time

  rtime = rospy.Time.now()
  if mode == "interface":
    # Interface
    print("Interface")
    n.move_joints(pos)
    etime = rospy.Time.now()
    print(((etime.secs * 1000000000 + etime.nsecs) - (rtime.secs * 1000000000 + rtime.nsecs)))
  elif mode == "moveit":
    # Moveit
    print("Moveit")
    #a.set_pose_target([3,3,3, 0,0,0])
    #etime = rospy.Time.now()
    #print(((etime.secs * 1000000000 + etime.nsecs) - (rtime.secs * 1000000000 + rtime.nsecs)))
#    a.go(pos, wait=False)
  elif mode == "control":

    # Control Mode
    print("Control")
    msg = JointTrajectory()
    msg.header.stamp = rtime
    msg.joint_names = ['joint_1', 'joint_2', # X_AXIS, Y_AXIS
                       'joint_3', 'joint_4', # Y2_AXIS, Z_AXIS
                       'joint_5', 'joint_6'] # Not supported yet

    point = JointTrajectoryPoint()
    point.positions = pos
    point.time_from_start = rospy.Duration(cmd_speed)
    msg.points = [point]
    p.publish(msg)

  # Save last position command
  last_position = pos
  moving = True
  init_time = rtime.secs * 1000000000 + rtime.nsecs

  # Sleep to ensure that the command was executed by the physical robot
  time.sleep(0.020)

if __name__=="__main__":
  settings = termios.tcgetattr(sys.stdin)

  # Variables
  mode = "control"
  cmd_speed = 0.020
  key_offset = 0.010
  position = [0, 0, 0, 0, 0, 0]

  rospy.init_node('niryo_one_keystick')
  pub = rospy.Publisher('/niryo_one_follow_joint_trajectory_controller/command',
                          JointTrajectory, queue_size=10)
  n = NiryoOne()
  m = MoveGroupCommander("arm")

  print("Waiting 2 Seconds to connect...")
  time.sleep(2)

  # Move to initial position
  print("Waiting 2 Seconds to move to initial position...")
  move_to_position(pub, n, m, position, cmd_speed, mode)
  n.move_joints([0,0,0,0,0,0]) 
  time.sleep(2)

  # Subscribe current pose, only after the initial state is set
  sub = rospy.Subscriber('/joint_states', JointState, callback_joint_states)

  print(usage)
  try:
    while(True):
      key = getKey()
      if key in modeBindings.keys():
        mode = modeBindings[key]
        print(mode)
      elif key in jointsBindings.keys():
        position[0] += jointsBindings[key][0] * key_offset
        position[1] += jointsBindings[key][1] * key_offset
        position[2] += jointsBindings[key][2] * key_offset
        position[3] += jointsBindings[key][3] * key_offset
        position[4] # Not implemented
        position[5] # Not implemented

        logging("joint_sent", 0, position)
        move_to_position(pub, n, m, position, cmd_speed, mode)
      elif (key == '\x03'):
        break
      else:
        pass # Do nothing

  except Exception as e:
    print(e)

  finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

