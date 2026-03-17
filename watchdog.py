import re
import os
import requests
from dotenv import load_dotenv

# Charge les variables cachées dans le fichier .env
load_dotenv()
API_KEY = os.getenv("ABUSEIPDB_API_KEY")

def check_ip_reputation(ip):
    """
    Interroge l'API AbuseIPDB pour obtenir le score de malveillance d'une IP.
    """
    if not API_KEY:
        return "Erreur : Clé API introuvable."

    url = 'https://api.abuseipdb.com/api/v2/check'
    querystring = {
        'ipAddress': ip,
        'maxAgeInDays': '90' # On vérifie les signalements des 90 derniers jours
    }
    headers = {
        'Accept': 'application/json',
        'Key': API_KEY
    }

    try:
        # On envoie la requête à l'API
        response = requests.get(url, headers=headers, params=querystring)
        
        # Si la réponse est 200 (Succès)
        if response.status_code == 200:
            data = response.json()
            # On extrait juste le score de confiance en pourcentage
            score = data['data']['abuseConfidenceScore']
            return score
        else:
            return f"Erreur API ({response.status_code})"
    except Exception as e:
        return "Erreur de connexion"

def analyze_logs(log_file_path):
    """
    Analyse un fichier de logs SSH et compte les tentatives échouées.
    """
    ip_pattern = r'[0-9]+(?:\.[0-9]+){3}'
    failed_attempts = {}

    try:
        with open(log_file_path, 'r') as file:
            for line in file:
                if "Failed password" in line:
                    match = re.search(ip_pattern, line)
                    if match:
                        ip = match.group()
                        if ip in failed_attempts:
                            failed_attempts[ip] += 1
                        else:
                            failed_attempts[ip] = 1

        print("\n=== Rapport d'Analyse WatchDog (Phase 2) ===")
        if not failed_attempts:
            print(" Aucune menace détectée.")
        
        for ip, count in failed_attempts.items():
            if count > 2:
                print(f"[*] Analyse de l'IP {ip} sur AbuseIPDB en cours...")
                score = check_ip_reputation(ip)
                
                # Formatage de l'alerte selon le score
                if isinstance(score, int) and score > 0:
                    print(f"[ ALERTE CRITIQUE] {count} tentatives depuis {ip} | Score de malveillance : {score}% ! ☠️")
                else:
                    print(f"[ ALERTE] {count} tentatives depuis {ip} | Score de malveillance : {score}% (Peut-être un bot non signalé)")
            else:
                print(f"[INFO] {count} tentative(s) échouée(s) depuis l'IP : {ip}")
        print("================================================\n")

    except FileNotFoundError:
        print(f"[ERREUR] Le fichier {log_file_path} est introuvable.")

if __name__ == "__main__":
    chemin_du_fichier = "sample_logs/auth.log"
    analyze_logs(chemin_du_fichier)
