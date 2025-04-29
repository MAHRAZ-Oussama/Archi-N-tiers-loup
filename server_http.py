from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from models import Game, Wolf, Villager

game = Game(nb_max_turn=50, width=10, height=10)

class SimpleGameServer(BaseHTTPRequestHandler):

    def _send_response(self, status=200, body=None):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        if body is not None:
            self.wfile.write(json.dumps(body).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        if self.path == "/players":
            pseudo = data.get("pseudo")
            role = data.get("role")
            if not pseudo or not role:
                self._send_response(400, {"error": "pseudo and role required"})
                return

            if role == "wolf":
                player = Wolf(pseudo)
            else:
                player = Villager(pseudo)

            game._Game__gameboard.subscribe_player(player)
            self._send_response(200, {"message": f"{role} '{pseudo}' added"})

        elif self.path == "/action":
            pseudo = data.get("pseudo")
            action = tuple(data.get("action", (0, 0)))
            for row in game._Game__gameboard._GameBoard__content:
                for cell in row:
                    if isinstance(cell, (Wolf, Villager)) and cell.pseudo == pseudo:
                        game.register_action(cell, action)
                        game.process_action()
                        game._Game__gameboard.end_round()
                        self._send_response(200, {"message": "action processed"})
                        return
            self._send_response(404, {"error": "player not found"})

    def do_GET(self):
        if self.path == "/state":
            board = repr(game._Game__gameboard)
            self._send_response(200, {"board": board})

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleGameServer)
    print(f"Serveur HTTP démarré sur le port {port}")
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
 