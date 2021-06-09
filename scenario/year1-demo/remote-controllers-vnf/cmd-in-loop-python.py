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

# To use the API, copy these 4 lines on each Python file you create
from niryo_one_python_api.niryo_one_api import *
import rospy
import time
import datetime
import csv
from sensor_msgs.msg import JointState
import sys, select, termios, tty
import argparse
import socket

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


def move_to_position(n,pos,cmd_speed):
  global moving, last_position, init_time

  rtime = rospy.Time.now()

  # Save last position command
  last_position = pos
  moving = True
  init_time = rtime.secs * 1000000000 + rtime.nsecs

  n.move_joints(pos)

def callback_joint_states(joint_states):
  global moving, last_position, init_time

  rtime = rospy.Time.now()

  diff = [abs(x1 - x2) for (x1, x2) in zip(last_position, joint_states.position)]
  if all(x < 0.0001 for x in diff) == True:
    if moving == True:
      moving = False
      elapsed_time = (rtime.secs * 1000000000 + rtime.nsecs) - init_time
      logging(name, elapsed_time / 1000000, position)
      print("Execution time: ", elapsed_time / 1000000, "ms")

if __name__=="__main__":
    rospy.init_node('niryo_one_example_python_api')
    n = NiryoOne()

    # Calibrate robot first
    n.calibrate_auto()
    print "Calibration performed!"
    
    # Variables
    cmd_speed = args.cmd_speed
    key_offset = args.key_offset
    position = [0, 0, 0, 0, 0, 0]    
   
    n.set_arm_max_velocity(100)
    print("Waiting 2 Seconds to connect")
    time.sleep(2)

    # Move to initial position
    print("Waiting 2 Seconds to move to initial position...")
    ipos = False
    while ipos == False:
      try:
        move_to_position(n, position, cmd_speed)
        time.sleep(2)
        ipos = True
      except Exception as e:
        print(e) 
  
    # Subscribe current pose, only after the initial state is set
    sub = rospy.Subscriber('/joint_states', JointState, callback_joint_states)
    time.sleep(2)
    while(True):
        try:
            for x in range(-1, -50, -1) + range(1, 50, 1):
                position[0] += (1 if x > 0 else -1) * key_offset
                position[1] += (1 if x > 0 else -1) * key_offset
                position[2] += (1 if x > 0 else -1) * key_offset
  #              start_time = time.time()
                move_to_position(n, position, cmd_speed)
   #             elapsed = time.time() - start_time
   #             logging(name, elapsed, position)
                time.sleep(1)

        except NiryoOneException as e:
            print(e)
