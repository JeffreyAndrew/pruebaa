from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc

from project.api.models import Smartphone
from project import db


smartphones_blueprint = Blueprint(
    'smartphones', __name__, template_folder='./templates')


@smartphones_blueprint.route('/smartphones/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'estado': 'satisfactorio',
        'mensaje': 'pong!'
    })


@smartphones_blueprint.route('/smartphones', methods=['POST'])
def add_smartphone():
    post_data = request.get_json()
    response_object = {
        'estado': 'falló',
        'mensaje': 'Datos no validos.'
    }
    if not post_data:
        return jsonify(response_object), 400

    name = post_data.get('name')
    brand = post_data.get('brand')
    price = post_data.get('price')
    quantity = post_data.get('quantity')
    color = post_data.get('color')
    try:
        smartphone = Smartphone.query.filter_by(brand=brand).first()
        if not smartphone:
            db.session.add(Smartphone(
                name=name, brand=brand, price=price,
                quantity=quantity, color=color))
            db.session.commit()
            response_object['estado'] = 'satisfactorio'
            response_object['mensaje'] = f'{brand} fue agregado!!!'
            return jsonify(response_object), 201
        else:
            response_object['mensaje'] = 'Disculpe, ese smartphone ya existe.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@smartphones_blueprint.route('/smartphones/<smartphone_id>', methods=['GET'])
def get_single_smartphone(smartphone_id):
    """Obteniendo detalles del usuario único"""
    response_object = {
        'estado': 'falló',
        'mensaje': 'El smartphone no existe'
    }
    try:
        smartphone = Smartphone.query.filter_by(
            idSmartphone=int(smartphone_id)).first()
        if not smartphone:
            return jsonify(response_object), 404
        else:
            response_object = {
                'estado': 'satisfactorio',
                'data': {
                    'idSmartphone': smartphone.idSmartphone,
                    'name': smartphone.name,
                    'brand': smartphone.brand,
                    'price': smartphone.price,
                    'quantity': smartphone.quantity,
                    'color': smartphone.color
                    }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@smartphones_blueprint.route('/smartphones', methods=['GET'])
def get_all_smartphones():
    """Obteniendo todos los smartphones"""
    response_object = {
        'estado': 'satisfactorio',
        'data': {
            'smartphones': [
                smartphone.to_json() for smartphone in Smartphone.query.all()]
        }
    }
    return jsonify(response_object), 200


@smartphones_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        brand = request.form['brand']
        price = request.form['price']
        quantity = request.form['quantity']
        color = request.form['color']
        db.session.add(Smartphone(
            name=name, brand=brand, price=price,
            quantity=quantity, color=color))
        db.session.commit()
    smartphones = Smartphone.query.all()
    return render_template('index.html', smartphones=smartphones)
