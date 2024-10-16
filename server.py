from flask import Flask, request, jsonify
import requests
import os
from base64 import b64encode
from dotenv import load_dotenv
from flask_cors import CORS  # Importando a biblioteca CORS

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()  

app = Flask(__name__)
CORS(app)  # Habilitando CORS para todas as rotas

# Verificando a variável de ambiente
secret_key = os.environ.get('SECRET_KEY')
# Definindo a URL base da API do Pagar.me
BASE_URL = "https://api.pagar.me/core/v5"

# Configurando o token de autenticação
AUTH_TOKEN = b64encode(f"{secret_key}:".encode()).decode()

print("token: " + AUTH_TOKEN)

@app.route('/pagarme/<path:endpoint>', methods=['GET', 'POST'])
def pagarme(endpoint):
    # Capturando os parâmetros de consulta
    query_params = request.query_string.decode()  # Obtendo os parâmetros de consulta
    url = f"{BASE_URL}/{endpoint.lstrip('/')}"
    
    # Adicionando os parâmetros de consulta à URL
    if query_params:
        url += f"?{query_params}"

    print("URL chamada: ", url)  # Exibindo a URL completa
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {AUTH_TOKEN}',
    }

    if request.method == 'GET':
        try:
            response = requests.get(url, headers=headers)
            return jsonify(response.json()), response.status_code
        except requests.exceptions.RequestException as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == 'POST':
        data = request.json  # Obter os dados JSON do corpo da requisição
        try:
            response = requests.post(url, headers=headers, json=data)
            return jsonify(response.json()), response.status_code
        except requests.exceptions.RequestException as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
