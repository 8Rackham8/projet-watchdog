# 🛡️ WatchDog - Log Analyzer & Threat Intelligence

**WatchDog** est un script Python développé dans le cadre de ma recherche d'alternance en cybersécurité. Il analyse les logs d'authentification pour détecter les attaques par force brute et vérifie la réputation des adresses IP malveillantes via l'API AbuseIPDB.

## 🚀 Fonctionnalités (Phase 2)
* Lecture automatisée de fichiers de logs locaux.
* Extraction des adresses IP via Expressions Régulières (Regex).
* **[Nouveau]** Intégration de l'API **AbuseIPDB** pour obtenir le score de malveillance (Threat Intelligence).
* Utilisation de variables d'environnement (`.env`) pour sécuriser les clés API.

## 🛠️ Installation et Utilisation

1. Cloner le dépôt et se rendre dans le dossier :
   ```bash
   git clone [https://github.com/TON_NOM_UTILISATEUR/projet-watchdog.git](https://github.com/TON_NOM_UTILISATEUR/projet-watchdog.git)
   cd projet-watchdog
