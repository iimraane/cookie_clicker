
# Cookie Simulator

Cookie Simulator est un jeu de type *clicker* dans lequel vous accumulez des cookies en effectuant des clics manuels et en investissant dans des bâtiments qui produisent des cookies automatiquement. Le jeu repose sur une **économie exponentielle** : les coûts et la production augmentent de manière exponentielle, ce qui permet d'atteindre des niveaux astronomiques (pensez quadrillions de cookies et plus).

Dans Cookie Simulator, vous débloquez **150 bâtiments** de manière séquentielle (seul le premier est disponible dès le départ, et pour acheter un bâtiment d'indice *i* (i ≥ 1), vous devez avoir acheté le bâtiment d'indice *i-1*) et vous bénéficiez de **50 améliorations (upgrades)** réparties en deux catégories (25 pour améliorer vos clics et 25 pour booster la production des bâtiments). Ces améliorations apparaissent aléatoirement dès que vous atteignez certains seuils de cookies.

Le jeu utilise **Pygame** pour l'interface graphique, avec un système intégré de saisie de texte pour réaliser des achats.

---

## Table des Matières

1. [Introduction](#introduction)
2. [Fonctionnalités](#fonctionnalités)
3. [Installation](#installation)
4. [Lancer le Jeu](#lancer-le-jeu)
5. [Contrôles et Commandes](#contrôles-et-commandes)
6. [Logique et Économie](#logique-et-économie)
    - [Clics Manuels](#clics-manuels)
    - [Production Automatique](#production-automatique)
    - [Bâtiments](#bâtiments)
    - [Upgrades / Améliorations](#upgrades--améliorations)
    - [Déblocage Séquentiel](#déblocage-séquentiel)
    - [Progression Exponentielle](#progression-exponentielle)
7. [Architecture et Code Technique](#architecture-et-code-technique)
8. [Personnalisation et Extensions](#personnalisation-et-extensions)
9. [Crédits et Remerciements](#crédits-et-remerciements)
10. [Conclusion](#conclusion)

---

## Introduction

Cookie Simulator est un jeu addictif où l'objectif est d'accumuler le plus grand nombre de cookies possible. Vous commencez par cliquer pour générer des cookies, puis vous investissez ces cookies dans des bâtiments qui produisent des cookies automatiquement. Au fil de votre progression, de nouvelles améliorations apparaissent pour augmenter la puissance de vos clics et la production de vos bâtiments. Grâce à une économie exponentielle, vous pourrez atteindre des niveaux de production inimaginables.

---

## Fonctionnalités

- **Production Manuelle et Automatique**
  - Génération de cookies par clic manuel.
  - Production automatique par des bâtiments investis.

- **150 Bâtiments Débloqués Séquentiellement**
  - Chaque bâtiment porte un nom humoristique (ex. "Grand-mère fabriqueuse de cookie", "Ferme à cookie", "Esclaves fabriqueurs de cookie", etc.).
  - Seul le bâtiment 0 est accessible dès le début. Pour acheter un bâtiment d'indice *i* (i ≥ 1), il faut avoir acheté le bâtiment d'indice *i-1*.

- **50 Améliorations (Upgrades)**
  - 25 upgrades pour améliorer le gain par clic.
  - 25 upgrades pour booster la production des bâtiments.
  - Les améliorations apparaissent aléatoirement dès que vous atteignez certains seuils de cookies.

- **Économie Exponentielle**
  - Les coûts et la production augmentent de façon exponentielle, vous permettant de progresser vers des sommes astronomiques de cookies.

- **Interface Graphique Interactive**
  - Utilisation de Pygame pour une interface fluide.
  - Système de saisie intégré pour acheter des bâtiments et des upgrades via le clavier.

---

## Installation

### Prérequis

- **Python 3.x**  
  Assurez-vous d'avoir Python 3 installé sur votre système.

- **Pygame**  
  Le jeu utilise Pygame pour l'affichage graphique.

### Installation de Pygame

Ouvrez votre terminal ou invite de commandes et exécutez :

```bash
pip install pygame
```

### Téléchargement du Code

Clonez ou téléchargez le code source du projet depuis votre dépôt Git, ou copiez le fichier source fourni et nommez-le par exemple `cookie_simulator.py`.

---

## Lancer le Jeu

Pour démarrer le jeu, placez-vous dans le répertoire contenant `cookie_simulator.py` et lancez :

```bash
python cookie_simulator.py
```

Une fenêtre graphique (1024x768 pixels) s'ouvrira, et le jeu commencera.

---

## Contrôles et Commandes

Pendant le jeu, utilisez les commandes suivantes :

- **C** : Effectuer un clic manuel pour générer des cookies.
- **B** : Acheter un bâtiment  
  - Appuyez sur **B** pour lancer le mode achat de bâtiment.
  - Une invite apparaîtra en bas de l'écran vous demandant d'entrer l'indice du bâtiment à acheter (de 0 à 149).
  - Saisissez le numéro correspondant et appuyez sur **Entrée**.
- **U** : Acheter une amélioration (upgrade)  
  - Appuyez sur **U** pour choisir le type d'upgrade :
    - Tapez **1** pour les améliorations de clic.
    - Tapez **2** pour les améliorations de bâtiments.
  - Une invite apparaîtra ensuite pour saisir l'indice de l'upgrade désirée.
- **Q** : Quitter le jeu.

---

## Logique et Économie

### Clics Manuels

- **Fonctionnement** :  
  Chaque pression sur **C** génère un nombre de cookies égal à :
  
  ```
  cookies_per_click * global_multiplier_click
  ```
  
- **Améliorations** :  
  Les upgrades de clic augmentent `global_multiplier_click`, boostant ainsi le gain de chaque clic.

### Production Automatique

- **Bâtiments** :  
  Chaque bâtiment produit un nombre de cookies par seconde, calculé selon :
  
  ```
  total_production = sum(building.count * building.production) * global_building_multiplier
  ```
  
  Ce total est ajouté au nombre de cookies en fonction du temps écoulé.
  
- **Global Building Multiplier** :  
  Les upgrades pour les bâtiments augmentent `global_building_multiplier`, améliorant ainsi l'ensemble de la production automatique.

### Bâtiments

- **Déblocage Séquentiel** :  
  Seul le bâtiment d'indice 0 est débloqué dès le départ. Pour qu'un bâtiment d'indice *i* (i ≥ 1) soit achetable, il faut avoir déjà acheté le bâtiment d'indice *i-1*.
  
- **Coût** :  
  Le coût d'un bâtiment est donné par la formule :
  
  ```
  cost = base_cost * (cost_multiplier ** count)
  ```
  
  - `base_cost` est défini de façon exponentielle (par exemple, 10 * (growth_factor ** i)).
  - `cost_multiplier` (par exemple 1.15) augmente le coût à chaque achat.
  
- **Production** :  
  La production de cookies par bâtiment augmente également de façon exponentielle.

### Upgrades / Améliorations

- **Catégories d'Upgrades** :  
  - **Upgrades de Clic** : Augmentent la puissance de vos clics.
  - **Upgrades de Bâtiments** : Boostent la production globale des bâtiments.
  
- **Apparition Aléatoire** :  
  Chaque upgrade reste cachée jusqu'à ce que vous atteigniez un certain seuil de cookies. Une fois ce seuil atteint, une faible probabilité (par exemple, 3 % par cycle) déclenche l'affichage de l'upgrade.
  
- **Effet** :  
  Lorsqu'une amélioration est achetée, elle multiplie soit la valeur de vos clics, soit la production de vos bâtiments.

### Progression Exponentielle

- **Coûts et Production** :  
  Grâce à des formules exponentielles, le coût des bâtiments et des upgrades ainsi que leur production augmentent de façon rapide, vous permettant d'accumuler des niveaux de cookies extrêmement élevés.

---

## Architecture et Code Technique

- **Langage et Bibliothèque** :  
  Développé en Python 3 avec Pygame pour l'interface graphique.

- **Boucle Principale** :  
  La boucle principale gère :
  - La mise à jour de la production automatique des cookies.
  - La gestion des événements clavier (clics, achats, saisie).
  - Le rendu graphique des statistiques, bâtiments et upgrades.

- **Système de Saisie** :  
  Un système de saisie texte intégré permet de saisir des indices pour acheter des bâtiments et des upgrades. Il gère les entrées clavier (caractères, retour arrière, validation).

- **Modèle Économique Exponentiel** :  
  Les coûts et la production évoluent selon des formules exponentielles, assurant une progression constante et addictive.

---

## Personnalisation et Extensions

Vous pouvez personnaliser et étendre Cookie Simulator en modifiant :

- **Les Bâtiments** :  
  - Changez les noms dans les listes prédéfinies.
  - Ajustez le facteur de croissance (`growth_factor`) pour modifier la progression.
  
- **Les Upgrades** :  
  - Modifiez les coûts, multiplicateurs et seuils.
  - Ajoutez de nouvelles catégories ou types d'améliorations.

- **L'Interface Graphique** :  
  - Personnalisez la taille de la fenêtre, les polices et les couleurs.
  - Intégrez de nouveaux éléments graphiques ou animations.

- **La Logique de Jeu** :  
  - Ajoutez des mécaniques supplémentaires (bonus temporaires, événements spéciaux, etc.).

---

## Crédits et Remerciements

- **Auteur** : [Votre Nom]
- **Inspirations** : Cookie Clicker et autres clicker games.
- **Bibliothèque Principale** : [Pygame](https://www.pygame.org/)
- Un grand merci à la communauté open-source pour son soutien et ses contributions.

---

## Conclusion

Cookie Simulator est un projet ambitieux et évolutif qui combine une économie exponentielle, un système de progression séquentielle et une interface graphique interactive. Que vous soyez joueur à la recherche d'un défi addictif ou développeur curieux d'explorer les mécaniques des clicker games, ce projet offre une base riche et personnalisable.

*Amusez-vous bien à accumuler des cookies interstellaires, et n'hésitez pas à partager vos retours et contributions !*
```

# License

Please just don't steal my code..