#!/usr/bin/env python3

import os
import cv2
import mediapipe as mp
import rclpy
from rclpy.node import Node
from rclpy.clock import Clock
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Twist, TwistStamped

# === Constantes de vitesse ===
LINEAR_SPEED = 0.2
ANGULAR_SPEED = 0.8

TURTLEBOT3_MODEL = os.environ.get('TURTLEBOT3_MODEL', 'burger')
ROS_DISTRO = os.environ.get('ROS_DISTRO', 'humble')


class FingerTeleop(Node):
    def __init__(self):
        super().__init__('finger_teleop')

        qos = QoSProfile(depth=10)
        if ROS_DISTRO == 'humble':
            self.pub = self.create_publisher(Twist, 'cmd_vel', qos)
        else:
            self.pub = self.create_publisher(TwistStamped, 'cmd_vel', qos)

        self.cap = cv2.VideoCapture(0)

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

        self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warn("Webcam inaccessible")
            return

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)

        hands_data = {}
        action = "Aucune main détectée"

        if result.multi_hand_landmarks and result.multi_handedness:
            for idx, hand_landmarks in enumerate(result.multi_hand_landmarks):
                hand_label = result.multi_handedness[idx].classification[0].label  # 'Left' or 'Right'
                lm = hand_landmarks.landmark
                is_palm_facing = lm[5].x < lm[17].x

                # Compter les doigts
                fingers = []
                if is_palm_facing:
                    fingers.append(1 if lm[4].x < lm[3].x else 0)  # Pouce
                else:
                    fingers.append(1 if lm[4].x > lm[3].x else 0)

                for tip in [8, 12, 16, 20]:
                    fingers.append(1 if lm[tip].y < lm[tip - 2].y else 0)

                hands_data[hand_label] = {
                    'fingers': sum(fingers),
                    'thumb_x': lm[4].x,
                    'thumb_ip_x': lm[3].x,
                    'landmarks': hand_landmarks
                }

                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        # Initialisation des vitesses
        lin = 0.0
        ang = 0.0

        # Logique de contrôle
        if 'Left' in hands_data and 'Right' in hands_data:
            left = hands_data['Left']
            right = hands_data['Right']

            if left['fingers'] == 5 and right['fingers'] == 5:
                # Orientation des pouces
                thumb_left_inward = left['thumb_x'] > left['thumb_ip_x']
                thumb_right_inward = right['thumb_x'] < right['thumb_ip_x']

                if thumb_left_inward and thumb_right_inward:
                    lin = LINEAR_SPEED
                    action = "Avancer"
                elif not thumb_left_inward and not thumb_right_inward:
                    lin = -LINEAR_SPEED
                    action = "Reculer"
                else:
                    action = "Pouces incohérents → Stop"

            elif left['fingers'] == 5 and right['fingers'] == 0:
                ang = ANGULAR_SPEED
                action = "Tourner à gauche"

            elif left['fingers'] == 0 and right['fingers'] == 5:
                ang = -ANGULAR_SPEED
                action = "Tourner à droite"

            elif left['fingers'] == 0 and right['fingers'] == 0:
                action = "Stop"

            else:
                action = "Gestes non reconnus → Stop"

        else:
            action = "Attente des deux mains"

        # Envoi commande
        if ROS_DISTRO == 'humble':
            twist = Twist()
            twist.linear.x = lin
            twist.angular.z = ang
            self.pub.publish(twist)
        else:
            twist_stamped = TwistStamped()
            twist_stamped.header.stamp = Clock().now().to_msg()
            twist_stamped.twist.linear.x = lin
            twist_stamped.twist.angular.z = ang
            self.pub.publish(twist_stamped)

        # Affichage
        cv2.putText(frame, f"Action: {action}", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 2)

        cv2.imshow("Finger Teleop", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.get_logger().info("Fermeture via 'q'")
            rclpy.shutdown()

    def destroy_node(self):
        self.cap.release()
        cv2.destroyAllWindows()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = FingerTeleop()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
