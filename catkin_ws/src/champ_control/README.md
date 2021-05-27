# Run the car
This is a description of how to run the car.

Before running anything on the github, make sure that the car is on and properly connected to the devices.

First, launch i2cpwm to enable the motor connection between the board and the car.

    $ roslaunch i2cpwm_board i2cpwm_node.launch
    
or
    
    $ roscore
    $ rosrun i2cpwm_board i2cpwm_board

Next, to launch the example, open a terminal and launch:

    $ roslaunch champ_control car_mapping.launch

This will open up rviz that displays the current position and generated map.
The goals can be set either by clicking the "2D Nav Goal" button and dragging on the screen, or through code.

# Emergency Escape
The file needed will be "position_tracking.py".

To start the process of detecting emergency, open a terminal and launch:

     $ python3 emergency_escape.py
     
This will enable emergency escape afterwards, and the corresponding help messages will appear in the terminal.
