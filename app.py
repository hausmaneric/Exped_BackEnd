from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from models.entrega import *
from models.evento import *
from itsdangerous import URLSafeSerializer, BadSignature

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = 'sigexped'
cors = CORS(app, resources={r"/api/*": {"origins": "*", "methods": "GET, POST, PUT, DELETE", "headers": "Origin, Content-Type, X-Auth-Token, charset=utf-8"}})

def generate_token(data):
    s = URLSafeSerializer(app.config['SECRET_KEY'])
    return s.dumps(data)

def verify_token(token):
    s = URLSafeSerializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
        return data
    except BadSignature:
        return None  

def require_token(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        print(request.headers)

        if not token or not token.startswith('Bearer '):
            return jsonify({'_message': 'Token não fornecido ou inválido.'}), 401

        token = token.replace('Bearer ', '')
        data = verify_token(token)
        if not data:
            return jsonify({'_message': 'Token inválido.'}), 401

        return func(token, *args, **kwargs)

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper

@app.route('/')
def main():
    return 'API OK 0.1.4'

@app.route('/api/token', methods=['POST'])
def get_token():
    if request.is_json:
        data = request.get_json()
        token = generate_token(data)
        return jsonify({'token': token})
    else:
        return jsonify({'_message': 'Requisição inválida. É necessário enviar um corpo JSON.'}), 400

#region Entrega
@app.route('/api/entrega/', methods=['GET', 'POST'])
@app.route('/api/entrega/<id>', methods=['GET', 'PUT'])
@require_token
def entrega(token, id=''):
    if request.method == 'GET':
        if id:
            return getEntrega(id)
        else:
            return jsonify({'_message': 'Requisição inválida. É necessário enviar um parâmetro.'}), 405
    elif request.method == 'POST':
        if request.is_json:
            entrega_data = request.get_json()
            entrega = Entrega(
                id          = entrega_data.get('id'),
                cnpj        = entrega_data.get('cnpj'),
                venda       = entrega_data.get('venda'),
                entrega     = entrega_data.get('entrega'),
                status      = entrega_data.get('status'),
                previsao    = entrega_data.get('previsao'),
            )
            return postEntrega(entrega)
        else:
            return jsonify({'_message': 'Requisição inválida. É necessário enviar um corpo JSON.'}), 400
    elif request.method == 'PUT':
        if request.is_json:
            entrega_data = request.get_json()
            entrega = Entrega(
                id          = entrega_data.get('id'),
                cnpj        = entrega_data.get('cnpj'),
                venda       = entrega_data.get('venda'),
                entrega     = entrega_data.get('entrega'),
                status      = entrega_data.get('status'),
                previsao    = entrega_data.get('previsao'),
            )
            return updateEntrega(id, entrega)
        else:
            return jsonify({'_message': 'Requisição inválida. É necessário enviar um corpo JSON.'}), 400

@app.route('/api/entregatoken/<id>', methods=['GET'])
@require_token
def entrega_by_token(token,id=''):
    if id:
        return getEntregaToken(id)
    else:
        return jsonify({'_message': 'Token inválido.'}), 401
#endregion

#region Evento
@app.route('/api/evento/', methods=['GET', 'POST'])
@app.route('/api/evento/<id>', methods=['GET', 'PUT'])
@require_token
def evento(token, id=''):
    if request.method == 'GET':
        if id:
            return getEvento(id)
        else:
            return jsonify({'_message': 'Requisição inválida. É necessário enviar um parâmetro.'}), 405
    elif request.method == 'POST':
        if request.is_json:
            evento_data = request.get_json()
            evento = Evento(
                id      = evento_data.get('id'),
                evento  = evento_data.get('evento'),
                entrega = evento_data.get('entrega'),
                tipo    = evento_data.get('tipo'),
                data    = evento_data.get('data'),
                hora    = evento_data.get('hora'),
            )
            return postEvento(evento)
        else:
            return jsonify({'_message': 'Requisição inválida. É necessário enviar um corpo JSON.'}), 400
    elif request.method == 'PUT':
        if request.is_json:
            evento_data = request.get_json()
            evento = Evento(
                id      = evento_data.get('id'),
                evento  = evento_data.get('evento'),
                entrega = evento_data.get('entrega'),
                tipo    = evento_data.get('tipo'),
                data    = evento_data.get('data'),
                hora    = evento_data.get('hora'),
            )
            return updateEvento(id, evento)
        else:
            return jsonify({'_message': 'Requisição inválida. É necessário enviar um corpo JSON.'}), 400

@app.route('/api/eventoentrega/<entrega>', methods=['GET', 'PUT'])
@require_token
def eventoentrega(token, entrega=''):
    if request.method == 'GET':
        return getEventoEntrega(entrega)
    elif request.method == 'PUT':
        if request.is_json:
            evento_data = request.get_json()
            evento = Evento(
                id      = evento_data.get('id'),
                evento  = evento_data.get('evento'),
                entrega = evento_data.get('entrega'),
                tipo    = evento_data.get('tipo'),
                data    = evento_data.get('data'),
                hora    = evento_data.get('hora'),
            )
            return updateEventoEntrega(entrega, evento)
        else:
            return jsonify({'_message': 'Requisição inválida. É necessário enviar um corpo JSON.'}), 400

@app.route('/api/eventovenda/<venda>', methods=['GET'])
@require_token
def eventovenda(token, venda=0):
    if venda:
        return getEventoevento(venda)
    else:
        return jsonify({'_message': 'Requisição inválida. É necessário enviar um parâmetro.'}), 405
#endregion

if __name__ == '__main__':
    app.run(host="0.0.0.0")
