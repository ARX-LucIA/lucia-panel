
from flask import Flask, request, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

LOG_DIR = os.path.join(os.path.dirname(__file__), 'data', 'api_logs')
os.makedirs(LOG_DIR, exist_ok=True)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok", "message": "API activa"}), 200

@app.route('/registrar', methods=['POST'])
def registrar():
    data = request.json
    if not data:
        return jsonify({"error": "No se recibió JSON"}), 400

    fecha = datetime.now().strftime('%Y-%m-%d')
    hora = datetime.now().strftime('%H:%M:%S')
    data['fecha'] = f"{fecha} {hora}"
    
    log_file = os.path.join(LOG_DIR, f"{fecha}.json")
    
    logs = []
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

    logs.append(data)

    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

    return jsonify({"status": "registrado", "evento": data}), 200

@app.route('/leer', methods=['GET'])
def leer_logs():
    fecha = request.args.get("fecha", datetime.now().strftime('%Y-%m-%d'))
    log_file = os.path.join(LOG_DIR, f"{fecha}.json")
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f)), 200
    return jsonify([]), 200

if __name__ == '__main__':
    app.run(port=5000)
@app.route('/', methods=['GET'])
def raiz():
    return jsonify({"mensaje": "Bienvenido a la API de Lucía 💫"}), 200
