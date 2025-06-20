from flask import Flask, request, make_response, jsonify, Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)

class Product(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(120), nullable=False)
    price       = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    def __init__(self, name: str, price, description: str) -> None:
        self.name        = name
        self.price       = price
        self.description = description

@app.route('/api/products/add', methods=['POST'])
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


if __name__ == '__main__':
    app.run(debug=True)

