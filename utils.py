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


def validate_paper(paper_data):
    if not paper_data.get('title') or len(paper_data['title']) > 200:
        return False, "Title is required and must be less than 200 characters."

    if not paper_data.get('abstract') or len(paper_data['abstract']) > 1000:
        return False, "Abstract is required and must be less than 1000 characters."

    if not paper_data.get('publication_date') or not validate_date(paper_data['publication_date']):
        return False, "Publication date is required and must be in ISO format (YYYY-MM-DD)."

    authors = paper_data.get('authors', [])
    if 1 <= len(authors) <= 5:
        for authors in authors:
            if len(authors) > 100:
                return False, "Each author must be a non-empty string with a maximum length of 100 characters."
    else:
        return False, "There must be between 1 and 5 authors."

    if len(paper_data.get('journal_conference', '')) > 200:
        return False, "Journal or conference name must be less than 200 characters."

    keywords = paper_data.get('keywords', [])
    if 1 <= len(keywords) <= 5:
        for keyword in keywords:
            if not keyword or len(keyword) > 50:
                return False, "Each keyword must be a non-empty string with a maximum length of 50 characters."
    else:
        return False, "There must be between 1 and 5 keywords."

    citations = paper_data.get('citations', [])
    if citations:
        if len(citations) > 5:
            return False, "A paper can have a maximum of 5 citations."

    return True, ""


def convert_objectid_to_str(doc):
    if doc:
        doc['_id'] = str(doc['_id'])
        if 'uploaded_by' in doc:
            doc['uploaded_by'] = str(doc['uploaded_by'])
    return doc
