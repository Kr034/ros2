## 🐳 ROS 2 + TurtleBot3 + OpenManipulator (Docker)

### ✅ Prérequis

1. Avoir `docker` et `docker-compose` installés
2. Exécuter **avant** toute commande Docker :

   ```bash
   xhost +local:docker
   ```

---

### 🚀 Lancer le conteneur Docker

1. **Build de l’image Docker :**

   ```bash
   docker build -t ros2-jazzy-noble .
   ```

2. **Lancer le conteneur :**

   ```bash
   docker-compose up -d
   ```

3. **Se connecter au terminal du conteneur :**

   ```bash
   docker exec -it ros2_jazzy_gui bash
   ```

---

### ⚙️ Initialisation du workspace ROS 2

Une fois dans le conteneur :

```bash
bash /ros2_ws/script.sh
```

---

### 🔁 Utilisation classique (3 terminaux requis)

Avant toute chose dans **chaque terminal** :

```bash
source /ros2_ws/ros_workshop_ws/install/setup.bash
```

Ensuite :

1. **Terminal 1 :** Gazebo simulation

   ```bash
   ros2 launch open_manipulator_bringup gazebo.launch.py
   ```

2. **Terminal 2 :** MoveIt2 avec OM-X

   ```bash
   LC_NUMERIC=en_US.UTF-8 ros2 launch open_manipulator_moveit_config moveit_core.launch.py
   ```

3. **Terminal 3 :** Exécution du mouvement

   ```bash
   ros2 run open_manipulator_playground take_ball
   ```

---
