#  WatchDog - Log Analyzer

**WatchDog** est un script Python développé dans le cadre de ma recherche d'alternance en cybersécurité. Il permet d'analyser automatiquement des fichiers de logs d'authentification (comme `auth.log` sous Linux) pour détecter les tentatives de connexion SSH échouées (Brute Force).

##  Fonctionnalités actuelles (Phase 1)
* Lecture automatisée de fichiers de logs locaux.
* Extraction des adresses IP malveillantes via Expressions Régulières (Regex).
* Comptage des tentatives et génération d'une alerte dans le terminal si un seuil de tolérance est dépassé.

## Installation et Utilisation

1. Cloner le dépôt :
   ```bash
   git clone [https://github.com/8Rackham8/projet-watchdog.git](https://github.com/8Rackham8/projet-watchdog.git)
   cd projet-watchdog
