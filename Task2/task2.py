from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import bcrypt
from dotenv import load_dotenv
import os

# download values from file .env
load_dotenv()

app = Flask(__name__)

#make database uding ORM (SQLAlchemy)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

db = SQLAlchemy(app)
jwt = JWTManager(app)

#Users Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Prodacts Table
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pname = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

# Tables will creat automatically
with app.app_context():
    db.create_all()

#main page
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the API!", "endpoints": ["/signup", "/login", "/products"]})

# sign up new user
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    if not data or "name" not in data or "username" not in data or "password" not in data:
        return jsonify({"error": "Missing name, username, or password"}), 400

    hashed_password = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())

    new_user = User(name=data["name"], username=data["username"], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# login and return JWT Token valid for 10 minutes
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Missing username or password"}), 400

    user = User.query.filter_by(username=data["username"]).first()

    if not user or not bcrypt.checkpw(data["password"].encode("utf-8"), user.password.encode("utf-8")):
        return jsonify({"error": "Invalid username or password"}), 401

    token = create_access_token(identity=str(user.id), expires_delta=timedelta(minutes=10))
    return jsonify({"token": token})

#update users data
@app.route("/users/<int:id>", methods=["PUT"])
@jwt_required()
def update_user(id):
    current_user = get_jwt_identity()
    user = User.query.get(id)

    if not user or user.id != int(current_user):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    user.name = data.get("name", user.name)
    user.username = data.get("username", user.username)

    db.session.commit()
    return jsonify({"message": "User updated successfully"})

#add product that require JWT
@app.route("/products", methods=["POST"])
@jwt_required()
def add_product():
    data = request.get_json()

    if not data or "pname" not in data or "price" not in data or "stock" not in data:
        return jsonify({"error": "Missing product details"}), 400

    new_product = Product(
        pname=data["pname"],
        description=data.get("description", ""),
        price=float(data["price"]),
        stock=int(data["stock"]),
        user_id=get_jwt_identity()
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product added successfully"}), 201

# show all products
@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([{
        "id": p.id, "pname": p.pname, "description": p.description,
        "price": p.price, "stock": p.stock, "created_at": p.created_at
    } for p in products])

# show one product with its ID
@app.route("/products/<int:pid>", methods=["GET"])
def get_product(pid):
    product = Product.query.get(pid)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({
        "id": product.id, "pname": product.pname, "description": product.description,
        "price": product.price, "stock": product.stock, "created_at": product.created_at
    })

# update product
@app.route("/products/<int:pid>", methods=["PUT"])
@jwt_required()
def update_product(pid):
    product = Product.query.get(pid)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    product.pname = data.get("pname", product.pname)
    product.description = data.get("description", product.description)
    product.price = data.get("price", product.price)
    product.stock = data.get("stock", product.stock)

    db.session.commit()
    return jsonify({"message": "Product updated successfully"})

# delete product
@app.route("/products/<int:pid>", methods=["DELETE"])
@jwt_required()
def delete_product(pid):
    product = Product.query.get(pid)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)



