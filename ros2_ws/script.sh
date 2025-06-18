#!/bin/bash

set -e

echo "[🛠️] Initialisation du workspace ROS..."

# Création du workspace
mkdir -p /ros2_ws/ros_workshop_ws/src
cd /ros2_ws/ros_workshop_ws/src/

# Clonage des dépôts nécessaires
git clone -b jazzy https://github.com/ROBOTIS-GIT/DynamixelSDK.git
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3.git
git clone -b jazzy https://github.com/ROBOTIS-GIT/open_manipulator.git

# 💡 Copie des sources personnalisées (écrasement)
echo "[📁] Remplacement du contenu de open_manipulator_playground par /ros2_ws/take_ball_src"
cp -r /ros2_ws/take_ball_src/* /ros2_ws/ros_workshop_ws/src/open_manipulator/open_manipulator_playground/

# Compilation
cd /ros2_ws/ros_workshop_ws
colcon build --symlink-install

# Ajout à ~/.bashrc si non déjà présent
echo 'source /ros2_ws/ros_workshop_ws/install/setup.bash' >> ~/.bashrc
echo 'export ROS_DOMAIN_ID=127' >> ~/.bashrc
echo 'export TURTLEBOT3_MODEL=burger' >> ~/.bashrc
echo 'export ROBOT_MODEL=om_x' >> ~/.bashrc

# Activation immédiate
source ~/.bashrc
source /ros2_ws/ros_workshop_ws/install/setup.bash

echo "[✅] Workspace prêt avec les sources personnalisées !"

