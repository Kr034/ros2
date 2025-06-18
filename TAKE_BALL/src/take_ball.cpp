#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.hpp>
#include <geometry_msgs/msg/pose.hpp>
#include <thread>
#include <chrono>

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<rclcpp::Node>(
    "take_ball_node",
    rclcpp::NodeOptions().automatically_declare_parameters_from_overrides(true));

  auto logger = rclcpp::get_logger("take_ball");

  using moveit::planning_interface::MoveGroupInterface;

  // Groupes
  MoveGroupInterface arm(node, "arm");
  MoveGroupInterface gripper(node, "gripper");

  // Paramètres de planification
  arm.setGoalPositionTolerance(0.005);
  arm.setGoalOrientationTolerance(0.01);
  arm.setPlanningTime(5.0);

  // Position au-dessus de l’objet
  geometry_msgs::msg::Pose pre_grasp_pose;
  pre_grasp_pose.position.x = 0.20;
  pre_grasp_pose.position.y = 0.0;
  pre_grasp_pose.position.z = 0.20;
  pre_grasp_pose.orientation.w = 1.0;

  // Position exacte à saisir
  geometry_msgs::msg::Pose grasp_pose = pre_grasp_pose;
  grasp_pose.position.z = 0.12;

  // Aller en pré-approche
  arm.setPoseTarget(pre_grasp_pose);
  if (!arm.move()) {
    RCLCPP_ERROR(logger, "Échec mouvement pré-grasp");
    return 1;
  }

  std::this_thread::sleep_for(std::chrono::seconds(1));

  // Descendre vers l’objet
  arm.setPoseTarget(grasp_pose);
  if (!arm.move()) {
    RCLCPP_ERROR(logger, "Échec descente vers l’objet");
    return 1;
  }

  std::this_thread::sleep_for(std::chrono::seconds(1));

  // Fermer la pince
  gripper.setNamedTarget("close");
  if (gripper.move()) {
    RCLCPP_INFO(logger, "Gripper fermé");
  } else {
    RCLCPP_WARN(logger, "Échec fermeture gripper");
  }

  std::this_thread::sleep_for(std::chrono::seconds(1));

  // Remonter l’objet
  arm.setPoseTarget(pre_grasp_pose);
  arm.move();

  std::this_thread::sleep_for(std::chrono::seconds(1));

 std::vector<double> home_joint_values = { 
    -170.0 * M_PI / 180.0,  // joint1
    0.0,                    // joint2
    0.0,                    // joint3
    0.0                     // joint4
  };
  arm.setJointValueTarget(home_joint_values);
  if (arm.move()) {
    RCLCPP_INFO(logger, "Retour position de départ réussi");
  }

  std::this_thread::sleep_for(std::chrono::seconds(1));

  // Ouvrir la pince
  gripper.setNamedTarget("open");
  gripper.move();

  rclcpp::shutdown();
  return 0;
}
