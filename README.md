# 🥧 Pi joue au labyrinthe

## Description

Ce projet illustre de manière visuelle et ludique l'utilisation des décimales de Pi pour résoudre un labyrinthe. Le programme génère un labyrinthe aléatoire et utilise chaque décimale de Pi comme instruction de mouvement, démontrant ainsi le caractère pseudo-aléatoire des décimales de cette constante mathématique.

## 🎮 Fonctionnement

### Principe de base

Le programme associe chaque décimale de Pi (après la virgule) à une direction de mouvement :

| Décimales | Direction | Symbole |
|-----------|-----------|---------|
| 0-1       | Haut      | ↑       |
| 2-3       | Droite    | →       |
| 4-5       | Bas       | ↓       |
| 6-7       | Gauche    | ←       |


### Règles du jeu

- 🟥 **Départ** : Case rouge en haut à gauche (position 0,0)
- 🟩 **Sortie** : Case verte en bas à droite
- 🟡 **Joueur** : Cercle jaune représentant Pi
- 🔵 **Cases visitées** : Marquées par des cercles bleus
- Si Pi essaie de traverser un mur, l'action est bloquée mais une nouvelle décimale est quand même consommée

## 🔢 Calcul de Pi

Le programme utilise la bibliothèque **mpmath** pour calculer Pi avec une précision arbitraire.

### Pourquoi mpmath ?

- **Précision illimitée** : Peut calculer des milliers de décimales
- **Optimisé** : Utilise l'algorithme de Chudnovsky, l'un des plus rapides pour calculer Pi
- **Simple d'utilisation** : Calcul en une seule ligne

### Fonctionnement du générateur

```python
class PiGenerator:
    def compute_pi(self):
        mp.dps = self.precision  # Définit le nombre de décimales
        pi = mp.pi               # Calcule Pi
        self.pi_str = str(pi).replace('.', '')  # Convertit en chaîne
```

Le générateur :
1. Calcule Pi avec 1000 décimales initialement
2. Stocke les décimales sous forme de chaîne
3. Retourne chaque décimale une par une via `get_next_digit()`
4. Si toutes les décimales sont consommées, recalcule avec 500 décimales supplémentaires

### L'algorithme de Chudnovsky

mpmath utilise par défaut l'algorithme de Chudnovsky, découvert en 1988 par les frères Chudnovsky. C'est l'un des algorithmes les plus rapides pour calculer Pi :

- Converge extrêmement rapidement (environ 14 décimales par itération)
- Utilisé pour battre des records mondiaux de calcul de Pi
- Basé sur des séries hypergéométriques

## 🌀 Génération du labyrinthe

Le labyrinthe est généré à l'aide de l'**algorithme de backtracking récursif** (ou Depth-First Search).

### Principe de l'algorithme

1. **Initialisation** : Toutes les cellules ont leurs 4 murs (haut, bas, gauche, droite)

2. **Processus de génération** :
   - Partir d'une cellule de départ (0,0)
   - Marquer la cellule comme visitée
   - Tant qu'il existe des cellules non visitées :
     - Regarder les voisins non visités de la cellule actuelle
     - Si des voisins existent :
       - Choisir un voisin aléatoirement
       - **Casser le mur** entre la cellule actuelle et le voisin
       - Empiler la cellule actuelle
       - Se déplacer vers le voisin
     - Sinon :
       - Dépiler et revenir à la cellule précédente

3. **Résultat** : Un labyrinthe parfait où :
   - Chaque cellule est accessible depuis n'importe quelle autre
   - Il n'existe qu'un seul chemin entre deux cellules (pas de boucles)

### Structure de données

Chaque cellule du labyrinthe possède :

```python
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {
            'top': True,
            'right': True,
            'bottom': True,
            'left': True
        }
        self.visited = False
```

### Avantages de cette méthode

- ✅ Génération rapide
- ✅ Crée des labyrinthes avec de longs couloirs (visuellement intéressants)
- ✅ Garantit qu'il existe toujours un chemin entre départ et sortie
- ✅ Pas de zones isolées ou inaccessibles

## 🎨 Affichage et optimisations

### Marquage des cases visitées

Au lieu de stocker tout le trajet de Pi (liste de positions), le programme utilise un **set de coordonnées** :

```python
self.visited_cells = set()
self.visited_cells.add((x, y))
```

Configuration actuelle :
- Écran : 1200×800 pixels
- Taille des cellules : 60×60 pixels
- Labyrinthe : 15×13 cellules
- Espace réservé pour les statistiques : 250 pixels à droite

## 📊 Interface utilisateur

### Pendant le jeu

L'interface affiche en temps réel :
- **Décimale** : La dernière décimale de Pi utilisée
- **Action** : La direction associée (Haut, Bas, Gauche, Droite)
- **Mouvements** : Nombre de déplacements réussis
- **Bloqué** : Nombre de tentatives bloquées par un mur
- **Total** : Nombre total de décimales consommées
- **Index** : Position actuelle dans la séquence de décimales
- **Position** : Coordonnées actuelles de Pi
- **Sortie** : Coordonnées de la case de sortie


## 🚀 Installation et utilisation

### Prérequis

```bash
pip install pygame mpmath
```

### Lancer le programme

```bash
python main.py
```

### Contrôles

- **ESPACE** : Générer un nouveau labyrinthe et recommencer

## 📝 Améliorations futures

Idées pour étendre le projet :

- [ ] Différents algorithmes de génération de labyrinthe (Prim, Kruskal)
- [ ] Comparer Pi avec d'autres constantes (e, φ, √2)
- [ ] Mode "course" avec plusieurs constantes mathématiques
- [ ] Statistiques détaillées (heatmap des zones visitées)

## 📚 Références

- [mpmath Documentation](http://mpmath.org/)
- [Algorithme de Chudnovsky](https://en.wikipedia.org/wiki/Chudnovsky_algorithm)
- [Maze Generation Algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Propriétés de Pi](https://en.wikipedia.org/wiki/Pi)

## 🤝 Contribution

N'hésitez pas à proposer des améliorations ou signaler des bugs !

## 📄 Licence

Projet éducatif libre d'utilisation.

---

*"Pi n'est pas seulement un nombre, c'est une fenêtre sur l'infini"* 🥧✨
