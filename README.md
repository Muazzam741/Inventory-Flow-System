
# Inventory Flow System

A Flask-based Inventory Management System with RESTful APIs to manage products, orders, and stock. This project allows users to add, update, and delete products, as well as manage stock levels.

## Features
- User authentication (JWT-based)
- Product management (CRUD operations)
- Stock management (Increase/Decrease stock)
- Order management
- SQLite as the database

## Technologies Used
- Python
- Flask
- SQLAlchemy (ORM for database)
- Flask-JWT-Extended (JWT for authentication)
- SQLite (Database)

## Prerequisites
- Python 3.6+ installed
- Pip (Python package installer)
- Virtual environment (optional but recommended)

## Getting Started

Follow these steps to get the project up and running on your local machine.

### 1. Clone the Repository

Clone this repository to your local machine using Git:

```bash
git clone https://github.com/muazzam741/inventory-flow-system.git
cd inventory-flow-system
```

### 2. Set Up Virtual Environment (optional but recommended)

It's recommended to use a virtual environment to isolate project dependencies.

```bash
python3 -m venv venv
```

Activate the virtual environment:

- **For macOS/Linux:**

```bash
source venv/bin/activate
```

- **For Windows:**

```bash
venv\Scriptsctivate
```

### 3. Install Dependencies

Install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Set Up the Database

Run the following command to create the SQLite database and initialize the tables:

```bash
python app.py
```

This will create the necessary tables in the `inventory.db` SQLite database.

### 5. Run the Application

Start the Flask development server:

```bash
python app.py
```

The app will be running at `http://127.0.0.1:5000`.

### 6. Test the API

You can test the following API routes using tools like Postman or curl:

- **User Authentication** (JWT):
  - `POST /auth/login` – Login to get the JWT token.

- **Product Management**:
  - `POST /api/products` – Add a new product.
  - `GET /api/products` – Get all products.
  - `GET /api/products/<id>` – Get a single product by ID.
  - `PUT /api/products/<id>` – Update a product.
  - `DELETE /api/products/<id>` – Delete a product.
  - `PATCH /api/products/<id>/increase_stock` – Increase stock for a product.
  - `PATCH /api/products/<id>/decrease_stock` – Decrease stock for a product.

### 7. Example Usage

1. **Login:**

```bash
POST /auth/login
```
- Request Body:
  ```json
  {
    "username": "yourusername",
    "password": "yourpassword"
  }
  ```

- Response:
  ```json
  {
    "access_token": "your_jwt_token_here"
  }
  ```

2. **Add a Product:**

```bash
POST /api/products
```
- Request Body:
  ```json
  {
    "name": "Product Name",
    "price": 19.99,
    "quantity": 100,
    "description": "Product description"
  }
  ```

- Response:
  ```json
  {
    "message": "Product added successfully"
  }
  ```

### 8. Additional Information

- You can find the project structure below:

```
inventory-flow-system/
├── app.py             # Flask application entry point
├── models.py          # SQLAlchemy models
├── routes/            # API routes
│   ├── auth_routes.py # Authentication routes
│   └── product_routes.py # Product management routes
├── db.py              # Database setup
├── requirements.txt   # Project dependencies
└── .gitignore         # Git ignore file
```

### 9. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Happy coding! 🎉
