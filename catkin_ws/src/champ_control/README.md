# Run the car
This is a description of how to run the car.

## Installation

Before running anything on the github, make sure that the car is on and properly connected to the devices and the repository is properly installed. 

    $ git clone https://github.com/yoyo802088/EEC193AB-RoveCrest.git
    

First, launch i2cpwm to enable the motor connection between the board and the car.

    $ roslaunch i2cpwm_board i2cpwm_node.launch
    
or
    
    $ roscore
    $ rosrun i2cpwm_board i2cpwm_board

Next, to launch the example, open a terminal and launch:

    $ roslaunch champ_control car_mapping.launch

This will open up rviz that displays the current position and generated map.

If rviz is not displaying the path and goal, click the "Add" button on the left of rviz display pannel and add "/move_base/NavfnROS/plan" with type "Path" for the display of planned path, and add "/move_base/current_goal" with type "Goal" for the display of the current goal.

The goals can be set either by clicking the "2D Nav Goal" button and dragging on the screen, or through code in ./script/move_base_seq.py.

## Remote connection between HDMI and a remote PC
There are times when we need to monitor the car's performance remotely on our own computer, so here is a simple guide on how to do so.

   1. Make sure the two devices are under the same network.
    
   2. Use ifconfig on both machines to get the IP addresses of each of the machines.
    
   3. On the HDMI connected device, type the following:

    $ export ROS_MASTER_URI=http://<HDMI IP address>:11311
    $ export ROS_IP=<HDMI IP address>
   4. On the remote computer, type the following:
  
    $ export ROS_MASTER_URI=http://<HDMI IP address>:11311
    $ export ROS_IP=<computer IP address>
    
   5. To test the connection, open a terminal and make sure roscore is running in the back. Type the following in both devices:
   
    $ rostopic list
   If the topics that appears are the same, then you have successfully established a connection.
   
 For more information, please visit [http://wiki.ros.org/ROS/Tutorials/MultipleMachines]
    

# Emergency Escape
The file needed will be "emergency_escape.py".

To start the process of detecting emergency, open a terminal and launch:

     $ python3 emergency_escape.py
     
This will enable emergency escape afterwards, and the corresponding help messages will appear in the terminal.
