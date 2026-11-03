# Détail des calculs du MGD

Ce document détaille le calcul de $T_{04} = T_{01} \times T_{12} \times T_{23} \times T_{34}$ pour la position de repos ($\theta_1 = \theta_2 = \theta_3 = \theta_4 = 0$).

Paramètres (en mm) : $d_1 = 136.6$, $a_2 = 142.07$, $a_3 = 158.8$, $d_4 = 0$.

## 1. Matrices avec tous les angles à 0

$$
T_{01} =
\begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 0 & -1 & 0 \\
0 & 1 & 0 & d_1 \\
0 & 0 & 0 & 1
\end{bmatrix}
\qquad
T_{12} =
\begin{bmatrix}
1 & 0 & 0 & a_2 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

$$
T_{23} =
\begin{bmatrix}
1 & 0 & 0 & a_3 \\
0 & 0 & 1 & 0 \\
0 & -1 & 0 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
\qquad
T_{34} =
\begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & d_4 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

## 2. Produit étape par étape

**Étape 1 : $T_{02} = T_{01} \times T_{12}$**

$$
T_{02} =
\begin{bmatrix}
1 & 0 & 0 & a_2 \\
0 & 0 & -1 & 0 \\
0 & 1 & 0 & d_1 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

**Étape 2 : $T_{03} = T_{02} \times T_{23}$**

Les deux rotations se compensent ($\alpha_1 = +90°$ puis $\alpha_3 = -90°$), la rotation redevient l'identité :

$$
T_{03} =
\begin{bmatrix}
1 & 0 & 0 & a_2 + a_3 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & d_1 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

**Étape 3 : $T_{04} = T_{03} \times T_{34}$**

$$
T_{04} =
\begin{bmatrix}
1 & 0 & 0 & a_2 + a_3 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & d_1 + d_4 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

## 3. Application numérique

$$
X = a_2 + a_3 = 142.07 + 158.8 = 300.87 \text{ mm}
$$

$$
Y = 0 \text{ mm}
$$

$$
Z = d_1 + d_4 = 136.6 + 0 = 136.6 \text{ mm}
$$

Ce résultat est identique à la sortie du code Python (`src/mgd.py`).

## 4. Lecture de la matrice finale

| Partie de $T_{04}$ | Signification |
| :--- | :--- |
| Bloc $3 \times 3$ en haut à gauche | Orientation de la pince (matrice de rotation) |
| 4ᵉ colonne, 3 premières lignes | Position $(X, Y, Z)$ de la pince par rapport à la base |
| Dernière ligne $[0\;0\;0\;1]$ | Terme de normalisation des coordonnées homogènes |

Ici, la rotation est l'identité : la pince a la même orientation que le repère de la base. Le bras est tendu vers l'avant, le long de l'axe $X$.

## 5. Vérification par la géométrie

Au repos, le bras est entièrement aligné selon $X$ : on parcourt la longueur du bras ($a_2$) puis celle de l'avant-bras ($a_3$), à la hauteur du socle ($d_1$). Le résultat $(a_2 + a_3,\ 0,\ d_1)$ est cohérent avec cette lecture physique.
