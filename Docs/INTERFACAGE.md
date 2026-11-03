# Interfaçage Python ↔ CoppeliaSim

Ce guide explique comment relier VS Code à CoppeliaSim pour lire et commander les articulations du uArm Swift Pro.

## 1. Prérequis

| Élément | Détail |
| :--- | :--- |
| **CoppeliaSim** | Version Edu (V4.6 ou plus récente recommandée) |
| **Python** | 3.8 ou plus |
| **VS Code** | Avec les extensions **Python** et **Code Runner** |

## 2. Installation des bibliothèques

Dans le terminal de VS Code :

```bash
pip install numpy
pip install coppeliasim-zmqremoteapi-client
```

Ou en une seule commande depuis la racine du dépôt :

```bash
pip install -r requirements.txt
```

Le second paquet installe automatiquement ses dépendances (`pyzmq`, `cbor2`). Vérification :

```bash
pip show coppeliasim-zmqremoteapi-client
```

## 3. Liaison VS Code ↔ CoppeliaSim

1. **Ouvrir CoppeliaSim** puis charger la scène du uArm Swift Pro.
2. **Serveur ZeroMQ** : dans les versions récentes, le serveur *ZMQ remote API* démarre automatiquement avec CoppeliaSim, sur le port **23000**. Aucune configuration n'est nécessaire.
3. **Ouvrir le script dans VS Code**, puis choisir le bon interpréteur (`Ctrl + Shift + P` → *Python: Select Interpreter*), celui où le `pip install` a été fait.
4. **Exécuter** avec Code Runner (`Ctrl + Alt + N`) ou avec le bouton ▶.

> **Important :** CoppeliaSim doit être ouvert **avant** de lancer le script Python, sinon la connexion échoue.

## 4. Test de connexion

Lancer `src/test_connexion.py`. Si la version de CoppeliaSim s'affiche, la liaison fonctionne.

## 5. Lecture et commande des moteurs

```python
import math
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require('sim')

# Récupération des articulations (adapter les noms à ceux de votre scène)
joints = [sim.getObject(f'/joint{i}') for i in range(1, 5)]

sim.startSimulation()

# Lecture des angles actuels (CoppeliaSim renvoie des radians)
angles_deg = [math.degrees(sim.getJointPosition(j)) for j in joints]
print("Angles actuels (°) :", angles_deg)

# Commande : envoi des angles (convertis en radians)
cibles = [30, 45, 20, 0]
for j, angle in zip(joints, cibles):
    sim.setJointTargetPosition(j, math.radians(angle))

sim.stopSimulation()
```

> Les noms `/joint1` à `/joint4` sont des exemples : ils doivent correspondre aux noms des articulations dans la hiérarchie de votre scène.

## 6. Dépannage

| Problème | Solution |
| :--- | :--- |
| `ConnectionRefusedError` | CoppeliaSim n'est pas ouvert, ou le serveur ZMQ n'est pas actif |
| `ModuleNotFoundError` | Le `pip install` a été fait pour un autre interpréteur Python |
| `Object does not exist` | Le nom donné à `sim.getObject` ne correspond pas à la scène |
