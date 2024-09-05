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

## 界面说明
Camera view/ Heatmap/ Markin/ Running main.py
![running the script](https://github.com/user-attachments/assets/9a19e64d-f236-491a-9a37-752c1673f733)
![Mankin](https://github.com/user-attachments/assets/ea48b4d8-dec8-4a51-8d33-0ebf9acff76f)
![HeightMap_Script](https://github.com/user-attachments/assets/583f6621-a6c9-483b-8b9a-9045b97b9a38)
![HeightMap](https://github.com/user-attachments/assets/b3d3d6e1-767f-4a21-bc57-7f2660f98b02)
![Camera View](https://github.com/user-attachments/assets/228fa66a-50d8-4d46-bafe-7866a9d06edc)

## Offboard 效果


## Onboard 效果

https://github.com/user-attachments/assets/0a4a3ffb-f2c7-4a74-8b7d-84edd04e5882



## Remark
项目文件在https://docs.px4.io/v1.12/zh/ros/mavros_offboard.html基础上，修改了Macros 功能包的 offboard 模式控制例程的.cpp文件

现在可以实现对无人机轨迹的控制，项目路径为src_PX4_MAVROS_OFFBOARD-main/src/px4_offboard/src/offboard_control.cpp, 其中PX4_MAVROS_OFFBOARD-main 参考 https://github.com/DengYaosheng/PX4_MAVROS_OFFBOARD.git.
