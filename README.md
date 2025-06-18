## 📘 README.md — Mise en route avec Docker (ROS 2 Jazzy)

Ce projet contient un environnement Docker prêt à l'emploi pour manipuler **TurtleBot3** et **OpenManipulator-X** dans **ROS 2 Jazzy**, avec MoveIt, Gazebo, RViz, et des démos personnalisées.

---

### ⚠️ Prérequis

* Docker installé
* Docker Compose installé
* Un affichage X11 disponible (nécessaire pour RViz et Gazebo)
* Ubuntu/Linux (testé sur Arch et Ubuntu 22.04)

---

### 🧪 Étapes de préparation (sur votre PC)

```bash
# 1. Autoriser l'affichage X11 au container Docker
sudo xhost +local:docker

# 2. Créer un dossier ros2_ws dans votre HOME (si pas déjà fait)
mkdir -p ~/ros2_ws

# 3. Cloner ce dépôt et copier les fichiers de configuration
git clone https://github.com/Kr034/ros2.git
cd ros2
cp -r ros2_ws/* ~/ros2_ws/
```

---

### 🐳 Construction & lancement du conteneur Docker

```bash
# 4. Construire l'image Docker
docker build -t ros2-jazzy-noble .

# 5. Lancer le conteneur avec Docker Compose
docker-compose up -d

# 6. Accéder au shell du container
docker exec -it ros2_jazzy_gui bash
```

---

### 📜 Initialisation du workspace ROS (dans le conteneur)

Une fois dans le terminal Docker, lance ce script pour configurer l’environnement complet :

```bash
chmod +x /ros2_ws/script.sh
/ros2_ws/script.sh
```

Ce script :

* Clone les dépôts nécessaires (TurtleBot3, OpenManipulator, etc.)
* Remplace les sources du package `open_manipulator_playground` avec `/ros2_ws/take_ball_src`
* Compile avec `colcon build`
* Configure les variables d’environnement dans `~/.bashrc`

---

### 🚀 Lancer la simulation

Ouvre **3 terminaux Docker** (ou utilise `tmux`/`tilix`) et exécute :

**Terminal 1 : Gazebo**

```bash
source ros_workshop_ws/install/setup.sh
ros2 launch open_manipulator_bringup gazebo.launch.py
```

**Terminal 2 : MoveIt**

```bash
docker-compose up -d
docker exec -it ros2_jazzy_gui bash
source ros_workshop_ws/install/setup.sh
LC_NUMERIC=en_US.UTF-8 ros2 launch open_manipulator_moveit_config moveit_core.launch.py
```

**Terminal 3 : Démo de manipulation**

```bash
docker-compose up -d
docker exec -it ros2_jazzy_gui bash
source ros_workshop_ws/install/setup.sh
ros2 run open_manipulator_playground take_ball
```

---

### 📦 Contenu

* `ros2_ws/`: environnement ROS 2 avec packages clonés + sources personnalisées
* `take_ball_src/`: contient un `take_ball.cpp` personnalisé pour manipuler un objet
* `script.sh`: script d’installation automatique dans le conteneur
