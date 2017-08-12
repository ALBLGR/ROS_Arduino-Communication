#!/usr/bin/env python
# license removed for brevity
import rospy
import random
from std_msgs.msg import UInt32

def talker():
    pub = rospy.Publisher('servo_topic', UInt32, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(2) # 1hz
    while not rospy.is_shutdown():
	degree = input()
        #hello_str = random.randint(1, 180)
	rospy.loginfo("Published")        
	#rospy.loginfo(rospy.get_time())
        pub.publish(degree)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
