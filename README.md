# color_depth_edit
calclate or edit color &amp; depth images from realsense or kinect
<img width="806" alt="color-depth-edit" src="https://user-images.githubusercontent.com/45028425/48907984-6c168180-eeac-11e8-9f89-f4cdedbddd98.png">

[Requirements]
Ubuntu 16.04  
ROS  

[Usage]  
(open a terminal)  
roscore  
(move to color_depth_edit/rosbag directory)  
rosbag play -l rs-sample-2m.bag  
roslaunch color_depth_edit color_depth_edit.launch  
