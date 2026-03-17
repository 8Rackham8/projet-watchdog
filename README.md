# 🛡️ WatchDog - Automated SOC & Threat Intelligence

**WatchDog** est un script Python d'analyse de logs orienté Blue Team. Développé comme un mini-SOC automatisé, il détecte les tentatives d'attaques par force brute, vérifie la réputation des adresses IP malveillantes via une API de Threat Intelligence, et remonte des alertes critiques en temps réel sur Discord.

## ✨ Fonctionnalités

* **Analyse de Logs Locale :** Parsing automatisé des fichiers `auth.log` et extraction des adresses IP via Expressions Régulières (Regex).
* **Threat Intelligence (CTI) :** Interrogation de l'API **AbuseIPDB** pour évaluer le score de malveillance des IP suspectes.
* **Alerting en Temps Réel :** Envoi d'alertes formatées sur un salon **Discord** via Webhook lorsqu'une menace est confirmée.
* **Sécurité (OpSec) :** Protection des identifiants et clés API via des variables d'environnement (`.env`).

---

## 📖 Guide de l'Utilisateur (Comment s'en servir)

Une fois le script configuré, voici comment l'utiliser pour surveiller votre serveur :

### 1. Préparer vos logs
Le script analyse par défaut le fichier situé dans `sample_logs/auth.log`. 
* **Pour tester :** Laissez les logs fournis par défaut dans le dossier.
* **Pour une vraie analyse :** Copiez votre propre fichier `/var/log/auth.log` (serveurs Linux) et placez-le dans le dossier `sample_logs/`.

### 2. Lancer l'analyse
Ouvrez votre terminal, assurez-vous que votre environnement virtuel est activé `(venv)`, et lancez la commande :
```bash
python3 watchdog.py

Comprendre les résultats dans le terminal

    [INFO] : Une IP a échoué à se connecter (moins de 3 fois). Bruit de fond normal d'Internet.

    [⚠️ INFO] : Une IP a échoué plusieurs fois. Le script a interrogé AbuseIPDB, mais l'IP n'est pas (encore) classée comme dangereuse.

    [🚨 ALERTE] : L'IP force l'accès ET est reconnue comme dangereuse par AbuseIPDB. Une alerte rouge est immédiatement envoyée sur Discord

🛠️ Guide du Développeur (Installation & Configuration)

Si vous souhaitez installer ce projet sur votre machine ou contribuer au code, suivez ces étapes :
1. Cloner le dépôt
Bash

git clone [https://github.com/TON_NOM_UTILISATEUR/projet-watchdog.git](https://github.com/TON_NOM_UTILISATEUR/projet-watchdog.git)
cd projet-watchdog

2. Créer et activer l'environnement virtuel

Il est indispensable d'isoler les dépendances Python :
Bash

python3 -m venv venv
source venv/bin/activate

3. Installer les dépendances
Bash

pip install -r requirements.txt

4. Configurer les clés API (Variables d'environnement)

Ce projet utilise des clés privées qui ne sont pas versionnées sur GitHub.

    Copiez le modèle de configuration pour créer votre fichier local :
    Bash

cp .env.example .env

Éditez le fichier .env pour y ajouter vos informations :

    Votre clé d'API AbuseIPDB.

    L'URL de votre Webhook Discord (créé dans les paramètres de votre salon).
