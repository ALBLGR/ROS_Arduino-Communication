#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import urllib
import urllib2
import json
from std_msgs.msg import UInt32
import datetime
import time

pub = rospy.Publisher('arduinoDisplayTopic', String, queue_size=10)
pub1 = rospy.Publisher('servo_topic', UInt32, queue_size=10)


def handleFinger(data):
    isWaiting = True
    count = 0
    while isWaiting :
        test_data = {'rfid': data}
        test_data_urlencode = urllib.urlencode(test_data)
        requrl = "http://alblgr.vicp.net/finger.php"
        req = urllib2.Request(url = requrl,data =test_data_urlencode)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        rospy.loginfo(res)
        JSON_1=json.loads(res)
        rospy.loginfo(JSON_1)
        if JSON_1['isValid'] == "3":
            pub1.publish(3)
            time.sleep(2)
            pub1.publish(0)
            pub.publish("FP Pass")
            isWaiting = False
            rospy.loginfo(JSON_1)
    else:
            time.sleep(1)
            count = count + 1
    if isWaiting:
            pub1.publish(3)
            time.sleep(2)
            pub1.publish(0)
            pub.publish("FP Timed out")

def talker():
    pub = rospy.Publisher('arduinoDisplayTopic', String, queue_size=10)
    if not rospy.is_shutdown():
        rospy.loginfo("Published") 
        #pub.publish(JSON_PAYLOAD['name'])
        try:
            pub.publish(JSON_PAYLOAD['name'])
            if JSON_PAYLOAD['name'] != "NO_MATCH_FOUND" :
                pub1.publish(1)
                time.sleep(2)
                pub1.publish(0)
                handleFinger(JSON_PAYLOAD['rfid'])
        except IndexError:
            pub.publish("NOT_FOUND")

def callback(data):
    dataString = data.data[0:8]
    rospy.loginfo('I heard %s', dataString)
    test_data = {'rfid': dataString}
    test_data_urlencode = urllib.urlencode(test_data)
    requrl = "http://alblgr.vicp.net/handleCardRequest.php"
    req = urllib2.Request(url = requrl,data =test_data_urlencode)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    rospy.loginfo(res)
    global JSON_PAYLOAD
    JSON_PAYLOAD=json.loads(res)
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('arduinoRfidTopic', String, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()

