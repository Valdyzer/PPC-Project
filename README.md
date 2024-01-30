# Hannabis - Jeu Coopératif avec Multiprocessing

## Introduction

Bienvenue dans le projet Hannabis, une version avancée du célèbre jeu de société Hanabi, développée en utilisant des concepts de multiprocessing en Python. Ce projet vise à créer une simulation réaliste du jeu où les joueurs échangent des données entre eux et avec un serveur central en utilisant des sockets, des Processus, une shared memory, des queues de messages et des signaux.

## Objectif

L'objectif principal de ce projet est de démontrer comment la programmation parallèle peut être exploitée pour créer une simulation immersive du jeu Hannabis. Nous utilisons des techniques avancées pour la communication entre processus, offrant ainsi une expérience de jeu réaliste et interactive.

## Fonctionnalités

- **Multiprocessing :** Utilisation de Process pour simuler une partie dynamique et concurrente du jeu.
- **Sockets :** Communication entre le serveur central et les joueurs pour une interaction transparente.
- **Shared Memory :** Partage de données globales entre les processes.
- **Message Queues :** Transmission asynchrone d'informations entre les joueurs.
- **Signal :** Synchronisation des actions entre les différents processus lors d'évènements particulier (ex : fin de partie).

## Installation

1. Clonez le dépôt : `git clone https://github.com/Valdyzer/PPC-Project.git`
2. Accédez au répertoire du projet : `cd PPC-Project`

## Utilisation

1. Exécutez le serveur : `python game.py`
2. Exécutez les joueurs : `python testclient.py`
3. Suivez les instructions pour participer à la simulation du jeu.
