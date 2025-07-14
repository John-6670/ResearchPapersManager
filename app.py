from flask import Flask, request, jsonify
from redis_client import RedisClient

from database import Database
from utils import validate_user, validate_paper

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
        missing_fields = [field for field, value in zip(['username', 'name', 'email', 'password', 'department'],
                                                       [username, name, email, password, department]) if not value]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

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


@app.route('/papers', methods=['POST'])
def upload_paper():
    try:
        user_id = request.headers.get('X-User-ID')
        if not user_id:
            return jsonify({"error": "Needs User session in header"}), 401

        user = db.get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "Session is invalid"}), 401

        data = request.get_json()

        is_valid, error_message = validate_paper(data)
        if not is_valid:
            return jsonify({"error": error_message}), 400

        citations = data.get('citations', [])
        if citations:
            for citation_id in citations:
                if not db.paper_exists(citation_id):
                    return jsonify({"error": f"There is no paper with {citation_id}"}), 404

        data['uploaded_by'] = str(user_id)
        paper_id = db.create_paper(data, citations)

        return jsonify({
            "message": "Paper uploaded",
            "paper_id": paper_id
        }), 201

    except Exception as e:
        return jsonify({"error": "Unknown error accrued."}), 500


@app.route('/papers', methods=['GET'])
def search_papers():
    try:
        search_term = request.args.get('search', '').strip()
        sort_by = request.args.get('sort_by', 'relevance')
        order = request.args.get('order', 'desc')

        if sort_by not in ['relevance', 'publication_date']:
            return jsonify({"error": "sort_by parameter should be either relevance or publication_date"}), 400

        if order not in ['asc', 'desc']:
            return jsonify({"error": "order parameter should be either asc or desc"}), 400

        # Check cache for the search result
        cached_result = redis_client.get_search_cache(search_term, sort_by, order)
        if cached_result:
            return jsonify({"papers": cached_result}), 200

        # Search papers in the database
        papers = db.search_papers(search_term, sort_by, order)

        result_papers = []
        for paper in papers:
            result_papers.append({
                "id": str(paper['_id']),
                "title": paper['title'],
                "authors": paper['authors'],
                "publication_date": paper['publication_date'],
                "journal_conference": paper.get('journal_conference', ''),
                "keywords": paper['keywords']
            })

        # Cache the result
        redis_client.set_search_cache(search_term, sort_by, order, result_papers)

        return jsonify({"papers": result_papers}), 200

    except Exception as e:
        return jsonify({"error": e}), 500


if __name__ == '__main__':
    app.run(debug=True)
