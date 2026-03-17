import re
import os
import requests
from dotenv import load_dotenv

# Charge les variables cachées dans le fichier .env
load_dotenv()
API_KEY = os.getenv("ABUSEIPDB_API_KEY")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK_URL")

def send_discord_alert(ip, count, score):
    """
    Envoie une notification formatée vers un salon Discord via Webhook.
    """
    if not DISCORD_WEBHOOK:
        return

    # Formatage du message pour Discord (Embed)
    data = {
        "username": "WatchDog Alert",
        "avatar_url": "https://cdn-icons-png.flaticon.com/512/2097/2097945.png",
        "content": "🚨 **NOUVELLE MENACE DÉTECTÉE** 🚨",
        "embeds": [
            {
                "title": "Attaque par Brute Force SSH",
                "description": "Un comportement suspect a été repéré dans les logs d'authentification.",
                "color": 16711680,
                "fields": [
                    {"name": "🛑 IP Malveillante", "value": f"`{ip}`", "inline": True},
                    {"name": "🔄 Tentatives", "value": str(count), "inline": True},
                    {"name": "☠️ Score AbuseIPDB", "value": f"{score}% de dangerosité", "inline": False}
                ],
                "footer": {"text": "WatchDog Security - Automated SOC"}
            }
        ]
    }

    try:
        requests.post(DISCORD_WEBHOOK, json=data)
    except Exception as e:
        print(f"[ERREUR LOCALE] Problème de connexion avec Discord : {e}")

def check_ip_reputation(ip):
    """Interroge l'API AbuseIPDB pour obtenir le score de malveillance."""
    if not API_KEY:
        return "Clé API manquante"

    url = 'https://api.abuseipdb.com/api/v2/check'
    headers = {'Accept': 'application/json', 'Key': API_KEY}
    querystring = {'ipAddress': ip, 'maxAgeInDays': '90'}

    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            return response.json()['data']['abuseConfidenceScore']
        return "Erreur API"
    except:
        return "Erreur Connexion"

def analyze_logs(log_file_path):
    """Analyse les logs et déclenche les alertes."""
    ip_pattern = r'[0-9]+(?:\.[0-9]+){3}'
    failed_attempts = {}

    try:
        with open(log_file_path, 'r') as file:
            for line in file:
                if "Failed password" in line:
                    match = re.search(ip_pattern, line)
                    if match:
                        ip = match.group()
                        failed_attempts[ip] = failed_attempts.get(ip, 0) + 1

        print("\n=== 🛡️ Rapport d'Analyse WatchDog (Phase 3) ===")
        
        for ip, count in failed_attempts.items():
            if count > 2:
                print(f"[*] Analyse de l'IP {ip} sur AbuseIPDB en cours...")
                score = check_ip_reputation(ip)
                
                # Remis à > 0 pour la version finale
                if isinstance(score, int) and score > 0:
                    print(f"[🚨 ALERTE] {count} tentatives depuis {ip} | Score : {score}% ! Envoi sur Discord...")
                    send_discord_alert(ip, count, score)
                else:
                    print(f"[⚠️ INFO] {count} tentatives depuis {ip} | Score : {score}%")
            else:
                print(f"[INFO] {count} tentative(s) depuis : {ip}")
                
        print("================================================\n")

    # C'est ce bloc "except" qui manquait ou qui était mal aligné !
    except FileNotFoundError:
        print(f"[ERREUR] Le fichier {log_file_path} est introuvable.")

if __name__ == "__main__":
    chemin_du_fichier = "sample_logs/auth.log"
    analyze_logs(chemin_du_fichier)
