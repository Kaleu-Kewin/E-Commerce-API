from src import app, login_manager
from flask import request, make_response, jsonify, Response
from flask_login import login_user, login_required, logout_user
from src.models import User

"""
Arquivo contendo as rotas de:
- Carregar usuário
- Login
- Logout
"""

@login_manager.user_loader
def load_user(user_id: int) -> User | None:
    return User.query.get(int(user_id))


@app.route('/login', methods=['POST'])
def login() -> Response:
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()

    if user:
        if data.get('password') == user.password:
            login_user(user)
            return jsonify({'message': 'Usuário autenticado com sucesso.'})

    return make_response(jsonify({'message': 'Não autorizado. Credenciais inválidas.'}), 401)


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout realizado com sucesso.'})
