# 🚀 Utilisation du TurtleBot3 avec ROS 2

Ce guide explique comment connecter, mettre à jour et piloter un robot TurtleBot3 en ROS 2, étape par étape.

---

## 🧩 Prérequis

* Un PC avec **ROS 2 (Jazzy)** installé et configuré.
* Le TurtleBot3 configuré en modèle **Burger**.
* Le fichier `burger.yaml` modifiable (voir plus bas pour les chemins).
* Une map `.pgm` et `.yaml` déjà créée (ex: `map_workshop.pgm` et `map_workshop.yaml`).

---

## 🤖 Configuration du robot TurtleBot3

1. **Connexion au réseau**
   Connecte-toi **au même WiFi que le robot**, ici le hotspot WiFi nommé *"iPhone de Vini"*.

2. **Connexion SSH au robot**
   Allume le robot, puis connecte-toi en SSH :

   ```bash
   ssh ubuntu@172.20.10.5
   # Mot de passe : turtlebot
   ```

3. **Mettre à jour le firmware du contrôleur OPENCR** :

   ```bash
   export OPENCR_PORT=/dev/ttyACM0
   export OPENCR_MODEL=burger

   cd ~/opencr_update
   ./update.sh $OPENCR_PORT $OPENCR_MODEL.opencr
   ```

4. **Configurer le domaine ROS 2** :

   ```bash
   export ROS_DOMAIN_ID=127
   ```

5. **Lancer le robot (bringup)** :

   ```bash
   ros2 launch turtlebot3_bringup robot.launch.py use_sim_time:=False
   ```

   À ce stade, le lidar doit commencer à renvoyer des données.

✅ **C'est tout pour la configuration du robot !**

---

## 💻 Configuration du PC (ROS 2) Docker

1. **Assurez-vous d'avoir** :

   * ROS 2 installé
   * Le workspace `ros2_ws` configuré avec les bons packages
   * Les fichiers de map dans :
     `/ros2_ws/test/map_workshop.pgm`
     `/ros2_ws/test/map_workshop.yaml`

2. **Modification de `burger.yaml`** :

   Si vous utilisez Docker, modifiez ce fichier :

   ```bash
   /ros2_ws/ros_workshop_ws/src/turtlebot3/turtlebot3_navigation2/burger.yaml
   ```

   ➤ Modifiez notamment le paramètre suivant :

   ```yaml
   inflation_radius: 0.15  # ou autre valeur selon votre environnement
   ```

---

## 🧭 Lancer la navigation

Lancez la navigation du robot avec :

```bash
ros2 launch turtlebot3_navigation2 navigation2.launch.py \
  map:=/ros2_ws/test/map_workshop.yaml \
  use_sim_time:=False
```

> Remplacez le chemin du fichier `.yaml` si nécessaire.

Une fois lancé, l’interface de navigation s’ouvre. Vous pouvez définir des goals dans Rviz2 ou utiliser les outils CLI ROS 2.

---

## ✅ Résumé

| Étape | Action                               |
| ----- | ------------------------------------ |
| Robot | Connexion WiFi + SSH                 |
| Robot | Flash OPENCR + Bringup               |
| PC    | Fichiers de map + config YAML        |
| PC    | Lancement de `navigation2.launch.py` |

