from flask import Blueprint, request, jsonify
from models import Product
from db import db
from flask_jwt_extended import jwt_required

product_bp = Blueprint("product", __name__)

# Add a new product
@product_bp.route("/products", methods=["POST"])
@jwt_required()
def add_product():
    data = request.json
    if not data.get("name") or not data.get("price") or not data.get("quantity"):
        return jsonify({"message": "Name, price, and quantity are required"}), 400

    new_product = Product(
        name=data["name"],
        description=data.get("description", ""),
        price=float(data["price"]),
        quantity=int(data["quantity"])
    )

    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added successfully"}), 201

# Get all products
@product_bp.route("/products", methods=["GET"])
@jwt_required()
def get_all_products():
    products = Product.query.all()
    product_list = [
        {"id": p.id, "name": p.name, "description": p.description, "price": p.price, "quantity": p.quantity}
        for p in products
    ]
    return jsonify(product_list), 200

# Get a single product by ID
@product_bp.route("/products/<int:id>", methods=["GET"])
@jwt_required()
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    return jsonify({"id": product.id, "name": product.name, "description": product.description, 
                    "price": product.price, "quantity": product.quantity}), 200

# Update a product
@product_bp.route("/products/<int:id>", methods=["PUT"])
@jwt_required()
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    data = request.json
    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description)
    product.price = float(data.get("price", product.price))
    product.quantity = int(data.get("quantity", product.quantity))

    db.session.commit()
    return jsonify({"message": "Product updated successfully"}), 200

# Delete a product
@product_bp.route("/products/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"}), 200

@product_bp.route("/products/<int:id>/increase_stock", methods=["PATCH"])
@jwt_required()
def increase_stock(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    
    data = request.json
    request_quantity = data.get("quantity")
    
    if request_quantity is None or request_quantity <= 0:
        return jsonify({"message": "Quantity must be greater than 0"}), 400
    
    product.quantity += request_quantity
    db.session.commit()
    
    return jsonify({"message": f"Stock for {product.name} increased by {request_quantity}. New stock: {product.quantity}"}), 200

# Decrease stock for a product
@product_bp.route("/products/<int:id>/decrease_stock", methods=["PATCH"])
@jwt_required()
def decrease_stock(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    
    data = request.json
    request_quantity = data.get("quantity")
    
    if request_quantity is None or request_quantity <= 0:
        return jsonify({"message": "Quantity must be greater than 0"}), 400
    
    if product.quantity < request_quantity:
        return jsonify({"message": "Insufficient stock"}), 400
    
    product.quantity -= request_quantity
    db.session.commit()
    
    return jsonify({"message": f"Stock for {product.name} decreased by {request_quantity}. New stock: {product.quantity}"}), 200