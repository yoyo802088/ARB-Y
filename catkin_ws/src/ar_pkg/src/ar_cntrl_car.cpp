#include "ros/ros.h"
#include "ar_track_alvar_msgs/AlvarMarkers.h"
#include "i2cpwm_board/ServoArray.h"

void car_cmd(i2cpwm_board::ServoArray::ConstPtr& car_msg, step)
{
    // change PWM values here
    double stop = 300;
    double reverse = 290;

    switch(step)
    {
        case 0:
            car_msg.servo = 2;
            car_msg.value = stop;
        case 1:
            car_msg.servo = 2;
            // realizing this would probably continuously put car into reverse continuously
            car_msg.value = reverse;
    }
}

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
	
    // Running at 10Hz - an arbitrary rate 
	ros::Rate loop_rate(10);

    while(ros::ok())
    {
        // if z is close then stop & reverse
        if(z == close)){
            car_cmd(markers, 0);
            car_cmd(markers, 1);
        }

        servo_pub.publish(markers);
        ros::spinOnce();
    }
	return 0;
}
