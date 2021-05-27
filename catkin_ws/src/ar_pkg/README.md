# Using the AR Tag package

## Installation
To start, install the package for your distribution:
We used the melodic distrubution of ROS which is compatible with Ubuntu 18.0.4 on Linux. 

```bash
sudo apt-get install ros-melodic-ar-track-alvar
```

## Usage
Create your first marker. Here I created a marker with the id '123'

```bash
rosrun ar_track_alvar createMarker 123
```

I'm using catkin workspaces which could be read about [here][catkin_ws]. In catkin_ws/src I ran:

```bash
git clone https://github.com/atomoclast/ar_tag_toolbox
```

Back in /catkin_ws I ran
```bash
catkin_make
```

At this point you need to calibrate your camera. I followed [this][cam_calibrate] tutorial on how to calibrate a monocular camera. It would be a slightly different procedure if you were using a stereo camera. 

For the calibration I didn't have access to a larger paper size than a regular 8.5x11 so I simply printed out the checkerboard on that and measured the squares myself. My squares came out to be 0.025m long.

Before you run the calibration program made sure to run the two following commands: (Note: if usb_cam isn't installed already, install it now!)

```bash
roscore
rosrun usb_cam usb_cam_node
```

Now run the calibration program:
```bash
rosrun camera_calibration cameracalibrator.py --size 8x6 --square 0.025 image:=/usb_cam/image_raw camera:=/usb_cam
```

Once the GUI is open, move your sheet of paper around in front of the webcam, at different angles and distances. Do this until the calibrate button is highlighted and then after it finishes calibrating save and commit it. Now point the camera at your printed AR tags and run the following: 
(My marker size was 5cm and my webcam was #2 but change if you need)

```bash
roslaunch ar_tag_toolbox usb_cam.launch cam_id:=2
roslaunch ar_tag_toolbox ar_track_usb_cam.launch marker_size:=5
```

This next command will let you see the id of the AR Tag being detected.
```bash
rostopic echo /ar_pose_marker
```

Here's the part most tutorials left out. I needed to see if the camera could see where the tags were in relation to itself. This is done in RViz. To open up Rviz I ran:

```bash
rosrun rviz rviz
```

Once there, make sure to point the camera at an AR tag.
- Add the Camera display to the sidebar, the camera stream should pop up
- Under Global Options, change the Fixed Frame to usb_cam
- Add the TF display to the sidebar
- You can now see the positions of the AR tags in relation to the camera!


[catkin_ws]: http://wiki.ros.org/catkin/Tutorials/create_a_workspace
[cam_calibrate]: http://wiki.ros.org/camera_calibration/Tutorials/MonocularCalibration#Before_Starting

