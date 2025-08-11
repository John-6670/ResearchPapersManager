# Research Papers Manager

## Overview
A Flask-based REST API for managing research papers, users, and citations with MongoDB for persistence and Redis for caching and counters. It provides user registration/login, paper upload with validation and citations, full-text search with relevance sorting, and view counting synchronized from Redis to MongoDB via a background scheduler.

## Key Features
- User management
  - Signup with validation (username, email, password) and bcrypt password hashing
  - Login with credential verification
  - Fast username availability checks cached in Redis (hash key: `usernames`)
- Paper management
  - Upload papers with validation (title, abstract, ISO date, 1–5 authors, 1–5 keywords, optional journal/conference)
  - Optional citations to other papers (stored as separate documents)
- Search and ranking
  - Full-text search over title, abstract, and keywords using MongoDB text index
  - Sorting by relevance or publication_date (asc/desc)
  - Search results cached in Redis (key: `search:{term}:{sort_by}:{order}`, TTL 300s)
- Views and analytics
  - Per-paper view counts incremented in Redis (key: `paper_views:{paper_id}`)
  - Background sync task (APScheduler) aggregates Redis views into MongoDB every 10 minutes
  - Citation count computed from `citations` collection
- Utilities and data
  - Input validators for users and papers
  - ObjectId serialization helper
  - Synthetic data generator using Faker for users, papers, and citations

## Tech Stack
- Python, Flask
- MongoDB (pymongo)
- Redis (redis-py)
- APScheduler for background jobs
- bcrypt for password hashing
- python-dotenv for configuration
- Faker for seeding test data

## Data Model (High Level)
- users: { _id, username, name, email, password (hashed), department }
- papers: { _id, uploaded_by (User._id), title, authors[], publication_date, abstract, journal_conference, keywords[], views }
- citations: { _id, paper_id (Paper._id), cited_paper_id (Paper._id) }

## API Endpoints
- POST /signup
  - Body: username, name, email, password, department
  - Creates user, checks Redis for username availability, stores bcrypt hash
- POST /login
  - Body: username, password
  - Verifies credentials, returns user_id
- POST /papers
  - Header: X-User-ID (existing user)
  - Body: title, abstract, publication_date (YYYY-MM-DD), authors[], keywords[], optional journal_conference, optional citations[]
  - Validates input, ensures cited papers exist, creates paper and citation docs
- GET /papers
  - Query: search, sort_by=relevance|publication_date, order=asc|desc
  - Returns cached or fresh search results
- GET /papers/{paper_id}
  - Increments Redis view counter, returns paper with aggregated views and citation_count

## Configuration (Environment)
- MongoDB: `DB_HOST`, `DB_PORT`, `DB_NAME`
- Redis: `REDIS_CACHE` (host), `REDIS_PORT`, `REDIS_DB`

## Background Processing
- A BackgroundScheduler job runs every 10 minutes:
  - Reads all `paper_views:*` keys, increments corresponding MongoDB paper views, then resets Redis counters to 0

## Seeding Data
- `data_generator.py` creates:
  - 100 users (unique usernames tracked in Redis)
  - 1000 papers across users
  - Up to 5 citations per paper

## Notes
- Dates should be ISO (YYYY-MM-DD).
- Text index is created on `title`, `abstract`, `keywords` for relevance scoring.
- Passwords are never stored