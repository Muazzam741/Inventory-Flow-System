from flask import Blueprint, request, jsonify
from models import Order, Product, db
from flask_jwt_extended import jwt_required

order_bp = Blueprint("order", __name__)

# Create a new order
@order_bp.route("/orders", methods=["POST"])
@jwt_required()
def create_order():
    data = request.json
    customer_name = data.get("customer_name")
    product_ids = data.get("product_ids", [])
    
    if not customer_name or not product_ids:
        return jsonify({"message": "Customer name and product IDs are required"}), 400
    
    # Fetch products from the database
    products = Product.query.filter(Product.id.in_(product_ids)).all()
    
    if len(products) != len(product_ids):
        return jsonify({"message": "Some products not found"}), 404
    
    total_amount = sum([p.price for p in products])

    new_order = Order(
        customer_name=customer_name,
        total_amount=total_amount,
        status="pending"
    )
    
    new_order.products = products
    
    db.session.add(new_order)
    db.session.commit()
    
    return jsonify({"message": "Order created successfully", "order_id": new_order.id}), 201

# Get all orders
@order_bp.route("/orders", methods=["GET"])
@jwt_required()
def get_all_orders():
    orders = Order.query.all()
    order_list = [
        {
            "id": o.id,
            "customer_name": o.customer_name,
            "status": o.status,
            "total_amount": o.total_amount,
            "products": [{"id": p.id, "name": p.name} for p in o.products]
        }
        for o in orders
    ]
    return jsonify(order_list), 200

# Get a single order by ID
@order_bp.route("/orders/<int:id>", methods=["GET"])
@jwt_required()
def get_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({"message": "Order not found"}), 404

    return jsonify({
        "id": order.id,
        "customer_name": order.customer_name,
        "status": order.status,
        "total_amount": order.total_amount,
        "products": [{"id": p.id, "name": p.name} for p in order.products]
    }), 200

# Update an order
@order_bp.route("/orders/<int:id>", methods=["PUT"])
@jwt_required()
def update_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({"message": "Order not found"}), 404
    
    data = request.json
    order.status = data.get("status", order.status)
    
    db.session.commit()
    
    return jsonify({"message": "Order updated successfully"}), 200

# Delete an order
@order_bp.route("/orders/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({"message": "Order not found"}), 404
    
    db.session.delete(order)
    db.session.commit()
    
    return jsonify({"message": "Order deleted successfully"}), 200
