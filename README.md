## 🤖 OpenManipulator-X — Démo de Prise d’Objet (`take_ball`) dans Docker

Ce projet permet de simuler et piloter l’OpenManipulator-X dans un environnement Docker ROS 2 Jazzy + MoveIt + Gazebo, avec une démo automatisée de type "pick and place".

---

### 🐳 1. Construire l'image Docker

Dans le dossier contenant le `Dockerfile` :

```bash
docker build -t ros2-jazzy-noble .
```

---

### 🧱 2. Lancer le conteneur avec `docker-compose`

Dans le même dossier que `docker-compose.yml` :

```bash
docker-compose up -d
```

> Cela lance un conteneur nommé `ros2_jazzy_gui`.

---

### 🖥️ 3. Se connecter au terminal Docker

```bash
docker exec -it ros2_jazzy_gui bash
```

---

### 📦 4. Compiler le workspace (si pas déjà fait)

Dans le conteneur Docker :

```bash
cd /ros2_ws/ros_workshop_ws
colcon build
```

---

### 🧭 5. Lancer la démo `take_ball` (3 terminaux requis)

#### Dans **les 3 terminaux**, exécute d’abord :

```bash
source ros_workshop_ws/install/setup.sh
```

---

#### 🧱 Terminal 1 : Lancer Gazebo

```bash
ros2 launch open_manipulator_bringup gazebo.launch.py
```

---

#### 🧠 Terminal 2 : Lancer MoveIt + RViz (avec locale fixée)

```bash
LC_NUMERIC=en_US.UTF-8 ros2 launch open_manipulator_moveit_config moveit_core.launch.py
```

---

#### 🤖 Terminal 3 : Lancer le script de prise

```bash
ros2 run open_manipulator_playground take_ball
```

---

### ✅ Comportement attendu

* Le bras se déplace au-dessus de l’objet
* Il descend, ferme la pince
* Remonte avec l’objet
* Revient à une position initiale
* Ouvre la pince pour relâcher

---

### 📝 Notes

* Fonctionne en simulation dans Gazebo avec contrôleurs ROS 2
* Compatible avec l’exécution factice (`use_fake_hardware:=true` si besoin)
* RViz permet d’observer et ajuster le plan

---

