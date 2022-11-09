from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    pictureUrl = db.Column(db.String(750), unique=False)
    price = db.Column(db.String(10), unique=False)
    type = db.Column(db.String(15), unique=False)

    def __init__(self, name, pictureUrl, price, type):
        self.name = name
        self.pictureUrl = pictureUrl
        self.price = price
        self.type = type


class CartItemSchema(ma.Schema):
    class Meta:
        fields = ('name', 'pictureUrl', 'price', 'type')


cartItem_schema = CartItemSchema()
cartItems_schema = CartItemSchema(many=True)

# Error Handler


@app.errorhandler(500)
def errorMessage(e):
    return jsonify(error=str(e)), 500

# Endpoint to create a merch item


@app.route('/merch-item', methods=["POST"])
def addCartItem():
    name = request.json['name']
    pictureUrl = request.json['pictureUrl']
    price = request.json['price']
    type = request.json['type']

    newCartItem = CartItem(name, pictureUrl, price, type)

    db.session.add(newCartItem)
    db.session.commit()

    cartItem = CartItem.query.get(newCartItem.id)

    return cartItem_schema.jsonify(cartItem)

# Endpoint to query all merch items


@app.route("/merch-items", methods=["GET"])
def getCartItems():
    allCartItems = CartItem.query.all()
    result = cartItems_schema.dump(allCartItems)
    return jsonify(result)

# Endpoint to query single merch item


@app.route("/merch-item/<id>", methods=["GET"])
def getCartItem(id):
    cartItem = CartItem.query.get(id)
    return cartItem_schema.jsonify(cartItem)

# Endpoint to update a merch item


@app.route('/merch-item/<id>', methods=["PUT"])
def updateCartItem(id):
    cartItem = CartItem.query.get(id)
    name = request.json['name']
    pictureUrl = request.json['pictureUrl']
    price = request.json['price']
    type = request.json['type']

    cartItem.name = name
    cartItem.pictureUrl = pictureUrl
    cartItem.price = price
    cartItem.type = type

    db.session.commit()
    return cartItem_schema.jsonify(cartItem)

# Endpoint to delete a merch item


@app.route('/merch-item/<id>', methods=["DELETE"])
def deleteCartItem(id):
    cartItem = CartItem.query.get(id)
    db.session.delete(cartItem)
    db.session.commit()

    return "Merch Item was successfully deleted"

# Endpoint to query for shirts


@app.route('/merch-items/shirt', methods=["GET"])
def getShirts():
    request = CartItem.query.filter_by(type='shirt')
    return cartItems_schema.jsonify(request)

# Endpoint to query for pants


@app.route('/merch-items/pants', methods=["GET"])
def getPants():
    request = CartItem.query.filter_by(type='pants')
    return cartItems_schema.jsonify(request)

# Endpoint to query for misc


@app.route('/merch-items/misc', methods=["GET"])
def getMisc():
    request = CartItem.query.filter_by(type='misc')
    return cartItems_schema.jsonify(request)


@app.route('/', methods=["GET"])
def test():
    request = CartItem.query.filter_by(type='shirt')
    return cartItems_schema.jsonify(request)


if __name__ == '__main__':
    app.run(debug=True)
