#!/usr/bin/env python

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import time
import datetime
import csv
from sensor_msgs.msg import JointState
import sys, select, termios, tty
import argparse
import socket

import rospy
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

name = socket.gethostbyname(socket.gethostname())
last_position = [0, 0, 0, 0, 0, 0]
moving = True
init_time = 0.0

global INPUT_DIR, OUT_PARSED_DIR
parser = argparse.ArgumentParser()
parser.add_argument('--filename', help="name of the file in which data will be stored", type=str, default="/home/niryo/logs/"+name)
parser.add_argument('--duration', help="duration in seconds of the command in loop",type=int,
                    default=60)
parser.add_argument('--cmd_speed', help="sleep time after each command execution",
                    type=float, default=0.020)
parser.add_argument('--key_offset',help="offset between each command",type=float,
                    default=0.010)
args = parser.parse_args()
filename=args.filename
f = open(filename+'.csv', 'w')
log = csv.writer(f)
log.writerow(["timestamp", "node", "latency", "joint_1", "joint_2", "joint_3", "joint_4", "joint_5", "joint_6"])


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
  sys.stdout.flush()


def move_to_position(p,pos,cmd_speed):
  rtime = rospy.Time.now()

  # Save last position command
  global moving, last_position, init_time
  last_position = pos
  moving = True
  init_time = rtime.secs * 1000000000 + rtime.nsecs

  msg = JointTrajectory()
  msg.header.stamp = rtime
  msg.joint_names = ['joint_1', 'joint_2', 'joint_3', # X, Y, Z
                     'joint_4', 'joint_5', 'joint_6'] # Not supported yet

  point = JointTrajectoryPoint()
  point.positions = pos
  point.time_from_start = rospy.Duration(cmd_speed)
  msg.points = [point]
  p.publish(msg)

def callback_joint_states(joint_states):
  rtime = rospy.Time.now()
  global moving, last_position, init_time
  print(last_position, " : ", joint_states.position)
  diff = [abs(x1 - x2) for (x1, x2) in zip(last_position, joint_states.position)]
  if all(x < 0.0001 for x in diff) == True:
    print("\n\nEqual")
    if moving == True:
      moving = False
      elapsed_time = (rtime.secs * 1000000000 + rtime.nsecs) - init_time
      logging(name, elapsed_time / 1000000, position)
      print("\n\nlog")
      #print("Execution time: ", elapsed_time / 1000000, "ms")

if __name__=="__main__":
  # Variables
  cmd_speed = args.cmd_speed
  key_offset = args.key_offset
  position = [0, 0, 0, 0, 0, 0]
  last_positon = position

  rospy.init_node('niryo_one_example_python_api')

  pub = rospy.Publisher('/niryo_one_follow_joint_trajectory_controller/command',
                         JointTrajectory, queue_size=1, tcp_nodelay=True)
  print("Waiting 2 Seconds to connect.")
  time.sleep(2)

  # Move to initial position
  print("Waiting 2 Seconds to move to initial position...")
  move_to_position(pub, position, cmd_speed)
  time.sleep(2)

  # Subscribe current pose, only after the initial state is set
  sub = rospy.Subscriber('/joint_states', JointState, callback_joint_states)
  time.sleep(2)
   
  while(True):
    try:
      for x in range(-1, -50, -1) + range(1, 50, 1):
        position[0] += (1 if x > 0 else -1) * key_offset
        position[1] += (1 if x > 0 else -1) * key_offset
        position[2] += (1 if x > 0 else -1) * key_offset
        move_to_position(pub, position, cmd_speed)
        print("move")
        time.sleep(1)

    except Exception as e:
      print(e) 

