from flask import Flask
from flask_jwt_extended import JWTManager
from db import db
import os
from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from routes.order_routes import order_bp


app = Flask(__name__)

# Load Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'supersecretkey'  # Change this in production

# Initialize Extensions
db.init_app(app)
jwt = JWTManager(app)

# Register Blueprints (Routes)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(product_bp, url_prefix="/api")
app.register_blueprint(order_bp, url_prefix="/api")

# Create Database Tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
