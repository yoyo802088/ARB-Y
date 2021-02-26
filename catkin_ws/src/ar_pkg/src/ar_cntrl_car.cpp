#include "ros/ros.h"
#include "ar_track_alvar_msgs/AlvarMarkers.h"
#include "i2cpwm_board/ServoArray.h"

int main(int argc, char **argv)
{
	ros::init(argc, argv, "ar_car_cntrl");
	ros::NodeHandle n;

    ros::Subscriber ar_sub = n.subscribe("ar_pose_marker", 1000, poseCallback);
	ros::Publisher servo_pub = n.advertise<i2cpwm_board::ServoArray>("servos_absolute", 1000);

    ar_track_alvar_msgs::AlvarMarkers markers;
    i2cpwm_board::ServoArray msg;

    // assume marker position
    z = markers.markers[0].pose.pose.position.z;
    z = 0;

    // condition for how close cam should be to ar tag - arbitrary 0.5 value
    double close = 0.5;

    // set steering (servo 1) and throttle (servo 2)
    servo = msg.servo; 
    value = msg.value;

    // assuming 300 is neutral for both - change if necessary
    double neutral = 300.0; 
	
    // Running at 10Hz - an arbitrary rate 
	ros::Rate loop_rate(10);

    while(ros::ok())
    {
        // if z is close then stop & reverse
        if(z == close)){
            neutral;
            reverse;
        }

        servo_pub.publish(something);
        servo_pub.publish(something);
        ros::spinOnce();
    }
	return 0;
}
