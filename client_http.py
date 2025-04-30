import http.client
import json
import sys

class WerewolfClient:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.conn = http.client.HTTPConnection(self.host, self.port)
        self.pseudo = None

    def _request(self, method, path, body=None):
        headers = {'Content-Type': 'application/json'} if body else {}
        payload = json.dumps(body) if body else None
        self.conn.request(method, path, payload, headers)
        response = self.conn.getresponse()
        raw = response.read().decode()
        if response.status >= 400:
            print(f"[Erreur HTTP {response.status}] {raw}")
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            print("[Erreur] réponse non-JSON :", raw)
            return None

    def subscribe(self, pseudo, role):
        """S'inscrire et mémoriser le pseudo."""
        resp = self._request('POST', '/players', {'pseudo': pseudo, 'role': role})
        if resp and 'message' in resp:
            print(f"Serveur: {resp['message']}")
            self.pseudo = pseudo
        else:
            print("Échec de l'inscription.")

    def send_action(self, dx, dy):
        """Envoyer un déplacement pour le pseudo inscrit."""
        if not self.pseudo:
            print("❗ Vous devez d'abord vous inscrire (option 1).")
            return
        resp = self._request('POST', '/action', {'pseudo': self.pseudo, 'action': [dx, dy]})
        if resp and 'message' in resp:
            print(f"Serveur: {resp['message']}")
        else:
            print("Échec de l'envoi de l'action.")

    def get_state(self):
        """Récupérer et afficher l'état du plateau et des joueurs en grille carrée."""
        resp = self._request('GET', '/state')
        if not resp:
            return
        turn = resp.get('turn')
        max_turns = resp.get('nb_max_turn')
        board = resp.get('board', [])
        players = resp.get('players', [])

        height = len(board)
        width = len(board[0]) if height > 0 else 0

        # Affichage des coordonnées X
        header = '    ' + '   '.join(f'{i:2}' for i in range(width))
        print(f"\n Tour {turn}/{max_turns}")
        print(header)

        # Ligne horizontale
        sep = '   +' + '---+' * width
        print(sep)

        # Affichage des lignes doublées pour carré
        for y, row in enumerate(board):
            row_display = ' | '.join(cell.center(1) for cell in row)
            line = f'{y:2} | ' + row_display + ' |'
            # Afficher deux fois chaque ligne
            print(line)
            print(line)
            print(sep)

        # Liste des joueurs
        print("Joueurs :")
        for p in players:
            x, y = p.get('position', [None, None])
            print(f"  • {p['pseudo']} ({p['role']}) en ({x},{y})")

    def list_games(self):
        """Lister les parties en attente."""
        resp = self._request('GET', '/games')
        if not resp:
            return
        print("\n🔎 Parties en attente :")
        for idx, g in enumerate(resp.get('games', []), 1):
            print(f"   {idx}. {g}")


def main():
    client = WerewolfClient()
    while True:
        print("\n--- Menu HTTP ---")
        print("1. S'inscrire")
        print("2. Envoyer une action")
        print("3. Afficher état")
        print("4. Lister parties")
        print("5. Quitter")
        choice = input("Choix : ").strip()

        if choice == '1':
            pseudo = input("Pseudo (1 lettre) : ").upper()
            role   = input("Rôle (wolf/villager) : ").lower()
            client.subscribe(pseudo, role)

        elif choice == '2':
            dx = int(input("Déplacement X (-1,0,1) : "))
            dy = int(input("Déplacement Y (-1,0,1) : "))
            client.send_action(dx, dy)

        elif choice == '3':
            client.get_state()

        elif choice == '4':
            client.list_games()

        elif choice == '5':
            print("Au revoir !")
            sys.exit(0)

        else:
            print("Choix invalide.")

if __name__ == '__main__':
    main()