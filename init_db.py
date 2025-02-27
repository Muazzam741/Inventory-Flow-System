from app import app, db

# Initialize the app context and create all tables
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
