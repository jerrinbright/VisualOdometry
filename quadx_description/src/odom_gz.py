#! /usr/bin/env python
import rospy
import tf
from gazebo_msgs.msg import ModelStates
from nav_msgs.msg import Odometry
import time

def control_kwad(msg):
  ind = msg.name.index('quadx')
  orientationObj = msg.pose[ind].orientation
  locationobj=msg.pose[ind].position
  positionlist=[locationobj.x,locationobj.y,locationobj.z]
  orientationList = [orientationObj.x, orientationObj.y,orientationObj.z, orientationObj.w]

  br.sendTransform(positionlist,orientationList,rospy.Time.now(),"world","base_link1")
  time.sleep(0.2)

rospy.init_node('turtle_tf_broadcaster')

br = tf.TransformBroadcaster()

PoseSub = rospy.Subscriber('/gazebo/model_states', ModelStates,control_kwad)
rospy.spin()
