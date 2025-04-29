import requests
import json
import sys

# Adresse serveur HTTP
SERVER_URL = 'http://localhost:5000'

def send_request(endpoint, payload):
    url = f"{SERVER_URL}/{endpoint}"
    try:
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
        print("Réponse du serveur:", json.dumps(data, ensure_ascii=False, indent=2))
    except requests.RequestException as e:
        print(f"Erreur HTTP: {e}")

if __name__ == '__main__':
    while True:
        print("\n--- Menu HTTP ---")
        print("1. S'inscrire")
        print("2. Envoyer une action")
        print("3. Quitter")
        choice = input("Choix : ")

        if choice == '1':
            pseudo = input("Pseudo (1 lettre) : ").upper()
            role   = input("Rôle (wolf/villager) : ").lower()
            payload = {'type': 'subscribe', 'pseudo': pseudo, 'role': role}
            send_request('subscribe', payload)

        elif choice == '2':
            pseudo = input("Votre pseudo : ").upper()
            dx     = int(input("Déplacement X (-1,0,1) : "))
            dy     = int(input("Déplacement Y (-1,0,1) : "))
            payload = {'type': 'action', 'pseudo': pseudo, 'action': [dx, dy]}
            send_request('action', payload)

        elif choice == '3':
            sys.exit(0)

        else:
            print("Choix invalide.")
