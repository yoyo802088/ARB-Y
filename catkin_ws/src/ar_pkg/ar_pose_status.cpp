#include "ros/ros.h"
#include "ar_track_alvar_msgs/AlvarMarkers.h"
void poseCallback(const ar_track_alvar_msgs::AlvarMarkers::ConstPtr& msg){
	double x = msgcd->markers[0].pose.pose.position.x;
	double y = msg->markers[0].pose.pose.position.y;
	double z = msg->markers[0].pose.pose.position.z;
	ROS_INFO("x: %f, y: %f z: %f", x, y, z);
}

int main(int argc, char **argv)
{
	ros::init(argc, argv, "ar_pose_status");
	ros::NodeHandle n;
	ros::Subscriber sub = n.subscribe("ar_pose_marker", 1000, poseCallback);
	ros::spin();
	return 0;
}
