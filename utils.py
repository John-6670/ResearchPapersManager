import re
from datetime import datetime


def validate_username(username):
    if not username or len(username) < 3 or len(username) > 20:
        return False
    return re.match(r'^[a-zA-Z0-9_]+$', username) is not None


def validate_password(password):
    if not password or len(password) < 8:
        return False
    return True


def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_date(date_string):
    try:
        datetime.fromisoformat(date_string)
        return True
    except:
        return False


def validate_user(**kwargs):
    for key, value in kwargs.items():
        if key == 'username':
            if not validate_username(value):
                return False, "Invalid username. Must be 3-20 characters long and contain only letters, numbers, and underscores."
        elif key == 'password':
            if not validate_password(value):
                return False, "Password must be at least 8 characters long."
        elif key == 'email':
            if not validate_email(value):
                return False, "Invalid email format."
        elif key == 'date':
            if not validate_date(value):
                return False, "Invalid date format. Use ISO format (YYYY-MM-DD)."
    return True, ""


def convert_objectid_to_str(doc):
    if doc:
        doc['_id'] = str(doc['_id'])
        if 'uploaded_by' in doc:
            doc['uploaded_by'] = str(doc['uploaded_by'])
    return doc