import tkinter as tk
from tkinter import ttk, messagebox
from services.library_service import LibraryService
from gui.book_dialog import BookDialog


class MainWindow:
    """Главное окно приложения (intermediate версия)"""

    def __init__(self):
        self.service = LibraryService()

        self.root = tk.Tk()
        self.root.title("Менеджер книг - INTERMEDIATE версия")
        self.root.geometry("850x550")

        self.create_toolbar()
        self.create_search_bar()
        self.create_book_table()

        self.load_books()

    def create_toolbar(self):
        """Создание панели инструментов"""
        toolbar = tk.Frame(self.root, bg='#f0f0f0', height=45)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопки
        tk.Button(toolbar, text="➕ Добавить книгу", command=self.show_add_dialog,
                  bg='#4CAF50', fg='white', padx=10, font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=5, pady=8)

        tk.Button(toolbar, text="✏️ Редактировать", command=self.show_edit_dialog,
                  bg='#2196F3', fg='white', padx=10, font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=5, pady=8)

        tk.Button(toolbar, text="🗑️ Удалить", command=self.delete_book,
                  bg='#f44336', fg='white', padx=10, font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=5, pady=8)

        tk.Button(toolbar, text="🔄 Обновить", command=self.load_books,
                  bg='#FF9800', fg='white', padx=10, font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=5, pady=8)

        # Разделитель
        tk.Label(toolbar, text=" | ", bg='#f0f0f0', font=('Arial', 10)).pack(side=tk.LEFT, padx=5)

        # Фильтр по авторам
        tk.Label(toolbar, text="Фильтр по автору:", bg='#f0f0f0', font=('Arial', 9)).pack(side=tk.LEFT, padx=(10, 5))

        self.author_var = tk.StringVar()
        self.author_combo = ttk.Combobox(toolbar, textvariable=self.author_var, width=20, font=('Arial', 9))
        self.author_combo.pack(side=tk.LEFT, padx=5)
        self.author_combo.bind('<<ComboboxSelected>>', self.filter_by_author)

    def create_search_bar(self):
        """Создание строки поиска"""
        search_frame = tk.Frame(self.root, bg='white', height=40)
        search_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        tk.Label(search_frame, text="🔍 Поиск:", bg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)

        self.search_entry = tk.Entry(search_frame, width=50, font=('Arial', 10))
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self.search_books)

        tk.Button(search_frame, text="Найти", command=self.search_books,
                  bg='#9C27B0', fg='white', font=('Arial', 9)).pack(side=tk.LEFT, padx=5)

        tk.Button(search_frame, text="Сбросить", command=self.clear_search,
                  bg='#757575', fg='white', font=('Arial', 9)).pack(side=tk.LEFT, padx=5)

    def create_book_table(self):
        """Создание таблицы книг"""
        # Фрейм для таблицы
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Скроллбар
        scrollbar = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Таблица
        self.tree = ttk.Treeview(table_frame,
                                 columns=('ID', 'Название', 'Автор', 'Год', 'Рейтинг', 'Жанр'),
                                 show='headings',
                                 yscrollcommand=scrollbar.set)

        scrollbar.config(command=self.tree.yview)

        # Настройка колонок
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Название', width=250)
        self.tree.column('Автор', width=180)
        self.tree.column('Год', width=80, anchor='center')
        self.tree.column('Рейтинг', width=100, anchor='center')
        self.tree.column('Жанр', width=150)

        # Заголовки
        self.tree.heading('ID', text='ID')
        self.tree.heading('Название', text='Название')
        self.tree.heading('Автор', text='Автор')
        self.tree.heading('Год', text='Год')
        self.tree.heading('Рейтинг', text='Рейтинг')
        self.tree.heading('Жанр', text='Жанр')

        # Двойной клик для редактирования
        self.tree.bind('<Double-1>', lambda e: self.show_edit_dialog())

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Статусная строка
        self.status = tk.Label(self.root, text="Готово", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def load_books(self, books=None):
        """Загрузка книг в таблицу"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Получение книг
        if books is None:
            books = self.service.get_all_books()

        # Заполнение таблицы
        for book in books:
            self.tree.insert('', 'end', values=(
                book.id,
                book.title,
                book.author,
                book.year,
                f"⭐ {book.rating:.1f}/5",
                book.genre
            ))

        # Обновление статуса
        self.status.config(text=f"Всего книг: {len(books)}")

        # Обновление списка авторов
        self.update_authors_list()

    def search_books(self, event=None):
        """Поиск книг"""
        query = self.search_entry.get()
        books = self.service.search_books(query)
        self.load_books(books)
        self.status.config(text=f"Найдено книг: {len(books)}")

    def clear_search(self):
        """Очистка поиска"""
        self.search_entry.delete(0, tk.END)
        self.load_books()

    def filter_by_author(self, event=None):
        """Фильтр по автору"""
        author = self.author_var.get()
        books = self.service.get_books_by_author(author)
        self.load_books(books)
        self.status.config(text=f"Книг автора '{author}': {len(books)}")

    def update_authors_list(self):
        """Обновление списка авторов в комбобоксе"""
        authors = self.service.get_all_authors()
        self.author_combo['values'] = [''] + authors

    def show_add_dialog(self):
        """Показать диалог добавления книги"""
        dialog = BookDialog(self.root, "Добавление книги")
        self.root.wait_window(dialog)

        if dialog.result:
            try:
                self.service.add_book(
                    title=dialog.result['title'],
                    author=dialog.result['author'],
                    year=int(dialog.result['year']),
                    genre=dialog.result['genre'],
                    description=dialog.result['description']
                )
                self.load_books()
                messagebox.showinfo("Успех", "Книга успешно добавлена!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить книгу: {str(e)}")

    def show_edit_dialog(self):
        """Показать диалог редактирования книги"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите книгу для редактирования")
            return

        # Получение ID выбранной книги
        item = self.tree.item(selected[0])
        book_id = int(item['values'][0])

        # Получение книги из сервиса
        book = self.service.get_book_by_id(book_id)
        if not book:
            messagebox.showerror("Ошибка", "Книга не найдена")
            return

        # Открытие диалога редактирования
        dialog = BookDialog(self.root, "Редактирование книги", book)
        self.root.wait_window(dialog)

        if dialog.result:
            try:
                # Обновляем книгу
                book.title = dialog.result['title']
                book.author = dialog.result['author']
                book.year = int(dialog.result['year'])
                book.genre = dialog.result['genre']
                book.rating = float(dialog.result['rating'])
                book.description = dialog.result['description']
                book.is_read = dialog.result['read']

                self.service.update_book(book)
                self.load_books()
                messagebox.showinfo("Успех", "Книга успешно обновлена!")

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось обновить книгу: {str(e)}")

    def delete_book(self):
        """Удаление выбранной книги"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите книгу для удаления")
            return

        # Подтверждение удаления
        if not messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту книгу?"):
            return

        # Получение ID и удаление
        item = self.tree.item(selected[0])
        book_id = int(item['values'][0])

        if self.service.delete_book(book_id):
            self.load_books()
            messagebox.showinfo("Успех", "Книга успешно удалена!")
        else:
            messagebox.showerror("Ошибка", "Не удалось удалить книгу")

    def run(self):
        """Запуск приложения"""
        self.root.mainloop()