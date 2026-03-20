from database.db_manager import DatabaseManager
from models.book import Book


class LibraryService:
    """Сервис для работы с библиотекой"""

    def __init__(self):
        self.db = DatabaseManager()
        self.current_books = []

    def add_book(self, title, author, year, genre="", description=""):
        """Добавить новую книгу"""
        book = Book(title, author, year, 0.0, genre, description)
        book.id = self.db.add_book(book)
        self.current_books.append(book)
        return book

    def get_all_books(self):
        """Получить все книги"""
        self.current_books = self.db.get_all_books()
        return self.current_books

    def search_books(self, query):
        """Поиск книг"""
        if not query.strip():
            return self.get_all_books()
        return self.db.search_books(query)

    def update_book_rating(self, book_id, rating):
        """Обновить рейтинг книги"""
        book = self.get_book_by_id(book_id)
        if book:
            if book.update_rating(rating):
                self.db.update_book(book)
                return True
        return False

    def get_book_by_id(self, book_id):
        """Получить книгу по ID"""
        # Сначала ищем в текущем списке
        for book in self.current_books:
            if book.id == book_id:
                return book
        # Если не нашли, загружаем все книги заново
        self.get_all_books()
        for book in self.current_books:
            if book.id == book_id:
                return book
        return None

    def delete_book(self, book_id):
        """Удалить книгу"""
        if self.db.delete_book(book_id):
            self.current_books = [b for b in self.current_books if b.id != book_id]
            return True
        return False

    def get_all_authors(self):
        """Получить список всех авторов"""
        books = self.get_all_books()
        authors = set(book.author for book in books if book.author)
        return sorted(list(authors))

    def get_books_by_author(self, author):
        """Получить книги конкретного автора"""
        if author and author.strip():
            return self.db.get_books_by_author(author)
        return self.get_all_books()

    def update_book(self, book_data):
        """Обновить книгу из словаря данных"""
        book = self.get_book_by_id(book_data['id'])
        if book:
            book.title = book_data['title']
            book.author = book_data['author']
            book.year = int(book_data['year'])
            book.genre = book_data['genre']
            book.rating = float(book_data['rating'])
            book.description = book_data['description']
            book.is_read = book_data['read']

            self.db.update_book(book)
            return True
        return False