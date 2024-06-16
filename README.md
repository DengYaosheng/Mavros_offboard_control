# Mavros_offboard_control

## 编译
1. 创建ros工作空间, 复制压缩包里的src。编译你的ws即可。

2. 或者直接解压到home后
   cd ~/catkin_ws_1，然后catkin_make，然后source

   bashrc中应具有以下source为正常
    source ~/catkin_ws_1/devel/setup.bash
    source /opt/ros/noetic/setup.bash
    source ~/catkin_ws_1/devel/setup.bash
    
    source ~/catkin_ws/devel/setup.bash
    source ~/PX4_Firmware/Tools/setup_gazebo.bash ~/PX4_Firmware/ ~/PX4_Firmware/build/px4_sitl_default
    export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:~/PX4_Firmware
    export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:~/PX4_Firmware/Tools/sitl_gazebo

## 运行
cd ~/PX4_Framwire (有的老版本是PX4-Autopliot)
roslaunch px4 mavros_posix_sitl.launch
./QGroundControl.AppImage
rosrun px4_offboard px4_offboard
即可运行

## Remark
项目文件在https://docs.px4.io/v1.12/zh/ros/mavros_offboard.html基础上，修改了Macros 功能包的 offboard 模式控制例程的.cpp文件
现在可以实现对无人机轨迹的控制，项目路径为src_PX4_MAVROS_OFFBOARD-main/src/px4_offboard/src/offboard_control.cpp, 其中PX4_MAVROS_OFFBOARD-main 参考 https://github.com/DengYaosheng/PX4_MAVROS_OFFBOARD.git.
