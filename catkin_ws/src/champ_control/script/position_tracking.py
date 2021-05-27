from __future__ import print_function

import threading
import sys, select, termios, tty
import pyzed.sl as sl
import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy
import time
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped
import sys, select, termios, tty

msg = ""

moveBindings = {
        'i':(1,0,0,0),
        'o':(1,0,0,-1),
        'j':(0,0,0,1),
        'l':(0,0,0,-1),
        'u':(1,0,0,1),
        ',':(-1,0,0,0),
        '.':(-1,0,0,1),
        'm':(-1,0,0,-1),
    }

class EmergencyControl():
    def __init__(self):
        self.posx = 0
        self.posy = 0
        self.posz = 0
        self.PosArr = []
        self.PrevStuck = -1

    def getPoseData(self,message):
        self.posx = message.pose.position.x
        self.posy = message.pose.position.y
        self.posz = message.pose.position.z
        if(self.PrevStuck == -1):
            self.PrevStuck = [self.posx,self.posy,self.posz]
        if(len(self.PosArr) > 10000):
            self.PosArr.pop(0)    
        self.PosArr.append([self.posx,self.posy,self.posz])

    def compareArr(self, PosArr,thres = 0.001):
        startx = self.PrevStuck[0]
        starty = self.PrevStuck[1]
        startz = self.PrevStuck[2]
        count = 0
        for i in range(len(PosArr)):
            if (PosArr[i][0] - startx < thres) and (PosArr[i][1] - starty < thres) and (PosArr[i][2] - startz < thres):
                count += 1
        return (count >= 9999)
           
    def start_control(self):
        #Hard code moving basic set
        settings = termios.tcgetattr(sys.stdin)

        rospy.init_node('teleop_twist_keyboard')

        speed = rospy.get_param("~speed", 0.4)
        turn = rospy.get_param("~turn", 1.0)
        repeat = rospy.get_param("~repeat_rate", 0.0)
        key_timeout = rospy.get_param("~key_timeout", 0.0)
        if key_timeout == 0.0:
            key_timeout = None
  
        pub_thread = PublishThread(repeat)

        x = 0
        y = 0
        z = 0
        th = 0
        status = 0
  

        text_translation = ""
        text_rotation = ""
        pub_thread.wait_for_subscribers()
        count = 0
        break_count = 0

        for i in range(10000):
            if(break_count >= 3):
                break
            print("hello")
            try:
                key_list = ['i','u','o','m','.']
                temp_x = rospy.Subscriber("/zed/zed_node/pose", PoseStamped, self.getPoseData)
                rospy.loginfo("> Subscriber corrrectly initialized")
                print(len(self.PosArr))
                print(self.PrevStuck)
                print(self.PosArr[len(self.PosArr)-5:])
                if(self.compareArr(self.PosArr)):
                    self.PrevStuck = self.PosArr[-1]
                    rospy.loginfo("Compared, not moving")
                    count +=1
                    if (count >= 5):
                        break_count += 1
                        rospy.loginfo("Help! Stuck!")
                        time.sleep(10)
                        count = 0
                    else:
                        key = key_list[count-1]
                        x = moveBindings[key][0]
                        y = moveBindings[key][1]
                        z = moveBindings[key][2]
                        th = moveBindings[key][3]
                        pub_thread.update(x, y, z, th, speed, turn)
                        time.sleep(2)
                        pub_thread.update(0,0,0,0,0,0)

                else:
                    self.PrevStuck = self.PosArr[-1]
                    count = 0
                    continue

            except Exception as e:
                print(e)



class PublishThread(threading.Thread):
    def __init__(self, rate):
        super(PublishThread, self).__init__()
        self.publisher = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.th = 0.0
        self.speed = 0.0
        self.turn = 0.0
        self.condition = threading.Condition()
        self.done = False

        # Set timeout to None if rate is 0 (causes new_message to wait forever
        # for new data to publish)
        if rate != 0.0:
            self.timeout = 1.0 / rate
        else:
            self.timeout = None

        self.start()

    def wait_for_subscribers(self):
        i = 0
        while not rospy.is_shutdown() and self.publisher.get_num_connections() == 0:
            if i == 4:
                print("Waiting for subscriber to connect to {}".format(self.publisher.name))
            rospy.sleep(0.5)
            i += 1
            i = i % 5
        if rospy.is_shutdown():
            raise Exception("Got shutdown request before subscribers connected")
            exit()

    def update(self, x, y, z, th, speed, turn):
        self.condition.acquire()
        self.x = x
        self.y = y
        self.z = z
        self.th = th
        self.speed = speed
        self.turn = turn
        # Notify publish thread that we have a new message.
        self.condition.notify()
        self.condition.release()

    def stop(self):
        self.done = True
        self.update(0, 0, 0, 0, 0, 0)
        self.join()

    def run(self):
        twist = Twist()
        while not self.done:
            self.condition.acquire()
            # Wait for a new message or timeout.
            self.condition.wait(self.timeout)

            # Copy state into twist message.
            twist.linear.x = self.x * self.speed
            twist.linear.y = self.y * self.speed
            twist.linear.z = self.z * self.speed
            twist.angular.x = 0
            twist.angular.y = 0
            twist.angular.z = self.th * self.turn

            self.condition.release()

            # Publish.
            self.publisher.publish(twist)

        # Publish stop message when thread exits.
        twist.linear.x = 0
        twist.linear.y = 0
        twist.linear.z = 0
        twist.angular.x = 0
        twist.angular.y = 0
        twist.angular.z = 0
        self.publisher.publish(twist)



def vels(speed, turn):
    return "currently:\tspeed %s\tturn %s " % (speed,turn)

def main():
    control = EmergencyControl()
    control.start_control()

main()

      
