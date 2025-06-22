from run   import app
from flask import request, make_response, jsonify, Response
from flask_login  import login_required
from src.database import db
from src.models   import Product

"""
Arquivo contendo as rotas de:
- Adicionar produtos
- Deletar produtos
- Atualizar produtos
- Buscar um produto específico
- Listar todos os produtos
"""

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
