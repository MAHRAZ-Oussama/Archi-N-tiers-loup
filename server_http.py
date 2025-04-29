from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    pseudo = data.get('pseudo')
    role   = data.get('role')
    if not pseudo or role not in ('wolf', 'villager'):
        return jsonify({'status': 'error', 'message': 'Paramètres invalides.'}), 400
    return jsonify({
        'status': 'success',
        'message': f"Joueur {pseudo} inscrit en tant que {role}."
    })

@app.route('/action', methods=['POST'])
def action():
    data = request.get_json()
    pseudo = data.get('pseudo')
    action = data.get('action')
    if (not pseudo or
        not isinstance(action, list) or
        len(action) != 2 or
        any(d not in (-1,0,1) for d in action)):
        return jsonify({'status': 'error', 'message': 'Paramètres invalides.'}), 400
    return jsonify({
        'status': 'success',
        'message': f"Joueur {pseudo} a effectué un déplacement {action}."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
