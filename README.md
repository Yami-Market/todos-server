# Todos Server

This is todos demo API server with PostgreSQL database.

## Installation

**Note**: It **ONLY** test on Python 3.10+. If you get any error,
please use Python 3.10+. If you still get any error, please open an issue.

```bash
# Download the source code
git clone git@github.com:Yami-Market/todos-server.git

# Create a Python 3.10+ virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the dependencies
pip install -r requirements.txt

# Install Git Hooks
pre-commit install
```

## Environment Variables

Create a Flask `SECRET_KEY` by running the following command:

```bash
python -c 'import secrets; print(secrets.token_hex())'
```

Create a `.env` file in the root directory and add the following:

```bash
FLASK_SECRET_KEY=secret_key_you_just_created
DB_HOST="127.0.0.1"
DB_NAME=your_db_name
DB_USERNAME=your_db_username
DB_PASSWORD=your_db_password
```

## Run the Server

```bash
python src/app.py
```
