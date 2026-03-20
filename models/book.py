class Book:
    """Модель книги"""

    def __init__(self, title, author, year, rating=0.0, genre="",
                 description="", book_id=None):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.rating = float(rating)  # Всегда float
        self.genre = genre
        self.description = description
        self.is_read = False

    def mark_as_read(self):
        """Отметить книгу как прочитанную"""
        self.is_read = True

    def update_rating(self, new_rating):
        """Обновить рейтинг книги"""
        try:
            # Преобразуем в float и проверяем диапазон
            rating = float(new_rating)
            if 0 <= rating <= 5:
                self.rating = rating
                return True
            else:
                print(f"Рейтинг {rating} вне диапазона 0-5")
                return False
        except (ValueError, TypeError) as e:
            print(f"Ошибка преобразования рейтинга: {e}")
            return False

    def to_dict(self):
        """Конвертация в словарь для БД"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'rating': float(self.rating),  # Явно преобразуем в float
            'genre': self.genre,
            'description': self.description,
            'is_read': self.is_read
        }

    @classmethod
    def from_dict(cls, data):
        """Создание книги из словаря"""
        book = cls(
            title=data['title'],
            author=data['author'],
            year=data['year'],
            rating=float(data.get('rating', 0)),  # Всегда float
            genre=data.get('genre', ''),
            description=data.get('description', ''),
            book_id=data.get('id')
        )
        book.is_read = bool(data.get('is_read', False))
        return book

    def __str__(self):
        """Строковое представление книги"""
        read_status = "Прочитана" if self.is_read else "Не прочитана"
        return f"{self.title} - {self.author} ({self.year}) | Рейтинг: {self.rating}/5 | {read_status}"