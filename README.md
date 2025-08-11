# Research Papers Manager

A comprehensive Flask-based web application for managing academic research papers with advanced search capabilities, user management, and intelligent caching system.

## 🎯 Overview

Research Papers Manager is a robust backend system designed to help researchers, academic institutions, and libraries organize, search, and manage academic research papers efficiently. The application provides a complete API for user management, paper uploads, advanced search functionality, and citation tracking.

## ✨ Key Features

### 📚 Paper Management
- **Upload Research Papers**: Add papers with comprehensive metadata including title, authors, abstract, publication date, keywords, and journal/conference information
- **Advanced Search**: Full-text search across titles, abstracts, and keywords with relevance-based and date-based sorting
- **Citation Tracking**: Link papers through citations and track citation counts
- **View Analytics**: Track paper view counts with real-time analytics

### 👥 User Management
- **Secure Registration**: User signup with comprehensive validation and secure password hashing
- **Authentication**: Login system with session management
- **User Profiles**: Manage user information including department and contact details

### 🚀 Performance Optimization
- **Redis Caching**: Intelligent caching of search results for improved performance
- **Background Synchronization**: Automated sync of view counts from cache to database
- **Database Indexing**: Optimized MongoDB indexes for fast text search and queries

### 🛠️ Developer Features
- **Test Data Generation**: Built-in fake data generator for development and testing
- **Comprehensive Validation**: Input validation for all user and paper data
- **Error Handling**: Robust error handling with meaningful error messages

## 🏗️ Technology Stack

### Backend Framework
- **Flask 2.3.3**: Modern Python web framework
- **Python 3.x**: Core programming language

### Database & Storage
- **MongoDB**: Primary database for storing users, papers, and citations
- **Redis**: High-performance caching and session management

### Key Libraries
- **PyMongo 4.6.0**: MongoDB driver for Python
- **Redis 5.0.1**: Redis client for Python
- **bcrypt 4.1.2**: Secure password hashing
- **APScheduler 3.10.1**: Background task scheduling
- **Faker 22.0.0**: Test data generation

## 📋 Prerequisites

Before running the application, ensure you have the following installed:

- **Python 3.8+**
- **MongoDB** (local installation or cloud instance)
- **Redis** (local installation or cloud instance)
- **pip** (Python package manager)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/John-6670/ResearchPapersManager.git
cd ResearchPapersManager
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory (use `.env.example` as a template):

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=27017
DB_NAME=research_papers

# Redis Configuration
REDIS_CACHE=localhost
REDIS_PORT=6379
REDIS_DB=0

# Flask Configuration (optional)
FLASK_ENV=development
FLASK_DEBUG=True
```

### 4. Start Required Services

#### MongoDB
```bash
# For local MongoDB installation
mongod

# Or using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

#### Redis
```bash
# For local Redis installation
redis-server

# Or using Docker
docker run -d -p 6379:6379 --name redis redis:latest
```

### 5. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📖 API Documentation

### Authentication Endpoints

#### User Registration
```http
POST /signup
Content-Type: application/json

{
    "username": "john_doe",
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "department": "Computer Science"
}
```

**Response:**
```json
{
    "message": "User registered",
    "user_id": "64f1a2b3c4d5e6f7a8b9c0d1"
}
```

#### User Login
```http
POST /login
Content-Type: application/json

{
    "username": "john_doe",
    "password": "securepassword123"
}
```

**Response:**
```json
{
    "message": "Login successful",
    "user_id": "64f1a2b3c4d5e6f7a8b9c0d1"
}
```

### Paper Management Endpoints

#### Upload Paper
```http
POST /papers
Content-Type: application/json
X-User-ID: 64f1a2b3c4d5e6f7a8b9c0d1

{
    "title": "Machine Learning in Healthcare: A Comprehensive Survey",
    "authors": ["Dr. Jane Smith", "Prof. Michael Johnson"],
    "abstract": "This paper presents a comprehensive survey of machine learning applications in healthcare...",
    "publication_date": "2024-01-15",
    "journal_conference": "Journal of Medical AI",
    "keywords": ["machine learning", "healthcare", "AI", "medical"],
    "citations": ["64f1a2b3c4d5e6f7a8b9c0d2"]
}
```

**Response:**
```json
{
    "message": "Paper uploaded",
    "paper_id": "64f1a2b3c4d5e6f7a8b9c0d3"
}
```

#### Search Papers
```http
GET /papers?search=machine learning&sort_by=relevance&order=desc
```

**Response:**
```json
{
    "papers": [
        {
            "id": "64f1a2b3c4d5e6f7a8b9c0d3",
            "title": "Machine Learning in Healthcare: A Comprehensive Survey",
            "authors": ["Dr. Jane Smith", "Prof. Michael Johnson"],
            "publication_date": "2024-01-15",
            "journal_conference": "Journal of Medical AI",
            "keywords": ["machine learning", "healthcare", "AI", "medical"]
        }
    ]
}
```

#### Get Paper Details
```http
GET /papers/64f1a2b3c4d5e6f7a8b9c0d3
```

**Response:**
```json
{
    "_id": "64f1a2b3c4d5e6f7a8b9c0d3",
    "title": "Machine Learning in Healthcare: A Comprehensive Survey",
    "authors": ["Dr. Jane Smith", "Prof. Michael Johnson"],
    "abstract": "This paper presents a comprehensive survey...",
    "publication_date": "2024-01-15",
    "journal_conference": "Journal of Medical AI",
    "keywords": ["machine learning", "healthcare", "AI", "medical"],
    "views": 42,
    "citation_count": 3,
    "uploaded_by": "64f1a2b3c4d5e6f7a8b9c0d1"
}
```

## 🔧 Configuration

### Database Configuration
The application uses environment variables for database configuration:

- `DB_HOST`: MongoDB host (default: localhost)
- `DB_PORT`: MongoDB port (default: 27017)
- `DB_NAME`: Database name (default: research_papers)

### Redis Configuration
- `REDIS_CACHE`: Redis host (default: localhost)
- `REDIS_PORT`: Redis port (default: 6379)
- `REDIS_DB`: Redis database number (default: 0)

### Background Tasks
The application automatically starts background tasks for:
- Synchronizing view counts from Redis to MongoDB every 10 minutes
- Maintaining cache consistency

## 🧪 Development & Testing

### Generate Test Data
To populate the database with test data for development:

```bash
python data_generator.py
```

This will create:
- 100 test users
- 1000 test papers
- Random citations between papers

### Manual Background Sync
To manually sync view counts from Redis to MongoDB:

```bash
python sync_cache_db.py
```

### Data Validation
The application includes comprehensive validation for:

#### User Data
- Username: 3-20 characters, alphanumeric and underscores only
- Password: Minimum 8 characters
- Email: Valid email format
- All fields: Maximum length restrictions

#### Paper Data
- Title: Required, maximum 200 characters
- Abstract: Required, maximum 1000 characters
- Authors: 1-5 authors, each maximum 100 characters
- Keywords: 1-5 keywords, each maximum 50 characters
- Citations: Maximum 5 citations per paper

## 🏗️ Architecture

### Application Structure
```
ResearchPapersManager/
├── app.py                 # Main Flask application
├── database.py           # MongoDB operations
├── redis_client.py       # Redis operations
├── utils.py              # Validation utilities
├── sync_cache_db.py      # Background synchronization
├── data_generator.py     # Test data generation
├── requirements.txt      # Python dependencies
└── .env                  # Environment configuration
```

### Database Schema

#### Users Collection
```javascript
{
    "_id": ObjectId,
    "username": String (unique),
    "name": String,
    "email": String,
    "password": String (hashed),
    "department": String
}
```

#### Papers Collection
```javascript
{
    "_id": ObjectId,
    "title": String,
    "authors": [String],
    "abstract": String,
    "publication_date": String (ISO format),
    "journal_conference": String,
    "keywords": [String],
    "views": Number,
    "uploaded_by": ObjectId (User reference)
}
```

#### Citations Collection
```javascript
{
    "_id": ObjectId,
    "paper_id": ObjectId,
    "cited_paper_id": ObjectId
}
```

### Caching Strategy
- **Search Results**: Cached for 5 minutes with automatic invalidation
- **Paper Views**: Tracked in Redis and synced to MongoDB every 10 minutes
- **Username Availability**: Cached in Redis hash for fast lookup

## 🔍 Search Capabilities

### Text Search
- Full-text search across paper titles, abstracts, and keywords
- MongoDB text indexes for optimized search performance
- Relevance-based scoring

### Sorting Options
- **Relevance**: Based on text search score (default for search queries)
- **Publication Date**: Chronological ordering (ascending/descending)

### Caching
- Search results cached in Redis for improved performance
- Cache keys include search term, sort criteria, and order
- Automatic cache invalidation after 5 minutes

## 📈 Performance Features

### Optimizations
- **Database Indexes**: Text search and unique constraints
- **Redis Caching**: Search results and view counts
- **Background Processing**: Async view count synchronization
- **Connection Pooling**: Efficient database connections

### Monitoring
- View count tracking for analytics
- Citation count calculation
- Search result caching metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add proper error handling
- Include input validation
- Write meaningful commit messages
- Test thoroughly before submitting

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙋‍♂️ Support

For questions, issues, or contributions, please:
1. Check existing issues on GitHub
2. Create a new issue with detailed description
3. Follow the issue template guidelines

## 🔒 Security Considerations

### Password Security
- Passwords are hashed using bcrypt with automatic salt generation
- Minimum password length: 8 characters
- Passwords are never stored in plain text

### Session Management
- User sessions are managed through Redis for scalability
- Session tokens are validated on each authenticated request
- Username uniqueness is enforced at both application and database levels

### Input Validation
- All user inputs are validated before processing
- SQL injection protection through MongoDB's native drivers
- XSS protection through proper JSON response handling

### Environment Security
- Sensitive configuration stored in environment variables
- Database credentials should be secured in production
- Consider using environment-specific configuration files

## 🐛 Troubleshooting

### Common Issues

#### MongoDB Connection Issues
```bash
# Check if MongoDB is running
mongosh --eval "db.runCommand('ping')"

# For Docker installations
docker logs mongodb
```

#### Redis Connection Issues
```bash
# Check if Redis is running
redis-cli ping

# For Docker installations
docker logs redis
```

#### Port Already in Use
```bash
# Check which process is using port 5000
lsof -i :5000

# Kill the process if needed
kill -9 <PID>
```

#### Module Import Errors
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Check Python version (requires 3.8+)
python --version
```

#### Database Index Issues
If you encounter search performance issues:
```bash
# Connect to MongoDB and rebuild indexes
mongosh research_papers
db.papers.dropIndexes()
db.papers.createIndex({ "title": "text", "abstract": "text", "keywords": "text" })
```

## 🔮 Future Enhancements

Potential features for future development:
- **File Upload**: Support for PDF and document uploads
- **Advanced Analytics**: Detailed usage statistics and insights
- **Collaboration Features**: User collaboration and paper sharing
- **API Rate Limiting**: Request throttling and quota management
- **Full-Text PDF Search**: OCR and content extraction from uploaded files
- **Export Features**: Bibliography export in various formats (BibTeX, APA, etc.)
- **Notification System**: Email alerts for new citations and papers

---

**Built with ❤️ for the academic research community**