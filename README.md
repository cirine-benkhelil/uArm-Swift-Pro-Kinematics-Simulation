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
