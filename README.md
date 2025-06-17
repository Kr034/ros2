---

## 🤖 OpenManipulator-X — Démo de Prise avec `take_ball` (Docker)

Ce projet lance une simulation Gazebo + MoveIt dans un conteneur Docker, permettant de planifier et exécuter un mouvement de type "prise d’objet" avec l’OpenManipulator-X.

---

### 🐳 Pré-requis

* Docker avec `ros2-jazzy` + Gazebo + MoveIt configurés
* Le workspace `ros_workshop_ws` compilé dans Docker (`colcon build`)
* X11 forwarding ou Wayland configuré si RViz ou Gazebo est utilisé

---

### 🧭 Étapes de lancement (dans 3 terminaux Docker)

#### 🛠 1. **Dans les 3 terminaux :** source de l’environnement

```bash
source ros_workshop_ws/install/setup.sh
```

---

#### 🧱 2. **Terminal 1** – Simulation Gazebo

Lance le monde avec le robot simulé :

```bash
ros2 launch open_manipulator_bringup gazebo.launch.py
```

---

#### 🎮 3. **Terminal 2** – MoveIt + RViz

⚠️ Fixe la locale pour éviter les erreurs de parsing de floats :

```bash
LC_NUMERIC=en_US.UTF-8 ros2 launch open_manipulator_moveit_config moveit_core.launch.py
```

---

#### 🧠 4. **Terminal 3** – Exécution automatique de la prise

```bash
ros2 run open_manipulator_playground take_ball
```

---

### 📈 Résultat attendu

* Le bras se déplace vers une position cartésienne prédéfinie (au-dessus de l’objet)
* Descente vers l’objet
* Fermeture de la pince
* Remontée
* Retour à une position de départ
* Ouverture du gripper

---

### 🧩 Remarques

* Vérifie que les `controllers` sont actifs dans Gazebo (`ros2 control list_controllers`)
* Le fichier `take_ball.cpp` peut être ajusté pour tester d’autres poses ou séquences
* Fonctionne avec ou sans exécution réelle (fake ou Gazebo)

