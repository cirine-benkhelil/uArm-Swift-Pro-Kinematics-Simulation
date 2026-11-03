# Modélisation Cinématique et Simulation du uArm Swift Pro

Ce dépôt documente l'analyse mathématique, la modélisation cinématique et la simulation du bras robotique 4-DDL **uArm Swift Pro**.

## Objectifs du projet

- Établir le **modèle géométrique direct (MGD)** à l'aide de la convention de Denavit-Hartenberg (D-H).
- Détailler le calcul des matrices de transformation homogène pour extraire la position spatiale de la pince.
- Simuler le comportement du manipulateur (Python / CoppeliaSim).

## Architecture et outils

| Outil | Rôle |
| :--- | :--- |
| **CoppeliaSim** | Modélisation de la scène et simulation physique |
| **Python** | Implémentation des calculs matriciels et contrôle |
| **Documentation uArm** | Paramétrage basé sur le guide développeur officiel (dimensions et limites articulaires) |

## Structure du dépôt

```text
uArm-Swift-Pro-Kinematics-Simulation/
├── README.md
├── requirements.txt
├── Docs/
│   ├── CALCULS.md          (détail des calculs matriciels)
│   ├── INTERFACAGE.md   (liaison VS Code ↔ CoppeliaSim)
|   ├── uArm swift pro dev guide ( guide officiel détaillé du robot )
|   ├── Reperes uarm ( details sur le choix des reperes de chacune des articulations )
|   └── mechanisme du pivot ( explication mecanique du pivot qui controle le bras ) 
└── src/
    ├── mgd.py              (calcul du MGD)
    └── test_connexion.py   (test de liaison avec CoppeliaSim)
```

---

## 1. Étapes du projet

1. **Analyse cinématique** : étude de la structure du robot.
2. **Définition des repères** : placement des repères cartésiens pour les 4 degrés de liberté (DDL).
3. **Tableau de Denavit-Hartenberg (D-H)** : extraction des paramètres géométriques.
4. **Calcul du MGD** : établissement du modèle géométrique direct via les matrices homogènes.
5. **Simulation** : interfaçage entre Python et CoppeliaSim.

---

## 2. Analyse cinématique et paramètres D-H

Pour passer du repère $i-1$ au repère $i$, on utilise 4 paramètres de Denavit-Hartenberg :

| Paramètre | Mouvement | Signification |
| :---: | :--- | :--- |
| $\theta_i$ | Rotation autour de $Z$ | Variable articulaire : angle du moteur (commande moteur). Il fait tourner le bras pour que l'axe $X$ pointe vers la prochaine articulation. |
| $d_i$ | Translation le long de $Z$ | Distance à parcourir le long de l'axe $Z$ pour arriver à la hauteur du prochain moteur. |
| $a_i$ | Translation le long de $X$ | Longueur physique du bras à parcourir le long de l'axe $X$ pour atteindre le nouveau repère. |
| $\alpha_i$ | Rotation autour de $X$ | Angle de torsion pour que l'ancien axe $Z$ s'aligne sur le nouvel axe $Z$. |

### Limites des moteurs et choix des angles

Selon le document *uArm Swift Pro_Developer Guide v1.0.6.pdf*, les limites de rotation sont :

| Articulation | Plage | Justification |
| :--- | :---: | :--- |
| **Base** | 0° à 180° | Protection du câblage interne |
| **Épaule** | 0° à 130° | Éviter que les tiges ne tapent contre le châssis ou entre elles, éviter le verrouillage mécanique, assurer l'équilibre et la stabilité du bras |
| **Coude** | 0° à 106° | Mêmes raisons que pour l'épaule |
| **Pince** | 0° à 180° | Limite technologique du servomoteur |

> **Note :** dans le code, ces limites peuvent être gérées avec des angles symétriques, par exemple de -90° à +90° au lieu de 0° à 180°.

---

## 3. Placement des repères et tableau D-H

| Articulation $i$ | $\theta_i$ (Rot Z) | $d_i$ (Trans Z) | $a_i$ (Trans X) | $\alpha_i$ (Rot X) |
| :--- | :---: | :---: | :---: | :---: |
| **1** (Base → Épaule) | $\theta_1$ | $d_1$ (hauteur socle) | $0$ | $\pi/2$ |
| **2** (Épaule → Coude) | $\theta_2$ | $0$ | $a_2$ (longueur bras) | $0$ |
| **3** (Coude → Poignet) | $\theta_3$ | $0$ | $a_3$ (avant-bras) | $-\pi/2$ |
| **4** (Poignet → Pince) | $\theta_4$ | $d_4$ (hauteur pince) | $0$ | $0$ |

Valeurs numériques utilisées (en mm) : $d_1 = 136.6$, $a_2 = 142.07$, $a_3 = 158.8$, $d_4 = 0$ (mettre $38$ pour inclure la pince).

---

## 4. Matrices de transformation homogène et MGD

La matrice de transformation homogène permet de calculer simultanément la position et l'orientation d'une articulation par rapport à la précédente :

$$
T_{i-1}^{\,i} = Rot_z(\theta_i) \times Trans_z(d_i) \times Trans_x(a_i) \times Rot_x(\alpha_i)
$$

### Formule universelle de D-H

$$
T_{i-1}^{\,i} =
\begin{bmatrix}
\cos\theta_i & -\sin\theta_i\cos\alpha_i & \sin\theta_i\sin\alpha_i & a_i\cos\theta_i \\
\sin\theta_i & \cos\theta_i\cos\alpha_i & -\cos\theta_i\sin\alpha_i & a_i\sin\theta_i \\
0 & \sin\alpha_i & \cos\alpha_i & d_i \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

### Matrices intermédiaires

**Base → Épaule ($T_{01}$)**, avec $\alpha_1 = \pi/2$ :

$$
T_{01} =
\begin{bmatrix}
\cos\theta_1 & 0 & \sin\theta_1 & 0 \\
\sin\theta_1 & 0 & -\cos\theta_1 & 0 \\
0 & 1 & 0 & d_1 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

**Épaule → Coude ($T_{12}$)**, avec $\alpha_2 = 0$ :

$$
T_{12} =
\begin{bmatrix}
\cos\theta_2 & -\sin\theta_2 & 0 & a_2\cos\theta_2 \\
\sin\theta_2 & \cos\theta_2 & 0 & a_2\sin\theta_2 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

**Coude → Poignet ($T_{23}$)**, avec $\alpha_3 = -\pi/2$ :

$$
T_{23} =
\begin{bmatrix}
\cos\theta_3 & 0 & -\sin\theta_3 & a_3\cos\theta_3 \\
\sin\theta_3 & 0 & \cos\theta_3 & a_3\sin\theta_3 \\
0 & -1 & 0 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

**Poignet → Pince ($T_{34}$)**, avec $\alpha_4 = 0$ :

$$
T_{34} =
\begin{bmatrix}
\cos\theta_4 & -\sin\theta_4 & 0 & 0 \\
\sin\theta_4 & \cos\theta_4 & 0 & 0 \\
0 & 0 & 1 & d_4 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

### Équation finale du MGD

$$
T_{04} = T_{01} \times T_{12} \times T_{23} \times T_{34}
$$

### Comment lire la matrice finale ?

$$
T_{04} =
\begin{bmatrix}
R_{3\times3} & P_{3\times1} \\
0\;\,0\;\,0 & 1
\end{bmatrix}
$$

- **Le bloc $R$ (3×3, en haut à gauche)** : matrice de rotation, c'est-à-dire l'orientation de la pince dans l'espace.
- **La 4ᵉ colonne $P = (X, Y, Z)^T$** : vecteur de translation, c'est-à-dire la position exacte de la pince par rapport à la base.

Le détail pas à pas du produit matriciel est dans [docs/CALCULS.md](docs/CALCULS.md).

---

## 5. Interfaçage Python & CoppeliaSim

Un script Python communique avec CoppeliaSim via la **ZeroMQ Remote API**. Il lit la position des moteurs dans la simulation, les commande, et permet de comparer avec le MGD calculé.

Installation rapide :

```bash
pip install -r requirements.txt
```

Le guide complet (liaison VS Code ↔ CoppeliaSim, test de connexion, commande des moteurs, dépannage) est dans [docs/INTERFACAGE.md](docs/INTERFACAGE.md).

### Code Python : calcul du MGD

Le code complet se trouve dans [src/mgd.py](src/mgd.py).

### Résultat obtenu (position de repos, tous les angles à 0°)

Sortie de l'exécution dans VS Code :

```text
Matrice finale :
 [[  1.     0.     0.   300.87]
 [  0.     1.     0.     0.  ]
 [  0.     0.     1.   136.6 ]
 [  0.     0.     0.     1.  ]]
Position de la pince :
 [300.87   0.   136.6 ]
```

$$
T_{04} =
\begin{bmatrix}
1 & 0 & 0 & 300.87 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 136.6 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

La rotation est l'identité (tous les angles sont nuls) et la position vaut :

$$
P = \begin{bmatrix} a_2 + a_3 \\ 0 \\ d_1 \end{bmatrix}
= \begin{bmatrix} 142.07 + 158.8 \\ 0 \\ 136.6 \end{bmatrix}
= \begin{bmatrix} 300.87 \\ 0 \\ 136.6 \end{bmatrix} \text{ mm}
$$

Ici $d_4 = 0$ : la position correspond à l'extrémité du poignet. Avec $d_4 = 38$ mm, on aurait $Z = d_1 + d_4 = 174.6$ mm.
