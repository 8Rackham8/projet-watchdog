import re

def analyze_logs(log_file_path):
    """
    Analyse un fichier de logs SSH et compte les tentatives de connexion échouées par adresse IP.
    """
    # Cette expression régulière (Regex) sert à repérer une adresse IP (ex: 192.168.1.1)
    ip_pattern = r'[0-9]+(?:\.[0-9]+){3}'
    
    # Dictionnaire pour stocker les IP et leur nombre de tentatives (ex: {"8.8.8.8": 5})
    failed_attempts = {}

    try:
        # On ouvre le fichier de logs en mode lecture ('r')
        with open(log_file_path, 'r') as file:
            for line in file:
                # On cherche les lignes contenant l'erreur spécifique
                if "Failed password" in line:
                    # On extrait l'adresse IP de la ligne
                    match = re.search(ip_pattern, line)
                    if match:
                        ip = match.group()
                        # Si l'IP est déjà dans notre dictionnaire, on ajoute +1
                        if ip in failed_attempts:
                            failed_attempts[ip] += 1
                        # Sinon, on l'ajoute avec la valeur 1
                        else:
                            failed_attempts[ip] = 1

        # --- AFFICHAGE DES RÉSULTATS ---
        print("\n=== Rapport d'Analyse WatchDog ===")
        if not failed_attempts:
            print(" Aucune menace détectée.")
        
        for ip, count in failed_attempts.items():
            # Si une IP a essayé de se connecter plus de 2 fois, on déclenche une alerte
            if count > 2:
                print(f"[ ALERTE] {count} tentatives échouées depuis l'IP : {ip}")
            else:
                print(f"[INFO] {count} tentative(s) échouée(s) depuis l'IP : {ip}")
        print("=====================================\n")

    except FileNotFoundError:
        print(f"[ERREUR] Le fichier {log_file_path} est introuvable. Vérifiez le chemin.")

# C'est ici que le script commence vraiment à s'exécuter
if __name__ == "__main__":
    # Chemin vers le faux fichier de logs qu'on a créé
    chemin_du_fichier = "sample_logs/auth.log"
    analyze_logs(chemin_du_fichier)
