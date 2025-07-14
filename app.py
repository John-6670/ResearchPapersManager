from flask import Flask, request, jsonify
from redis_client import RedisClient

from database import Database
from utils import validate_user

app = Flask(__name__)

db = Database()
redis_client = RedisClient()


@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()

        username = data.get('username', '').strip()
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        department = data.get('department', '').strip()

        # Check for required fields
        if not all([username, name, email, password, department]):
            return jsonify({"error": "All fields are required"}), 400

        # Validate user data
        is_valid, error_message = validate_user(
            username=username, password=password,
            email=email, name=name, department=department
        )
        if not is_valid:
            return jsonify({"error": error_message}), 400

        if len(name) > 100 or len(email) > 100 or len(department) > 100:
            return jsonify({"error": "None of the fields can be more than 100 characters long."}), 400

        if redis_client.is_username_taken(username):
            return jsonify({"error": "This username is taken."}), 409

        # Create user in the database
        try:
            user_id = db.create_user(data)
            # Set the username as taken in Redis
            redis_client.mark_username_taken(username)

            return jsonify({
                "message": "User registered",
                "user_id": user_id
            }), 201

        except Exception as e:
            if "duplicate key" in str(e).lower():
                return jsonify({"error": "This username is taken."}), 409
            raise e

    except Exception as e:
        return jsonify({"error": "Unknown error accrued."}), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        username = data.get('username', '').strip()
        password = data.get('password', '')

        if not username or not password:
            return jsonify({"error": "All fields are required."}), 400

        user = db.get_user_by_username(username)

        if not (user or db.verify_password(password, user['password'])):
            return jsonify({"error": "Username or password is incorrect."}), 401

        return jsonify({
            "message": "Login successful",
            "user_id": str(user['_id'])
        }), 200

    except Exception as e:
        return jsonify({"error": "Unknown error accrued."}), 500


if __name__ == '__main__':
    app.run(debug=True)
