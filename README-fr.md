### **Architecture principale**

L'architecture du jeu repose sur une structure solide et modulaire, permettant de séparer efficacement les différentes tâches tout en assurant une communication fluide entre les divers composants du système. Au cœur de cette architecture se trouve le système **Engine**, qui joue un rôle central en coordonnant l'ensemble des actions du jeu. Il gère plusieurs éléments essentiels, tels que la fenêtre du jeu, les entrées de l'utilisateur, la boucle de jeu, ainsi que la communication entre les différents sous-systèmes.

Le système **Scene** est responsable de l'organisation des états du jeu. Chaque scène représente un état spécifique, comme le menu principal, le jeu lui-même ou la fin de la partie. Les scènes servent de conteneurs pour les objets du jeu, en gérant leur cycle de vie, depuis leur création jusqu'à leur destruction. Cela permet d'assurer des transitions fluides entre les différentes phases du jeu, tout en maintenant une organisation claire et bien définie des éléments.

Le système **Node** constitue la base de tous les objets du jeu. Chaque **Node** est un composant autonome ayant des fonctions spécifiques, qu'il s'agisse de la gestion d'éléments visuels ou de la logique du jeu. Les nodes gèrent leur propre cycle de vie, traitent les événements qui les concernent et gèrent leurs ressources. Cette indépendance permet une grande flexibilité, offrant la possibilité d'ajouter, de modifier ou de supprimer des composants sans perturber l'intégrité du système global.

Le système **Event** facilite la communication entre les différents composants, sans qu'ils soient directement liés les uns aux autres. Il repose sur un modèle de publication-abonnement, où les composants s'échangent des événements au lieu de s'appeler mutuellement. Cela réduit les dépendances entre les éléments, rendant le système plus modulaire et plus facile à maintenir. Les événements couvrent une large gamme d'actions, allant des entrées utilisateur aux changements d'état du jeu, en passant par la gestion de la fenêtre et les conditions de victoire.

---

### **Logique du jeu**

Les mécaniques fondamentales du jeu sont gérées par le système **Logic**, qui suit l'état des piles et valide les actions des joueurs selon les règles du jeu de Grundy. Lorsqu'un joueur tente de diviser une pile, le système vérifie la validité du coup : les piles résultantes doivent être de tailles inégales et la division doit respecter les règles du jeu.

Le système **Logic** est également responsable de l'alternance des tours et de l'exécution des coups. Il gère l'alternance entre le joueur humain et l'adversaire contrôlé par l'IA, valide les coups et diffuse les événements relatifs aux actions des joueurs. L'IA utilise une logique simple, choisissant au hasard des divisions valides. Le système suit l'évolution de la partie et déclare un vainqueur lorsque les conditions sont remplies.

---

### **Systèmes graphiques**

Le système **Canvas** étend les capacités du canvas de **turtle** (`turtle.getcanvas()`) pour offrir des fonctionnalités de rendu avancées. Il prend en charge les dégradés et les formes personnalisées, permettant ainsi de dessiner tous les éléments visuels du jeu, allant des éléments de base aux effets de particules, en passant par les interfaces utilisateurs.

Le système **Viewport**, quant à lui, étend les capacités de la fenêtre de **turtle** (`turtle.Screen()`). Il gère les événements liés à la fenêtre, ajuste la résolution de l'écran et veille à ce que l'affichage du jeu soit adapté aux différentes tailles d'écrans et résolutions disponibles.

---

### **Composants graphiques**

La communication entre les composants repose sur un modèle basé sur les événements. Dans ce système, chaque composant peut s'abonner à des événements spécifiques plutôt que d'établir des appels directs vers d'autres composants. Ce modèle permet de réduire les dépendances et de rendre le code plus modulaire.

Lorsqu'une nouvelle fonctionnalité est ajoutée, il est souvent préférable d'utiliser le système d'événements pour la communication entre les composants, car cela facilite la gestion des interactions. Chaque composant peut s'abonner aux événements dont il a besoin et recevoir les notifications appropriées.
Lorsque les composants sont désactivés, il est important de se désabonner des événements pour éviter toute interférence, et de gérer correctement les paramètres associés aux événements pour assurer une communication fluide et sans erreurs.