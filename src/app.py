import os

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from flask import Flask, redirect, request, url_for
from flask_cors import CORS

load_dotenv()

FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY') or 'secret'
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

if DB_HOST is None:
    raise ValueError('DB_HOST is not set')
elif DB_NAME is None:
    raise ValueError('DB_NAME is not set')
elif DB_USERNAME is None:
    raise ValueError('DB_USERNAME is not set')
elif DB_PASSWORD is None:
    raise ValueError('DB_PASSWORD is not set')

app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY
CORS(app)


def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        cursor_factory=psycopg2.extras.RealDictCursor,
    )
    return conn


@app.route('/')
def index():
    return redirect(url_for('v1_index'))


@app.route('/v1')
def v1_index():
    return 'Todos API v1'


# TODO: Add HTTP Status Code
@app.route('/v1/debug')
def v1_debug():
    return 'Todos Market API v1 Debug', 100


@app.route('/v1/todos')
def todos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM todos')
    todos = cur.fetchall()
    cur.close()
    conn.close()
    return todos


@app.route('/v1/todos/<int:todo_id>')
def get_todo_by_id(todo_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM todos WHERE id = {todo_id}')
    todo = cur.fetchone()
    cur.close()
    conn.close()
    return todo or (f'Todo with id {todo_id} not found', 404)


@app.route('/v1/todos/<int:todo_id>', methods=['POST'])
def update_todo_by_id(todo_id: int):
    if request.is_json:
        body = request.get_json()
        title = body.get('title')  # type: ignore
        completed = body.get('completed')  # type: ignore

        if title is None:
            return {'message': 'title is required'}, 400

        if completed is None:
            return {'message': 'completed is required'}, 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            f"""UPDATE todos SET title = '{title}', completed = {completed}
                        WHERE id = {todo_id}
                    """)

        if cur.rowcount == 0:
            cur.close()
            conn.close()
            return (f'Todo with id {todo_id} not found', 404)

        conn.commit()
        cur.execute(f'SELECT * FROM todos WHERE id = {todo_id}')
        todo = cur.fetchone()
        cur.close()
        conn.close()
        return todo or (f'Todo with id {todo_id} not found', 404)
    else:
        return {'message': 'request body must be JSON'}, 400


if __name__ == '__main__':
    app.run(port=8000, debug=True)
