import logging
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

# Определение модели книги для базы данных
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)

# Создание таблиц базы данных
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    logging.info("Главная страница загружена.")
    return render_template('index.html')

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    logging.info("Получен список книг.")
    return jsonify([{"id": book.id, "title": book.title, "author": book.author} for book in books])

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    logging.info(f"Добавлена новая книга: {new_book.title} by {new_book.author}")
    return jsonify({
        "message": "Book added successfully!",
        "book": {"id": new_book.id, "title": new_book.title, "author": new_book.author}
    }), 201

@app.route('/books/log', methods=['POST'])
def log_book():
    data = request.get_json()
    logging.debug(f"Данные, отправленные на сервер: {data}")
    return jsonify({
        "message": "Data received",
        "data_received": data
    }), 200

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    db.session.commit()
    logging.info(f"Обновлена книга с ID {id}: {book.title} by {book.author}")
    return jsonify({"id": book.id, "title": book.title, "author": book.author})

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    logging.warning(f"Удалена книга с ID {id}: {book.title} by {book.author}")
    db.session.delete(book)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    logging.info("Запуск приложения Flask...")
    app.run(debug=True)
