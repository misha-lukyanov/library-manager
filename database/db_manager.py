import sqlite3
import os
from models.book import Book


class DatabaseManager:
    """Менеджер базы данных SQLite"""

    def __init__(self, db_path="data/library.db"):
        # Создаем папку data, если её нет
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        """Получить соединение с БД"""
        return sqlite3.connect(self.db_path)

    def init_database(self):
        """Инициализация таблиц"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year INTEGER,
                    rating REAL DEFAULT 0,
                    genre TEXT,
                    description TEXT,
                    is_read INTEGER DEFAULT 0
                )
            ''')
            conn.commit()

    def add_book(self, book):
        """Добавить книгу"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO books (title, author, year, rating, genre, description, is_read)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (book.title, book.author, book.year, book.rating,
                  book.genre, book.description, book.is_read))
            conn.commit()
            return cursor.lastrowid

    def get_all_books(self):
        """Получить все книги"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM books')
            rows = cursor.fetchall()

            books = []
            for row in rows:
                book = Book(
                    title=row[1],
                    author=row[2],
                    year=row[3],
                    rating=row[4],
                    genre=row[5],
                    description=row[6],
                    book_id=row[0]
                )
                book.is_read = bool(row[7])
                books.append(book)
            return books

    def search_books(self, query):
        """Поиск книг по названию или автору"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM books 
                WHERE title LIKE ? OR author LIKE ?
            ''', (f'%{query}%', f'%{query}%'))

            rows = cursor.fetchall()
            books = []
            for row in rows:
                book = Book(
                    title=row[1],
                    author=row[2],
                    year=row[3],
                    rating=row[4],
                    genre=row[5],
                    description=row[6],
                    book_id=row[0]
                )
                book.is_read = bool(row[7])
                books.append(book)
            return books

    def update_book(self, book):
        """Обновить информацию о книге"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE books 
                SET title=?, author=?, year=?, rating=?, genre=?, description=?, is_read=?
                WHERE id=?
            ''', (book.title, book.author, book.year, book.rating,
                  book.genre, book.description, book.is_read, book.id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_book(self, book_id):
        """Удалить книгу"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM books WHERE id=?', (book_id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_books_by_author(self, author):
        """Получить книги по автору"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM books WHERE author=?', (author,))
            rows = cursor.fetchall()

            books = []
            for row in rows:
                book = Book(
                    title=row[1],
                    author=row[2],
                    year=row[3],
                    rating=row[4],
                    genre=row[5],
                    description=row[6],
                    book_id=row[0]
                )
                book.is_read = bool(row[7])
                books.append(book)
            return books