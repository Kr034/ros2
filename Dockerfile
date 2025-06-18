FROM ubuntu:24.04

# UTF-8 locale
RUN apt update && apt install -y locales && \
    locale-gen en_US en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
    
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# Outils système de base
RUN apt update && apt install -y \
    curl gnupg2 lsb-release ca-certificates \
    build-essential git wget unzip \
    python3-pip software-properties-common \
    net-tools iputils-ping

# Ajout des dépôts ROS 2 Jazzy
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | \
    gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu noble main" > /etc/apt/sources.list.d/ros2.list && \
    apt update

# Installation des paquets ROS 2 Jazzy + Gazebo Harmonic
RUN apt install -y \
    ros-jazzy-desktop \
    ros-jazzy-rqt* \
    ros-jazzy-rviz2 \
    ros-jazzy-ros-gz \
    ros-jazzy-ros-gz-sim \
    ros-jazzy-navigation2 \
    ros-jazzy-nav2-bringup \
    ros-jazzy-turtlesim \
    nano

# Installation de colcon et vcstool via pip
RUN pip3 install -U \
    colcon-common-extensions \
    vcstool --break-system-packages
    
# Supprime scipy system-wide et installe-le avec pip
RUN apt remove -y python3-scipy && \
    pip3 install scipy --break-system-packages && \
    pip3 install mediapipe opencv-python --break-system-packages


    
# À la fin de ton Dockerfile
RUN apt update && apt install -y \
  ros-jazzy-turtlebot3* \
  ros-jazzy-turtlebot3-gazebo \
  ros-jazzy-turtlebot3-navigation2
  
RUN apt update && apt install -y \
    libboost-all-dev \
    ros-jazzy-hardware-interface \
    ros-jazzy-controller-manager \
    ros-jazzy-ros2-controllers \
    ros-jazzy-tf-transformations \
    ros-jazzy-gz* \
    ros-jazzy-pal-statistics \
    ros-jazzy-moveit-* --no-install-recommends
  
# Source automatique de ROS 2
SHELL ["/bin/bash", "-c"]
RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
RUN echo 'export ROBOT_MODEL=om_x' >> ~/.bashrc

RUN source ~/.bashrc
CMD ["bash"]
