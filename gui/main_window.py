import tkinter as tk
from tkinter import ttk, messagebox
from services.library_service import LibraryService
from gui.book_dialog import BookDialog


class MainWindow:
    def __init__(self):
        self.service = LibraryService()

        # Создание главного окна
        self.root = tk.Tk()
        self.root.title("Менеджер книг")
        self.root.geometry("800x600")

        # Установка стилей
        self.setup_styles()

        # Создание меню
        self.create_menu()

        # Создание панели инструментов
        self.create_toolbar()

        # Создание поля поиска
        self.create_search_bar()

        # Создание таблицы книг
        self.create_book_table()

        # Загрузка данных
        self.load_books()

    def setup_styles(self):
        """Настройка стилей для виджетов"""
        style = ttk.Style()
        style.theme_use('clam')

        # Настройка цветов
        style.configure('Treeview', rowheight=30, font=('Arial', 10))
        style.configure('Treeview.Heading', font=('Arial', 11, 'bold'))

    def create_menu(self):
        """Создание меню приложения"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Меню Файл
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Добавить книгу", command=self.show_add_dialog, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit, accelerator="Ctrl+Q")

        # Меню Правка
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Редактировать", command=self.show_edit_dialog, accelerator="Ctrl+E")
        edit_menu.add_command(label="Удалить", command=self.delete_selected_book, accelerator="Del")

        # Меню Вид
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Вид", menu=view_menu)
        view_menu.add_command(label="Обновить", command=self.load_books, accelerator="F5")

        # Меню Справка
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)

        # Горячие клавиши
        self.root.bind('<Control-n>', lambda e: self.show_add_dialog())
        self.root.bind('<Control-e>', lambda e: self.show_edit_dialog())
        self.root.bind('<Delete>', lambda e: self.delete_selected_book())
        self.root.bind('<F5>', lambda e: self.load_books())

    def create_toolbar(self):
        """Создание панели инструментов"""
        toolbar = tk.Frame(self.root, bg='#f0f0f0', height=50)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопки
        tk.Button(toolbar, text="Добавить книгу", command=self.show_add_dialog,
                  bg='#4CAF50', fg='white', padx=10).pack(side=tk.LEFT, padx=5, pady=10)

        tk.Button(toolbar, text="Редактировать", command=self.show_edit_dialog,
                  bg='#2196F3', fg='white', padx=10).pack(side=tk.LEFT, padx=5, pady=10)

        tk.Button(toolbar, text="Удалить", command=self.delete_selected_book,
                  bg='#f44336', fg='white', padx=10).pack(side=tk.LEFT, padx=5, pady=10)

        tk.Button(toolbar, text="Обновить", command=self.load_books,
                  bg='#FF9800', fg='white', padx=10).pack(side=tk.LEFT, padx=5, pady=10)

        # Фильтр по авторам
        tk.Label(toolbar, text="Автор:", bg='#f0f0f0').pack(side=tk.LEFT, padx=(20, 5))

        self.author_var = tk.StringVar()
        self.author_combo = ttk.Combobox(toolbar, textvariable=self.author_var, width=20)
        self.author_combo.pack(side=tk.LEFT, padx=5)
        self.author_combo.bind('<<ComboboxSelected>>', self.filter_by_author)

    def create_search_bar(self):
        """Создание строки поиска"""
        search_frame = tk.Frame(self.root, bg='white', height=40)
        search_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        tk.Label(search_frame, text="Поиск:", bg='white').pack(side=tk.LEFT, padx=5)

        self.search_entry = tk.Entry(search_frame, width=50, font=('Arial', 10))
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self.search_books)

        tk.Button(search_frame, text="Найти", command=self.search_books,
                  bg='#9C27B0', fg='white').pack(side=tk.LEFT, padx=5)

    def create_book_table(self):
        """Создание таблицы для отображения книг"""
        # Фрейм для таблицы и скроллбара
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Скроллбар
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Таблица
        self.tree = ttk.Treeview(table_frame,
                                 columns=('ID', 'Название', 'Автор', 'Год', 'Рейтинг', 'Жанр', 'Прочитано'),
                                 show='tree headings',
                                 yscrollcommand=scrollbar.set)

        scrollbar.config(command=self.tree.yview)

        # Настройка колонок
        self.tree.column('#0', width=0, stretch=False)
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Название', width=200)
        self.tree.column('Автор', width=150)
        self.tree.column('Год', width=80, anchor='center')
        self.tree.column('Рейтинг', width=80, anchor='center')
        self.tree.column('Жанр', width=120)
        self.tree.column('Прочитано', width=80, anchor='center')

        # Заголовки
        self.tree.heading('ID', text='ID')
        self.tree.heading('Название', text='Название')
        self.tree.heading('Автор', text='Автор')
        self.tree.heading('Год', text='Год')
        self.tree.heading('Рейтинг', text='Рейтинг')
        self.tree.heading('Жанр', text='Жанр')
        self.tree.heading('Прочитано', text='Прочитано')

        # Двойной клик для редактирования
        self.tree.bind('<Double-1>', lambda e: self.show_edit_dialog())

        self.tree.pack(fill=tk.BOTH, expand=True)

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
            read_status = "Да" if book.is_read else "Нет"
            self.tree.insert('', 'end', values=(
                book.id, book.title, book.author, book.year,
                f"{book.rating}/5", book.genre, read_status
            ))

        # Обновление списка авторов
        self.update_authors_list()

    def search_books(self, event=None):
        """Поиск книг"""
        query = self.search_entry.get()
        books = self.service.search_books(query)
        self.load_books(books)

    def filter_by_author(self, event=None):
        """Фильтр по автору"""
        author = self.author_var.get()
        books = self.service.get_books_by_author(author)
        self.load_books(books)

    def update_authors_list(self):
        """Обновление списка авторов в комбобоксе"""
        authors = self.service.get_all_authors()
        self.author_combo['values'] = authors

    def show_add_dialog(self):
        """Показать диалог добавления книги"""
        dialog = BookDialog(self.root, title="Добавление книги")
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
        dialog = BookDialog(self.root, title="Редактирование книги", book=book)
        self.root.wait_window(dialog)

        if dialog.result:
            try:
                book.title = dialog.result['title']
                book.author = dialog.result['author']
                book.year = int(dialog.result['year'])
                book.genre = dialog.result['genre']
                book.description = dialog.result['description']

                self.service.db.update_book(book)
                self.load_books()
                messagebox.showinfo("Успех", "Книга успешно обновлена!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось обновить книгу: {str(e)}")

    def delete_selected_book(self):
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

    def show_about(self):
        """Показать информацию о программе"""
        about_text = """
        Менеджер книг v1.0

        Приложение для управления личной библиотекой

        Функции:
        - Добавление/редактирование книг
        - Поиск по названию и автору
        - Фильтрация по авторам
        - Рейтинг книг
        - База данных SQLite

        Разработано в учебных целях
        """
        messagebox.showinfo("О программе", about_text)

    def run(self):
        """Запуск приложения"""
        self.root.mainloop()