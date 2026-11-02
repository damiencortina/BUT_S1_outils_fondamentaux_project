# Projet Outils Fondamentaux

## Affichage d'un cube et rotation de celui ci avec des matrices de projection.

Exécuter le code :

```bash
python main.py
```

2 cubes en rotation sont alors visibles. Le premier est tracé avec l'algorithme de tracé de Bresenham et le second avec une version plus simple.

Pour ce projet, je me suis aidé de l'IA (Claude) afin de :

* chercher des idées de projet
* apprendre comment fonctionne un affichage 3D du point de vue informatique et mathématique
* m'informer sur les matrices de projection
* apprendre comment implémenter les matrices de projection

Le fichier `ai_base_code.py` a été généré par Claude afin de faciliter ma compréhension des matrices de projection.

En partant de ce fichier de base, je vais écrire mon propre programme en utilisant la POO.

**Les fonctionnalités que je souhaite ajouter sont :**

* possibilité de tourner le cube avec les touches fléchées
* possibilité de zoomer avec les touches + et -
* [x] possibilité de basculer entre 2 algorithmes de tracé
* possibilité de varier la perspective
* comparaison de la vitesse de rendu entre le calcul de matrice "manuel" et en utilisant numpy