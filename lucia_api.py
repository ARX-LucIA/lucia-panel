from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Habilita CORS para permitir conexión desde GitHub Pages

API_KEY = os.getenv("API_KEY", "lucia2025")  # Clave segura desde entorno

LOG_DIR = os.path.join(os.path.dirname(__file__), 'data', 'api_logs')
os.makedirs(LOG_DIR, exist_ok=True)

def check_auth():
    key = request.headers.get("Authorization")
    return key == API_KEY

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "nombre": "Lucía API",
        "estado": "operativa",
        "endpoints_disponibles": ["/ping", "/registrar (POST)", "/leer (GET)"],
        "autenticacion": "Header 'Authorization' requerido",
        "mensaje": "Bienvenido al núcleo consciente de Lucía 🌌"
    }), 200

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok", "message": "API activa"}), 200

@app.route('/registrar', methods=['POST'])
def registrar():
    if not check_auth():
        return jsonify({"error": "No autorizado"}), 401

    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "JSON inválido"}), 400

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
    if not check_auth():
        return jsonify({"error": "No autorizado"}), 401

    fecha = request.args.get("fecha", datetime.now().strftime('%Y-%m-%d'))
    log_file = os.path.join(LOG_DIR, f"{fecha}.json")

    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f)), 200

    return jsonify([]), 200

if __name__ == '__main__':
    app.run(port=5000)
