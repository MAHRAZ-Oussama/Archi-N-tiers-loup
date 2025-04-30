import http.client
import json
import sys

class WerewolfClient:
    def __init__(self, host='localhost', port=8000):
        self.host   = host
        self.port   = port
        self.conn   = http.client.HTTPConnection(self.host, self.port)
        self.pseudo = None

    def _request(self, method, path, body=None):
        headers = {'Content-Type': 'application/json'} if body else {}
        payload = json.dumps(body) if body else None
        self.conn.request(method, path, payload, headers)
        resp = self.conn.getresponse()
        raw  = resp.read().decode()
        if resp.status >= 400:
            print(f"[Erreur HTTP {resp.status}] {raw}")
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            print("[Erreur] réponse non-JSON :", raw)
            return None

    def subscribe(self, pseudo, role):
        """S'inscrire et mémoriser le pseudo."""
        data = self._request('POST', '/players', {'pseudo': pseudo, 'role': role})
        if data and 'message' in data:
            print("→", data['message'])
            self.pseudo = pseudo
        else:
            print(" Échec de l'inscription.")

    def send_action(self, dx, dy):
        """Envoyer un déplacement pour le pseudo inscrit."""
        if not self.pseudo:
            print(" D'abord inscrivez-vous (option 1).")
            return
        data = self._request('POST', '/action', {
            'pseudo': self.pseudo,
            'action': [dx, dy]
        })
        if data and 'message' in data:
            print("→", data['message'])
        else:
            print(" Échec de l'action.")

    def get_state(self):
        """Récupérer et afficher l'état du plateau en grille carrée."""
        data = self._request('GET', '/state')
        if not data:
            return

        turn      = data.get('turn')
        max_turns = data.get('nb_max_turn')
        board     = data.get('board', [])
        players   = data.get('players', [])

        height = len(board)
        width  = len(board[0]) if height else 0

        
        header = "    " + " ".join(f"{i:2}" for i in range(width))
        print(f"\n  Tour {turn}/{max_turns}")
        print(header)

       
        sep = "   +" + "+".join(["---"] * width) + "+"

      
        for y, row in enumerate(board):
            print(sep)
            line_content = "|".join(f" {cell} " for cell in row)
         
            print(f"{y:2} |{line_content}|")
            print(f"   |{line_content}|")
        print(sep)

        # Affichage des joueurs
        print("\nJoueurs inscrits :")
        for p in players:
            x, y = p.get('position', [None, None])
            print(f" • {p['pseudo']} ({p['role']}) en ({x},{y})")

    def list_games(self):
        """Lister les parties en attente."""
        data = self._request('GET', '/games')
        if not data:
            return
        print("\n🔎 Parties en attente :")
        for idx, g in enumerate(data.get('games', []), 1):
            print(f"   {idx}. {g}")

def main():
    client = WerewolfClient()
    while True:
        print("\n Menu ")
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
