#include "ros/ros.h"
#include "ar_track_alvar_msgs/AlvarMarkers.h"
#include "i2cpwm_board/ServoArray.h"

int main(int argc, char **argv)
{
	ros::init(argc, argv, "simple_car_cntrl");
	ros::NodeHandle n;
    // subscribe to ar tag detection
    ros::Subscriber ar_sub = n.subscribe("ar_pose_marker", 1000, poseCallback);
    // publish to car servos (motor, steering)
	ros::Publisher servo_pub = n.advertise<i2cpwm_board::ServoArray>("servos_absolute", 1000);
	
    // this while statement should check for a different condition
    // like if the ar tag is x distance away ?
    // not sure how to do this without both subscribing and publishing... hm
    // something about the z value being small (meaning its very close to the camera)
    // backup if z value reaches this point?
    while(ros::ok())
    {
        i2cpwm_board::ServoArray msg;

        // here i need to publish to servo value and its value
        // servo 1 - steering
        // servo 2 - throttle
        // pwm limits (to test) - 300 neutral?

        servo = msg.servo;
        value = msg.value;

        chatter_pub.publish(msg);
        ros::spinOnce();
        loop_rate.sleep();
    }

	return 0;
}
