## 📘 README.md — Mise en route avec Docker (ROS 2 Jazzy)

Ce projet contient un environnement Docker prêt à l'emploi pour manipuler **TurtleBot3** et **OpenManipulator-X** dans **ROS 2 Jazzy**, avec MoveIt, Gazebo, RViz, et des démos personnalisées.

---

### 📦 Contenu

Ce projet ROS 2 combine plusieurs modules pour démontrer une intégration complète entre perception, manipulation et navigation :

- 🦾 **open_manipulator_playground** : Script C++ MoveIt 2 pour récupérer une balle avec le bras OpenManipulator-X.
- 🧠 **finger_nav** : Interface gestuelle en Python utilisant MediaPipe + OpenCV, permettant de sélectionner un objectif avec les doigts (1 à 6), valider avec 10 doigts (paumes visibles), puis :
  - Exécuter la prise d'objet avec le bras ;
  - Envoyer le TurtleBot vers un point prédéfini.
- 🤖 **turtlebot3 + navigation2** : Navigation autonome (Nav2) dans un environnement Gazebo simulé.
- 🧩 **MoveIt 2** : Planification et exécution des trajectoires pour le bras manipulateur.
- 🌍 **Gazebo** : Simulation du robot complet (TurtleBot + bras) dans un environnement 3D.

L’interface est conçue pour fonctionner **sans clavier ni souris**, avec uniquement les gestes pour piloter la prise d’objet et le déplacement.

---

```bash
🖐️  Chiffre (1 à 6)    ➜  Sélection d’un point
🖐️🖐️ 10 doigts (paumes) ➜  Validation et déclenchement
🦾  Bras → prend la balle
🤖  Robot mobile → navigue automatiquement
````

### ⚠️ Prérequis

* Docker installé
* Docker Compose installé
* Un affichage X11 disponible (nécessaire pour RViz et Gazebo)
* Ubuntu/Linux (testé sur Arch et Ubuntu 22.04)

---
### Connexion au robot

Avant d’utiliser la webcam, vous devez être connecté au robot et avoir lancé la pile de navigation.
Veuillez suivre les instructions détaillées dans [`nav-turtle-READ.md`](https://github.com/Kr034/ros2/blob/main/nav-turtle-READ.md).

Cela inclut :

* Le lancement de Gazebo ou de la robotique réelle
* Le lancement de `navigation2` et du bringup TurtleBot3

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
sudo usermod -aG docker $USER
exec su -l $USER
```

```bash

# 4. Construire l'image Docker (pensez a retourner dans le répertoire ros2 du git)
docker build -t ros2-jazzy-noble .

# 5. Lancer xhost
xhost +local:docker
# 6. Lancer le conteneur avec Docker Compose
docker-compose up -d

# 7. Accéder au shell du container
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


## 🎬 End-to-end demo : bras + navigation + interface gestuelle - Présentation le 20 juin 2025

> Prérequis :  
> * L’image Docker est déjà construite (`docker build -t ros2-jazzy-noble .`)  
> * Le conteneur est lancé via **docker-compose** (`docker-compose up -d`)  
> * Votre utilisateur est dans le groupe *docker* :

```bash
sudo usermod -aG docker $USER
exec su -l $USER        # recharge le shell avec les droits
````

---

### 1 . Autoriser l’affichage X11/Wayland

```bash
xhost +local:docker      # à exécuter une seule fois sur l’hôte
```

---

### 2 . Ouvrir trois terminaux dans le conteneur

```bash
docker exec -it ros2_jazzy_gui bash
source ros_workshop_ws/install/setup.sh
```

Répétez la commande dans **quatre** fenêtres séparées ; chacune exécutera un rôle différent.

---

### 3 . Lancer la simulation

| Terminal | Commande                                                                                  | Rôle                                                                 |
| -------- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **T1**   | `ros2 launch open_manipulator_bringup gazebo.launch.py`                                   | Gazebo : monde + OpenManipulator-X + TurtleBot3                      |
| **T2**   | `LC_NUMERIC=en_US.UTF-8 ros2 launch open_manipulator_moveit_config moveit_core.launch.py` | MoveIt 2 : planification bras + gripper                              |
| **T3**   | `ros2 launch turtlebot3_navigation2 navigation2.launch.py   map:=/ros2_ws/test/map_workshop.yaml   use_sim_time:=False` | Rviz : Interface pour configurer la navigation et la position du robot |
| **T4**   | `ros2 launch finger_nav finger_nav.launch.py`                                             | Interface gestuelle (MediaPipe) ⇒ prise de balle + navigation mobile |


---

### 4 . Utilisation

| Geste                                                                                                      | Action                                          |
| ---------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| **Main(s) montrant un chiffre** (paume visible)                                                            | Sélection d’un point d’intérêt (chiffres 1 → 6) |
| **10 doigts levés** (paumes visibles) pendant ≥ 5 s                                                        | Validation de la sélection                      |
| Le bras récupère la balle (action *take\_ball*) puis le TurtleBot se rend automatiquement au point validé. |                                                 |

*Note : tant que le bras ou le robot sont en mouvement, l’interface ignore les nouveaux gestes et affiche l’état courant dans la fenêtre vidéo.*

---

### 5 . Arrêt

Dans chaque terminal :

```bash
Ctrl-C
exit
```

Puis arrêtez le conteneur :

```bash
docker-compose down
```

---

## 📷 Utilisation de la webcam avec ROS 2 - Bonus de la présentation

### 1. Connexion au robot, si vous effectué avez déjà tout configuré, il faut juste aller à la partie 2

Avant d’utiliser la webcam, vous devez être connecté au robot et avoir lancé la pile de navigation.
Veuillez suivre les instructions détaillées dans [`nav-turtle-READ.md`](https://github.com/Kr034/ros2/blob/main/nav-turtle-READ.md).

Cela inclut :

* Le lancement de Gazebo ou de la robotique réelle
* Le lancement de `navigation2` et du bringup TurtleBot3

---

### 2. Lancer la détection de doigts via la webcam

Une fois le robot prêt, exécutez le module de détection de doigts basé sur Mediapipe et OpenCV.
Ce module détecte les mains via la webcam et publie sur un topic ROS le **nombre total de doigts levés** (main gauche + main droite).

#### ✅ Lancement a partir du terminal docker ROS (voir plus haut)

```bash
source ros_workshop_ws/install/setup.sh
ros2 run turtlebot3_webcam talker
```

#### 🧠 Fonctionnalité

* Affichage en temps réel du flux webcam avec les **landmarks des mains** dessinés.
* Calcule **la somme des doigts levés** (main gauche + droite).
* **Publication uniquement en cas de changement** sur un topic ROS.
* Commandes de contrôle gestuel du robot :

| Geste détecté                                                   | Action ROS     |
| --------------------------------------------------------------- | -------------- |
| 👋👋 **Deux mains ouvertes, paumes visibles**                   | Avancer        |
| ✊✊ **Deux mains retournées, paumes non visibles**               | Reculer        |
| ✊👋 **Main gauche fermée, main droite ouverte (paume visible)** | Aller à droite |
| 👋✊ **Main droite fermée, main gauche ouverte (paume visible)** | Aller à gauche |

---

### 🛠 Prérequis

* Une webcam fonctionnelle, accessible depuis le conteneur Docker.
* Les paquets Python suivants doivent être installés dans l’environnement Docker :

  * `mediapipe`
  * `opencv-python`
* Ces dépendances sont installées dans l’image Docker fournie dans ce projet.
  
---


### 🚀 Lancer la simulation du mouvement du bras manipulateur 

Ouvre **3 terminaux Docker** (ou utilise `tmux`/`tilix`) et exécute :

**Terminal 1 : Gazebo**

```bash
source ros_workshop_ws/install/setup.sh
ros2 launch open_manipulator_bringup gazebo.launch.py
```

**Terminal 2 : MoveIt**

```bash
sudo usermod -aG docker $USER
exec su -l $USER
docker exec -it ros2_jazzy_gui bash
source ros_workshop_ws/install/setup.sh
LC_NUMERIC=en_US.UTF-8 ros2 launch open_manipulator_moveit_config moveit_core.launch.py
```

**Terminal 3 : Démo de manipulation**

```bash
sudo usermod -aG docker $USER
exec su -l $USER
docker exec -it ros2_jazzy_gui bash
source ros_workshop_ws/install/setup.sh
ros2 run open_manipulator_playground take_ball
```

---
