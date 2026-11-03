# uArm-Swift-Pro-Kinematics-Simulation
# Modélisation Cinématique et Simulation du uArm Swift Pro

Ce dépôt documente l'analyse mathématique, la modélisation cinématique et la simulation du bras robotique 4-DDL **uArm Swift Pro**. 

**Objectifs du projet :**
- Établir le modèle cinématique direct (MCD) à l'aide de la convention de Denavit-Hartenberg (D-H).
- Détailler les calculs de la matrice de transformation homogène pour extraire la position spatiale de la pince.
- Simuler le comportement du manipulateur et l'exécution du code (Python / CoppeliaSim).

**Architecture et Outils :**
- **CoppeliaSim** : Modélisation de la scène et simulation physique.
- **Python** : Implémentation des calculs matriciels et contrôle.
- **Documentation uArm** : Paramétrage basé sur le guide développeur officiel (dimensions et limites articulaires).

# Modélisation Cinématique et Simulation du uArm Swift Pro

Ce projet détaille l'analyse cinématique, la modélisation mathématique et la simulation du bras manipulateur uArm Swift Pro (4 degrés de liberté). 

## 1. Arborescence et Étapes du Projet

Voici les étapes méthodologiques suivies pour la réalisation de ce projet :
1. **Analyse cinématique** : Étude de la structure du robot.
2. **Définition des repères** : Placement des repères cartésiens pour les 4 degrés de liberté (DDL).
3. **Tableau de Denavit-Hartenberg (D-H)** : Extraction des paramètres géométriques.
4. **Calcul du MGD** : Établissement du Modèle Géométrique Direct via les matrices homogènes.
5. **Simulation** : Interfaçage entre Python et CoppeliaSim.

## 2. Analyse Cinématique et Paramètres D-H

Pour établir le modèle cinématique, nous utilisons les 4 paramètres de Denavit-Hartenberg pour passer du repère i-1 au repère i :
* theta_i : Rotation autour de l'axe Z. Sur le uArm, c'est la variable articulaire (l'angle du moteur qui varie quand le bras bouge, correspondant à la commande moteur). C'est l'angle dont le moteur tourne autour de son axe Z pour que son axe X pointe vers la prochaine articulation.
* d_i : Translation le long de l'axe Z. C'est la distance à glisser le long de l'axe Z pour arriver à la hauteur du prochain moteur.
* a_i : Translation le long de l'axe X. C'est la longueur physique du bras à parcourir le long de l'axe X pour atteindre le nouveau repère.
* alpha_i : Rotation autour de l'axe X. C'est l'angle de torsion du poignet autour de ce bras pour que l'ancien axe Z s'aligne sur le nouvel axe Z.

### Limites des moteurs et Choix des Angles
Selon le document "uArm Swift Pro_Developer Guide v1.0.6.pdf", les limites de rotation des moteurs sont les suivantes :
* **Base** : 0° to 180° (Choix justifié par la protection du câblage interne).
* **Épaule** : 0° to 130° (Pour éviter que les tiges tapent contre le châssis ou elles-mêmes, éviter le verrouillage mécanique, et assurer l'équilibre et la stabilité du bras).
* **Coude** : 0° to 106° (Mêmes raisons que pour l'épaule).
* **Pince** : 0° to 180° (Limite technologique du servomoteur).

*(Note : Dans le code, ces limites peuvent être gérées avec des angles symétriques, par exemple de -90° à +90° au lieu de 0° à 180°.*

## 3. Placement des Repères et Tableau D-H

| Articulation i | theta_i (Rot Z) | d_i (Trans Z) | a_i (Trans X) | alpha_i (Rot X) |
| :--- | :--- | :--- | :--- | :--- |
| **1 (Base - Épaule)** | theta_1 | d_1 (hauteur socle) | 0 | pi/2 |
| **2 (Épaule - Coude)** | theta_2 | 0 | a_2 (long. bras) | 0 |
| **3 (Coude - Poignet)** | theta_3 | 0 | a_3 (avant-bras) | -\pi/2 |
| **4 (Poignet - Pince)** | theta_4 | d_4 (hauteur pince) | 0 | 0 |

## 4. Matrices de Transformation Homogène et MGD

La matrice de transformation homogène permet à l'ordinateur de calculer simultanément la position et l'orientation d'une articulation par rapport à la précédente. La formule de composition est :
$$\text{Repère}_{i} = Rot_z(\theta) \times Trans_z(d) \times Trans_x(a) \times Rot_x(\alpha)$$

**Formule universelle de D-H :**
$$
T_{i}^{i-1} = \begin{bmatrix} 
\cos\theta_i & -\sin\theta_i\cos\alpha_i & \sin\theta_i\sin\alpha_i & a_i\cos\theta_i \\ 
\sin\theta_i & \cos\theta_i\cos\alpha_i & -\cos\theta_i\sin\alpha_i & a_i\sin\theta_i \\ 
0 & \sin\alpha_i & \cos\alpha_i & d_i \\ 
0 & 0 & 0 & 1 
\end{bmatrix}
$$

### Calcul des Matrices intermédiaires

- **Base $\to$ Épaule ($T_{01}$)** :
$$
T_{01} = \begin{bmatrix} 
\cos\theta_1 & 0 & \sin\theta_1 & 0 \\ 
\sin\theta_1 & 0 & -\cos\theta_1 & 0 \\ 
0 & 1 & 0 & d_1 \\ 
0 & 0 & 0 & 1 
\end{bmatrix}
$$

- **Épaule $\to$ Coude ($T_{12}$)** :
$$
T_{12} = \begin{bmatrix} 
\cos\theta_2 & -\sin\theta_2 & 0 & a_2\cos\theta_2 \\ 
\sin\theta_2 & \cos\theta_2 & 0 & a_2\sin\theta_2 \\ 
0 & 0 & 1 & 0 \\ 
0 & 0 & 0 & 1 
\end{bmatrix}
$$

- **Coude $\to$ Poignet ($T_{23}$)** :
$$
T_{23} = \begin{bmatrix} 
\cos\theta_3 & 0 & -\sin\theta_3 & a_3\cos\theta_3 \\ 
\sin\theta_3 & 0 & \cos\theta_3 & a_3\sin\theta_3 \\ 
0 & -1 & 0 & 0 \\ 
0 & 0 & 0 & 1 
\end{bmatrix}
$$

- **Poignet $\to$ Pince ($T_{34}$)** :
$$
T_{34} = \begin{bmatrix} 
\cos\theta_4 & -\sin\theta_4 & 0 & 0 \\ 
\sin\theta_4 & \cos\theta_4 & 0 & 0 \\ 
0 & 0 & 1 & d_4 \\ 
0 & 0 & 0 & 1 
\end{bmatrix}
$$

**Équation finale du MGD :**
$$T_{04} = T_{01} \times T_{12} \times T_{23} \times T_{34}$$

### Comment lire la Matrice Finale ?
Le produit de ces matrices génère une matrice 4x4. Elle est purement mathématique et se lit ainsi :
- **Le bloc 3x3 en haut à gauche** : Représente la matrice de rotation (l'orientation de la pince dans l'espace).
- **La 4ème colonne (les 3 premières lignes)** : Représente le vecteur de translation $(X, Y, Z)$, c'est-à-dire la position exacte de la pince par rapport à la base.

## 5. Interfaçage et Communication : Python & CoppeliaSim

Pour lier le Modèle Géométrique Direct à la simulation 3D, nous utilisons un script Python communiquant avec CoppeliaSim via la **ZeroMQ Remote API**. Cela permet de lire les positions actuelles des moteurs dans la simulation et d'envoyer les résultats matriciels.

**Extrait du code Python (Calcul du MGD au repos) :**

```python
import numpy as np
from math import cos, sin, radians

def D_H(theta, d, a, alpha):
    theta = radians(theta)
    alpha = radians(alpha)
    matrice_D_H = np.array([
        [cos(theta), -sin(theta)*cos(alpha), sin(theta)*sin(alpha), a*cos(theta)],
        [sin(theta),  cos(theta)*cos(alpha), -cos(theta)*sin(alpha), a*sin(theta)],
        [0,          sin(alpha),            cos(alpha),            d],
        [0,          0,                     0,                     1]
    ])
    return matrice_D_H

def MGD(theta1, theta2, theta3, theta4):
    d1 = 136.6  # Hauteur ajustée
    a2 = 142.07
    a3 = 158.8
    d4 = 38.0

    T01 = D_H(theta1, d1, 0, 90)
    T12 = D_H(theta2, 0, a2, 0)
    T23 = D_H(theta3, 0, a3, -90)
    T34 = D_H(theta4, d4, 0, 0)

    matrice_homogene = T01 @ T12 @ T23 @ T34
    position_pince = matrice_homogene[0:3, 3]
    return np.round(matrice_homogene, 2), np.round(position_pince, 2)

matrice_finale, position = MGD(0, 0, 0, 0)

print("Matrice finale :\n", matrice_finale)
print("Position de la pince :\n", position)
