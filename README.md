# Pi joue au labyrinthe

Ce projet est une visualisation interactive où les décimales de π contrôlent un joueur traversant un labyrinthe généré procéduralement.  
Chaque chiffre détermine une direction, et Pi tente d’atteindre la sortie automatiquement.

Projet réalisé en Python avec Pygame et mpmath.

---

## Fonctionnalités

- Génération d’un labyrinthe parfait (sans cycles).
- Calcul arbitraire de décimales de π avec mpmath.
- Déplacement automatique du joueur selon les chiffres successifs de π.
- Affichage en temps réel : décimale, direction, mouvements, blocages, position, index.
- Réinitialisation complète avec la touche Espace.

---

## Prérequis

- Python 3.8 ou plus.
- Dépendances :  
  ```bash
  pip install pygame mpmath
