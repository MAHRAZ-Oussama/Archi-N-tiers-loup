import requests
import sys

# Configuration du serveur HTTP
SERVER_URL = 'http://localhost:8000'

# Inscrire un joueur (/players)
def subscribe(pseudo, role):
    url = f"{SERVER_URL}/players"
    payload = {'pseudo': pseudo, 'role': role}
    try:
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
        print(f"Serveur: {data.get('message')}")
    except requests.RequestException as e:
        print(f"Erreur lors de l'inscription: {e}")

# Envoyer une action (/action)
def send_action(pseudo, dx, dy):
    url = f"{SERVER_URL}/action"
    payload = {'pseudo': pseudo, 'action': [dx, dy]}
    try:
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
        print(f"Serveur: {data.get('message')}")
    except requests.RequestException as e:
        print(f"Erreur lors de l'envoi de l'action: {e}")

# Récupérer l'état du jeu (/state)
def get_state():
    url = f"{SERVER_URL}/state"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        print("État du plateau :")
        print(data.get('board'))
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération de l'état: {e}")

if __name__ == '__main__':
    while True:
        print("\n--- Menu HTTP ---")
        print("1. S'inscrire")
        print("2. Envoyer une action")
        print("3. Afficher état")
        print("4. Quitter")
        choice = input("Choix : ")

        if choice == '1':
            pseudo = input("Pseudo (1 lettre) : ").upper()
            role   = input("Rôle (wolf/villager) : ").lower()
            subscribe(pseudo, role)

        elif choice == '2':
            pseudo = input("Votre pseudo : ").upper()
            dx     = int(input("Déplacement X (-1,0,1) : "))
            dy     = int(input("Déplacement Y (-1,0,1) : "))
            send_action(pseudo, dx, dy)

        elif choice == '3':
            get_state()

        elif choice == '4':
            sys.exit(0)

        else:
            print("Choix invalide.")
