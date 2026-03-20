import json
import os


class StorageManager:
    """Сохранение и загрузка книг в JSON файл"""

    def __init__(self, filename="data/books.json"):
        self.filename = filename
        # Создаём папку data, если её нет
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    def save(self, books):
        """Сохранить книги в JSON"""
        data = [book.to_dict() for book in books]
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Сохранено {len(books)} книг в {self.filename}")

    def load(self):
        """Загрузить книги из JSON"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                from models.book import Book
                books = [Book.from_dict(item) for item in data]
                print(f"Загружено {len(books)} книг из {self.filename}")
                return books
        except FileNotFoundError:
            print(f"Файл {self.filename} не найден, создана пустая библиотека")
            return []
        except json.JSONDecodeError:
            print(f"Ошибка чтения файла {self.filename}")
            return []