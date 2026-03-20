from models.book import Book
from storage.storage_manager import StorageManager


class LibraryService:
    """Сервис для работы с библиотекой (JSON версия)"""

    def __init__(self):
        self.storage = StorageManager()
        self.books = self.storage.load()
        # Определяем следующий ID
        self.next_id = max([book.id for book in self.books if book.id is not None], default=0) + 1

    def add_book(self, title, author, year, genre="", description=""):
        """Добавить новую книгу"""
        book = Book(title, author, year, 0, genre, description)
        book.id = self.next_id
        self.next_id += 1
        self.books.append(book)
        self.storage.save(self.books)
        return book

    def get_all_books(self):
        """Получить все книги"""
        return self.books

    def search_books(self, query):
        """Поиск книг по названию или автору"""
        if not query or not query.strip():
            return self.books
        query = query.lower().strip()
        return [b for b in self.books if query in b.title.lower() or query in b.author.lower()]

    def get_books_by_author(self, author):
        """Получить книги конкретного автора"""
        if not author or not author.strip():
            return self.books
        return [b for b in self.books if b.author == author]

    def get_all_authors(self):
        """Получить список всех авторов"""
        authors = set(book.author for book in self.books if book.author)
        return sorted(list(authors))

    def get_book_by_id(self, book_id):
        """Получить книгу по ID"""
        for book in self.books:
            if book.id == book_id:
                return book
        return None

    def update_book(self, book):
        """Обновить книгу"""
        for i, b in enumerate(self.books):
            if b.id == book.id:
                self.books[i] = book
                self.storage.save(self.books)
                return True
        return False

    def delete_book(self, book_id):
        """Удалить книгу"""
        for i, book in enumerate(self.books):
            if book.id == book_id:
                del self.books[i]
                self.storage.save(self.books)
                return True
        return False

    def update_book_rating(self, book_id, rating):
        """Обновить рейтинг книги"""
        book = self.get_book_by_id(book_id)
        if book:
            if book.update_rating(rating):
                self.storage.save(self.books)
                return True
        return False