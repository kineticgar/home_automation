#!/usr/bin/env python
#
#    Copyright (C) 2014 Garrett Brown
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import roslib; roslib.load_manifest('home_automation')
import rospy
import smach
import smach_ros

# State Exhibit
class Exhibit(smach.State):
  def __init__(self):
    smach.State.__init__(self, outcomes=['succeeded', 'preempted', 'aborted'])
    self.counter = 0

  def execute(self, userdata):
    rospy.loginfo('Executing state EXHIBIT')
    if self.counter < 3:
      self.counter += 1
      return 'succeeded'
    else:
      return 'aborted'

# State Idle
class Idle(smach.State):
  def __init__(self):
    smach.State.__init__(self, outcomes=['succeeded', 'preempted', 'aborted'])

  def execute(self, userdata):
    rospy.loginfo('Executing state IDLE')
    return 'succeeded'

# Entry point
def main():
  rospy.init_node('home_automation_state_machine')

  # Create a SMACH state machine
  sm = smach.StateMachine(outcomes=['preempted', 'aborted'])

  # Open the container
  with sm:
    # Add states to the container
    smach.StateMachine.add('EXHIBIT', Exhibit(), 
      transitions = {
        'succeeded': 'IDLE',
        'preempted': 'preempted',
        'aborted':   'aborted'
      }
    )
    smach.StateMachine.add('IDLE', Idle(), 
      transitions = {
        'succeeded': 'EXHIBIT',
        'preempted': 'preempted',
        'aborted':   'aborted'
      }
    )

  # Execute SMACH plan
  outcome = sm.execute()

if __name__ == '__main__':
  main()

