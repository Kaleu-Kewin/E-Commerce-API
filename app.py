import os

from flask import Flask, request, make_response, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager()

db = SQLAlchemy(app)

login_manager.init_app(app)
login_manager.login_view = 'login' # type: ignore

CORS(app)

class Product(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(120), nullable=False)
    price       = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    def __init__(self, name: str, price, description: str) -> None:
        self.name        = name
        self.price       = price
        self.description = description


class User(db.Model, UserMixin):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password


@app.route('/api/products/add', methods=['POST'])
@login_required
def add_product() -> Response:
    data = request.get_json()

    if data and 'name' in data and 'price' in data:
        product = Product(
            name=data['name'],
            price=data['price'],
            description=data.get('description', '') # usando get() para evitar erro caso 'description' não esteja presente no JSON
        )
        db.session.add(product)
        db.session.commit()
        return make_response(jsonify({'message': 'Produto cadastrado com sucesso!'}), 201)

    return make_response(jsonify({'error': 'Dados inválidos ou incompletos'}), 400)


@app.route('/api/products/delete/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id: int) -> Response:
    product = Product.query.get(product_id)

    if product:
        db.session.delete(product)
        db.session.commit()
        return make_response(jsonify({'message': 'Produto deletado com sucesso!'}), 200)

    return make_response(jsonify({'error': 'Produto não encontrado!'}), 404)


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_products_details(product_id: int) -> Response:
    product = Product.query.get(product_id)

    if product:
        return jsonify({
            'id'          : product.id,
            'name'        : product.name,
            'price'       : product.price,
            'description' : product.description
        })

    return make_response(jsonify({'error': 'Produto não encontrado!'}), 404)


@app.route('/api/products/update/<int:product_id>', methods=['PUT'])
@login_required
def update_product(product_id: int) -> Response:
    product = Product.query.get(product_id)

    if not product:
        return make_response(jsonify({'error': 'Produto não encontrado!'}), 404)

    data = request.get_json()

    if data:
        if 'id' in data:
            return make_response(jsonify({'error': 'Não é possível atualizar o "id"!'}), 400)
        if 'name' in data:
            product.name = data['name']
        if 'price' in data:
            product.price = data['price']
        if 'description' in data:
            product.description = data['description']
        db.session.commit()

    return make_response(jsonify({'message': 'Produto atualizado com sucesso!'}), 200)


@app.route('/api/products', methods=['GET'])
def get_products() -> Response:
    products     = Product.query.all()
    product_list = []

    for p in products:
        product = {
            'id'          : p.id,
            'name'        : p.name,
            'price'       : p.price,
            'description' : p.description
        }
        product_list.append(product)

    if not product_list:
        return make_response(jsonify({'message': 'Nenhum produto encontrado!'}), 404)

    return jsonify(product_list)


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


if __name__ == '__main__':
    app.run(debug=True)

