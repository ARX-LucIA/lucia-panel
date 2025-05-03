from flask import Flask, request, jsonify
import os, json
from datetime import datetime

app = Flask(__name__)
LOG_DIR = os.path.join(os.path.dirname(__file__), 'data', 'api_logs')
os.makedirs(LOG_DIR, exist_ok=True)

# Token de autenticación (puede cambiarse)
AUTH_TOKEN = "lucia2025supersegura"

def autorizado():
    token = request.args.get("token") or request.headers.get("Authorization")
    return token == AUTH_TOKEN

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok", "message": "API activa"}), 200

@app.route('/registrar', methods=['POST'])
def registrar():
    if not autorizado():
        return jsonify({"error": "No autorizado"}), 401

    data = request.json
    if not data:
        return jsonify({"error": "No se recibió JSON"}), 400

    fecha = datetime.now().strftime('%Y-%m-%d')
    hora = datetime.now().strftime('%H:%M:%S')
    data['fecha'] = f"{fecha} {hora}"

    log_file = os.path.join(LOG_DIR, f"{fecha}.json")
    logs = []
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            pass

    logs.append(data)
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

    return jsonify({"status": "registrado", "evento": data}), 200

@app.route('/leer', methods=['GET'])
def leer_logs():
    if not autorizado():
        return jsonify({"error": "No autorizado"}), 401

    fecha = request.args.get("fecha", datetime.now().strftime('%Y-%m-%d'))
    log_file = os.path.join(LOG_DIR, f"{fecha}.json")
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f)), 200
    return jsonify([]), 200

if __name__ == '__main__':
    app.run(port=5000)

