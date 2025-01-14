## Fonctionnalités

- 🎮 Gameplay interactif avec division des piles par glisser-déposer
- ⚛️ Visualisation atomique avec des orbites électroniques dynamiques
- 🎨 Arrière-plans en dégradé et effets de particules *magnifiques*
- 🤖 Adversaire IA pour une expérience solo
- 📊 Suivi de l'historique des mouvements
- 🔄 Gestion de l'état du jeu
- 🖥️ Redimensionnement de la fenêtre réactif

## Interface en ligne de commande

```bash
usage: python -m grundy [-h] [--width WIDTH] [--height HEIGHT] [--pile PILE] [--scene {menu,play,gameover}]

Grundy's Game Settings

options:
  -h, --help            show this help message and exit
  --width WIDTH         set the initial screen width (default: 800)
  --height HEIGHT       set the initial screen height (default: 600)
  --pile PILE, -p PILE  set the initial pile size (default: 16)
  --scene {menu,play,gameover}
                        choose the initial scene to start (default: 'menu')
```

## Architecture

L'architecture du jeu repose sur une structure modulaire, permettant de séparer efficacement les différentes tâches tout en assurant une communication fluide entre les divers composants du système. Au cœur de cette architecture se trouve le système moteur `Engine`, il s'agit du coordinateur central gérant la fenêtre d'affichage, le canvas, les événements, les scènes et la logique du jeu.

## **Logique du jeu**

Les mécaniques fondamentales du jeu sont gérées par le système **Logic**, qui suit l'état des piles et valide les actions des joueurs selon les règles du jeu de Grundy. Lorsqu'un joueur tente de diviser une pile, le système vérifie la validité du coup : les piles résultantes doivent être de tailles inégales et la division doit respecter les règles du jeu.

Le système **Logic** est également responsable de l'alternance des tours et de l'exécution des coups. Il gère l'alternance entre le joueur humain et l'adversaire contrôlé par l'IA, valide les coups et diffuse les événements relatifs aux actions des joueurs. L'IA utilise une logique simple, choisissant au hasard des divisions valides. Le système suit l'évolution de la partie et déclare un vainqueur lorsque les conditions sont remplies.

## Système d'évènements

Le système d'évènements facilite la communication entre les différents composants, sans qu'ils soient directement liés les uns aux autres. Il repose sur un modèle de publication-abonnement, où les composants s'échangent des événements au lieu de s'appeler mutuellement. Cela réduit les dépendances entre les éléments, rendant le système plus modulaire et plus facile à maintenir.

Les événements couvrent une large gamme d'actions, allant des entrées utilisateur aux changements d'état du jeu, en passant par la gestion de la fenêtre et les conditions de victoire.

Voici une liste non-exhaustive des évènements existants:
- `WINDOW_RESIZE`: Changement de résolution
- `UPDATE`: Mis à jour du rendu
- `SCENE_CHANGED`: Transition à une nouvelle scène
- `MOVE_MADE`: Coup effectué par un joueur
- `GAME_OVER`: Fin de la partie
- `GAME_RESET`: Réinitialisation de la partie
- `PILE_ADDED/REMOVED`: Etat d'une pile mise à jour

## Système de composants

Le jeu utilise une architecture basée sur des nœuds où chaque composant visuel hérite de la classe de base `Node`.

Chaque **Node** est un composant autonome ayant des fonctions spécifiques, qu'il s'agisse de la gestion d'éléments visuels ou de la logique du jeu. Les nodes gèrent leur propre cycle de vie, traitent les événements qui les concernent et gèrent leurs ressources. Cette indépendance permet une grande flexibilité, offrant la possibilité d'ajouter, de modifier ou de supprimer des composants sans perturber l'intégrité du système global.

## Système de scènes

Le système **Scene** est responsable de l'organisation des états du jeu. Chaque scène représente un état spécifique, comme le menu principal, le jeu lui-même ou la fin de la partie. Les scènes servent de conteneurs pour les objets du jeu, en gérant leur cycle de vie (création et destruction).

 Cela permet d'assurer des transitions fluides entre les différentes phases du jeu, tout en maintenant une organisation claire et bien définie des éléments.