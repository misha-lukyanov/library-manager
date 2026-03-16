class Book:
    """Модель книги"""

    def __init__(self, title, author, year, rating=0, genre="",
                 description="", book_id=None):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.rating = rating  # от 0 до 5
        self.genre = genre
        self.description = description
        self.is_read = False

    def mark_as_read(self):
        """Отметить книгу как прочитанную"""
        self.is_read = True

    def update_rating(self, new_rating):
        """Обновить рейтинг книги"""
        if 0 <= new_rating <= 5:
            self.rating = new_rating

    def to_dict(self):
        """Конвертация в словарь для БД"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'rating': self.rating,
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
            rating=data['rating'],
            genre=data.get('genre', ''),
            description=data.get('description', ''),
            book_id=data.get('id')
        )
        book.is_read = data.get('is_read', False)
        return book