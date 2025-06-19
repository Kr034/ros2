import rclpy
from rclpy.node import Node
import cv2
import mediapipe as mp
import time
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from geometry_msgs.msg import PoseStamped
from tf_transformations import quaternion_from_euler
from .points import GOAL_POSITIONS
import threading


class VideoStream:
    def __init__(self, src=0, width=640, height=480):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.stream.set(cv2.CAP_PROP_FPS, 30)

        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
        self.lock = threading.Lock()

    def start(self):
        threading.Thread(target=self.update, daemon=True).start()
        return self

    def update(self):
        while not self.stopped:
            (grabbed, frame) = self.stream.read()
            with self.lock:
                self.grabbed, self.frame = grabbed, frame

    def read(self):
        with self.lock:
            return self.grabbed, self.frame.copy()

    def stop(self):
        self.stopped = True
        self.stream.release()


class FingerNav(Node):
    def __init__(self):
        super().__init__('finger_nav')
        self.navigator = BasicNavigator()
        self.cap = VideoStream().start()

        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            model_complexity=0,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.last_sent = 0
        self.cooldown = 5  # seconds

        self.selected_goal = None
        self.validation_start = None
        self.status_message = "Montrez un chiffre pour choisir un point."
        self.goal_in_progress = False

        self.create_timer(0.05, self.timer_callback)  # 20Hz

    def timer_callback(self):
        # Vérifie si un goal est en cours
        if self.goal_in_progress:
            if self.navigator.isTaskComplete():
                result = self.navigator.getResult()
                if result == TaskResult.SUCCEEDED:
                    self.status_message = "Objectif atteint. Vous pouvez choisir un nouveau point."
                else:
                    self.status_message = "Échec de l'objectif ou annulé."
                self.goal_in_progress = False
            self.display_status()
            return

        grabbed, frame = self.cap.read()
        if not grabbed:
            return

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)

        count = -1
        if result.multi_hand_landmarks and result.multi_handedness:
            fingers_total = 0
            palm_oriented = True
            for idx, hand_landmarks in enumerate(result.multi_hand_landmarks):
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                lm = hand_landmarks.landmark
                handedness = result.multi_handedness[idx].classification[0].label

                is_palm = lm[5].x < lm[17].x if handedness == 'Right' else lm[5].x > lm[17].x
                if not is_palm:
                    palm_oriented = False

                thumb_extended = (lm[4].x < lm[3].x) if handedness == 'Right' else (lm[4].x > lm[3].x)
                fingers = [1 if lm[i].y < lm[i - 2].y else 0 for i in [8, 12, 16, 20]]
                fingers.insert(0, 1 if thumb_extended else 0)
                fingers_total += sum(fingers)

            count = fingers_total
            cv2.putText(frame, f"Doigts total: {count}", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 0), 2)

            if count in GOAL_POSITIONS:
                if self.selected_goal != count:
                    if not hasattr(self, 'selection_start') or self.selection_start is None:
                        self.selection_start = time.time()
                    elif time.time() - self.selection_start >= 1.0:
                        self.selected_goal = count
                        self.validation_start = None
                        self.status_message = f"Chiffre {count} ok. Maintenez 10 doigts (paumes visibles) pour valider."
                        self.get_logger().info(self.status_message)
                        self.selection_start = None
                else:
                    self.selection_start = None


            if self.selected_goal is not None:
                if count == 10 and palm_oriented:
                    if self.validation_start is None:
                        self.validation_start = time.time()
                        self.status_message = "Validation en cours..."
                    elif time.time() - self.validation_start >= 5:
                        x, y, theta = GOAL_POSITIONS[self.selected_goal]
                        self.status_message = f"Objectif  {self.selected_goal} . Le robot se déplace..."
                        self.send_goal(x, y, theta)
                        self.last_sent = time.time()
                        self.goal_in_progress = True
                        self.selected_goal = None
                        self.validation_start = None
                        self.get_logger().info(self.status_message)
                else:
                    self.validation_start = None
                    self.status_message = f"Chiffre {self.selected_goal} en attente de validation (10 doigts )"
        else:
            self.validation_start = None
            if self.selected_goal is None:
                self.status_message = "Montrez un chiffre pour choisir un point."
            else:
                self.status_message = f"Chiffre {self.selected_goal} en attente de validation (10 doigts + paumes visibles)"

        cv2.putText(frame, self.status_message, (30, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)

        cv2.imshow("FingerNav", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.cap.stop()
            cv2.destroyAllWindows()
            rclpy.shutdown()

    def display_status(self):
        grabbed, frame = self.cap.read()
        if not grabbed:
            return
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, self.status_message, (30, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)
        cv2.imshow("FingerNav", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.cap.stop()
            cv2.destroyAllWindows()
            rclpy.shutdown()

    def send_goal(self, x, y, theta):
        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.header.stamp = self.get_clock().now().to_msg()
        goal.pose.position.x = x
        goal.pose.position.y = y
        q = quaternion_from_euler(0, 0, theta)
        goal.pose.orientation.x = q[0]
        goal.pose.orientation.y = q[1]
        goal.pose.orientation.z = q[2]
        goal.pose.orientation.w = q[3]

        self.get_logger().info(f"Envoi vers : x={x:.2f}, y={y:.2f}, θ={theta:.2f} rad")
        self.navigator.goToPose(goal)


def main():
    rclpy.init()
    node = FingerNav()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.cap.stop()
        cv2.destroyAllWindows()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
