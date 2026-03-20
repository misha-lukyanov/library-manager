class Book:
    """Модель книги для intermediate версии"""

    def __init__(self, title, author, year, rating=0, genre="", description=""):
        self.id = None
        self.title = title
        self.author = author
        self.year = year
        self.rating = float(rating)
        self.genre = genre
        self.description = description
        self.is_read = False

    def mark_as_read(self):
        """Отметить книгу как прочитанную"""
        self.is_read = True

    def update_rating(self, new_rating):
        """Обновить рейтинг"""
        try:
            rating = float(new_rating)
            if 0 <= rating <= 5:
                self.rating = rating
                return True
            return False
        except:
            return False

    def to_dict(self):
        """Конвертация в словарь для JSON"""
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
            data['title'],
            data['author'],
            data['year'],
            data.get('rating', 0),
            data.get('genre', ''),
            data.get('description', '')
        )
        book.id = data.get('id')
        book.is_read = data.get('is_read', False)
        return book