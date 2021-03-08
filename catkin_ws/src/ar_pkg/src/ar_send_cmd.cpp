#include "ros/ros.h"
#include "ar_track_alvar_msgs/AlvarMarkers.h"
#include "geometry_msgs/Twist.h"

void poseCallback(const ar_track_alvar_msgs::AlvarMarkers::ConstPtr& msg){
	double x = msg->markers[0].pose.pose.position.x;
	double y = msg->markers[0].pose.pose.position.y;
	double z = msg->markers[0].pose.pose.position.z;
	ROS_INFO("x: %f, y: %f z: %f", x, y, z);
}

int main(int argc, char **argv)
{
	ros::init(argc, argv, "ar_car_cntrl");
	ros::NodeHandle n;

	ros::Subscriber pose_sub = n.subscribe("ar_pose_marker", 1000, poseCallback);
	ros::Publisher cmd_pub = n.advertise<geometry_msgs::Twist>("cmd_vel", 1000);
	
	ar_track_alvar_msgs::AlvarMarkers markers;
	geometry_msgs::Twist cmd;

	double z = markers.markers[0].pose.pose.position.z;

    while(ros::ok())
    {
        // if tag is close
        if(z < 10)
        {
            // move closer to the tag
            cmd.linear.z = 5;
        } else {

        }

        cmd_pub.publish(cmd);
    }

	ros::spin();
	return 0;
}