# ARB-Y (Autonomous Rover Bot - Youngling)

## Introduction
Autonomous rover project for the EEC193AB course and University Rover Challenge
Key features included:
- Autonomous driving & Goal Setting
- Pit detection & avoidance
- AR Tag Detection
- Emergency escape mechanism

## Objectives \& Testing
Tested each mechanism separately from each other to avoid complications

### Goal Setting & Autonomous Driving 
Utilized the rtabmap package on ROS to integrate vSLAM into our system. Mainly aimed at the car’s throttle and steering responding to a set goal. The goal is designed to be set through a series of local goals (set automatically by the rover) moving towards a global goal (set by humans).

### Pit Detection Feature
Leveraged the openCV package on Python to perform depth perception using our 3D stereo camera. openCV is also used to cluster regions with "deeper" pixels, to detect potential pits for the rover to avoid.
    
### Ar Tag Detection & Action
Basic AR tag detection. If the rover detected an AR Tag, then it would respond by moving slowly towards it
    
### Emergency Detection & Escape Mechanism
Designed for the rover to perform a fixed set of operations to attempt to "escape" from an emergency situation (e.g., getting stuck). The "emergency" is detected through calculating the difference between throttle and actual movement of the rover.
    
# Reports \& Presentations
For a simple demo video, please watch [this video](https://www.youtube.com/watch?v=riW5-ti9QEk).

For our poster presentation, refer to [this](./poster.pdf)

# Contributions

- Yu-Shih Chen - Team lead, mainly contributed to the development of the pit detection feature and vSLAM integration.
- Wanyue Zhai - Main developer of the vSLAM \& sensor integration and emergency escape mechanism.
- May Eusebio - Main developer of the AR tag detection mechanism.
- Zeyuan Hou - Main developer of the emergency escape mechanism.

