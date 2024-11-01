# src/main/app.py

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
from logger import setup_logging
import logging

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Set up logging
setup_logging()

# Initialize the database
db = SQLAlchemy(app)

# Database model for User
class User(db.Model):
    """User  model for storing user information."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User  {self.username}>'

@app.route('/')
def home():
    return jsonify({"message": "Welcome to MatrixAI-Core API!"})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        logging.warning("Missing user data: %s", data)
        return jsonify({"error": "Missing username, email, or password"}), 400

    # Check if user already exists
    existing_user = User.query.filter((User .username == username) | (User .email == email)).first()
    if existing_user:
        logging.warning("User  already exists: %s", username)
        return jsonify({"error": "User  already exists"}), 409

    # Create new user
    new_user = User(username=username, email=email, password_hash=password)  # Hash the password in a real app
    db.session.add(new_user)
    db.session.commit()

    logging.info("User  created: %s", username)
    return jsonify({"message": "User  created successfully", "userId": new_user.id}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve user information by ID."""
    user = User.query.get(user_id)
    if not user:
        logging.warning("User  not found: %d", user_id)
        return jsonify({"error": "User  not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logging.error("Internal server error: %s", error)
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(host='0.0.0.0', port=5000)
