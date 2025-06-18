#!/bin/bash

set -e

echo "[🛠️] Initialisation du workspace ROS..."

mkdir -p /ros2_ws/ros_workshop_ws/src
cd /ros2_ws/ros_workshop_ws/src/

git clone -b jazzy https://github.com/ROBOTIS-GIT/DynamixelSDK.git
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3.git
git clone -b jazzy https://github.com/ROBOTIS-GIT/open_manipulator.git

cd /ros2_ws/ros_workshop_ws
colcon build --symlink-install

echo 'source /ros2_ws/ros_workshop_ws/install/setup.bash' >> ~/.bashrc
echo 'export ROS_DOMAIN_ID=127' >> ~/.bashrc
echo 'export TURTLEBOT3_MODEL=burger' >> ~/.bashrc
echo 'export ROBOT_MODEL=om_x' >> ~/.bashrc

# Activation immédiate de l’environnement
source ~/.bashrc
source /ros2_ws/ros_workshop_ws/install/setup.bash

echo "[✅] Workspace prêt !"

