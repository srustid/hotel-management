# Hotel Registration CRUD App (Flask)

A simple Flask + SQLAlchemy web application for registering, viewing, editing, and deleting hotel records, backed by a SQLite database.

## Features
- Create, Read, Update, Delete (CRUD) operations for hotel records
- SQLite database stored at `instance/example.db`
- Auto-creates the `hotels` table on startup if it doesn't already exist (safe even if `example.db` already exists)
- Flash messages for user feedback
- Single-page UI (`templates/index.html`)

## Requirements
- Python 3.8+
- Flask
- Flask-SQLAlchemy

## Installation

```bash
pip install flask flask-sqlalchemy
```

## Project Structure
