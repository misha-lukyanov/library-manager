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
        self.root.geometry("900x600")

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

        # Настройка выделения
        style.map('Treeview',
                  background=[('selected', '#347083')],
                  foreground=[('selected', 'white')])

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
        edit_menu.add_separator()
        edit_menu.add_command(label="Отметить как прочитанное", command=self.mark_as_read, accelerator="Ctrl+R")

        # Меню Вид
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Вид", menu=view_menu)
        view_menu.add_command(label="Обновить", command=self.load_books, accelerator="F5")
        view_menu.add_separator()
        view_menu.add_command(label="Показать все книги", command=self.show_all_books)
        view_menu.add_command(label="Показать только прочитанные", command=self.show_read_books)
        view_menu.add_command(label="Показать только непрочитанные", command=self.show_unread_books)

        # Меню Справка
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)
        help_menu.add_command(label="Статистика", command=self.show_statistics)

        # Горячие клавиши
        self.root.bind('<Control-n>', lambda e: self.show_add_dialog())
        self.root.bind('<Control-e>', lambda e: self.show_edit_dialog())
        self.root.bind('<Delete>', lambda e: self.delete_selected_book())
        self.root.bind('<Control-r>', lambda e: self.mark_as_read())
        self.root.bind('<F5>', lambda e: self.load_books())

    def create_toolbar(self):
        """Создание панели инструментов"""
        toolbar = tk.Frame(self.root, bg='#f0f0f0', height=50)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопки
        tk.Button(toolbar, text="➕ Добавить книгу", command=self.show_add_dialog,
                  bg='#4CAF50', fg='white', padx=10, font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=5, pady=10)

        tk.Button(toolbar, text="✏️ Редактировать", command=self.show_edit_dialog,
                  bg='#2196F3', fg='white', padx=10, font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=5, pady=10)

        tk.Button(toolbar, text="🗑️ Удалить", command=self.delete_selected_book,
                  bg='#f44336', fg='white', padx=10, font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=5, pady=10)

        tk.Button(toolbar, text="✓ Прочитано", command=self.mark_as_read,
                  bg='#FF9800', fg='white', padx=10, font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=5, pady=10)

        tk.Button(toolbar, text="🔄 Обновить", command=self.load_books,
                  bg='#9C27B0', fg='white', padx=10, font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=5, pady=10)



        # Фильтр по авторам
        tk.Label(toolbar, text="Фильтр по автору:", bg='#f0f0f0', font=('Arial', 9)).pack(side=tk.LEFT, padx=(20, 5))

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
                  bg='#9C27B0', fg='white', font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=5)

        tk.Button(search_frame, text="Сбросить", command=self.clear_search,
                  bg='#757575', fg='white', font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=5)

    def create_book_table(self):
        """Создание таблицы для отображения книг"""
        # Фрейм для таблицы и скроллбара
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Скроллбары
        v_scrollbar = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        h_scrollbar = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Таблица
        self.tree = ttk.Treeview(table_frame,
                                 columns=('ID', 'Название', 'Автор', 'Год', 'Рейтинг', 'Жанр', 'Прочитано'),
                                 show='headings',
                                 yscrollcommand=v_scrollbar.set,
                                 xscrollcommand=h_scrollbar.set)

        v_scrollbar.config(command=self.tree.yview)
        h_scrollbar.config(command=self.tree.xview)

        # Настройка колонок
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Название', width=250, anchor='w')
        self.tree.column('Автор', width=200, anchor='w')
        self.tree.column('Год', width=80, anchor='center')
        self.tree.column('Рейтинг', width=100, anchor='center')
        self.tree.column('Жанр', width=150, anchor='w')
        self.tree.column('Прочитано', width=100, anchor='center')

        # Заголовки
        self.tree.heading('ID', text='ID')
        self.tree.heading('Название', text='Название')
        self.tree.heading('Автор', text='Автор')
        self.tree.heading('Год', text='Год издания')
        self.tree.heading('Рейтинг', text='Рейтинг')
        self.tree.heading('Жанр', text='Жанр')
        self.tree.heading('Прочитано', text='Прочитано')

        # Двойной клик для редактирования
        self.tree.bind('<Double-1>', lambda e: self.show_edit_dialog())

        # Правый клик для контекстного меню
        self.tree.bind('<Button-3>', self.show_context_menu)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Создание контекстного меню
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Редактировать", command=self.show_edit_dialog)
        self.context_menu.add_command(label="Удалить", command=self.delete_selected_book)
        self.context_menu.add_command(label="Отметить как прочитанное", command=self.mark_as_read)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Поставить рейтинг 5", command=self.set_rating_5)
        self.context_menu.add_command(label="Поставить рейтинг 0", command=self.set_rating_0)

    def show_context_menu(self, event):
        """Показать контекстное меню"""
        # Выделяем элемент под курсором
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

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
            read_status = "✅ Да" if book.is_read else "❌ Нет"
            # Форматируем рейтинг с одним знаком после запятой
            rating_display = f"⭐ {book.rating:.1f}/5"

            # Определяем цвет строки в зависимости от статуса
            tags = ('read',) if book.is_read else ('unread',)

            self.tree.insert('', 'end', values=(
                book.id,
                book.title,
                book.author,
                book.year,
                rating_display,
                book.genre,
                read_status
            ), tags=tags)

        # Настройка цветов для строк
        self.tree.tag_configure('read', background='#e8f5e8')  # Светло-зеленый для прочитанных
        self.tree.tag_configure('unread', background='#fff3e0')  # Светло-оранжевый для непрочитанных

        # Обновление списка авторов
        self.update_authors_list()

        # Обновление статусной строки
        self.update_status_bar()

    def update_status_bar(self):
        """Обновление статусной строки"""
        total = len(self.tree.get_children())
        read_count = len([item for item in self.tree.get_children()
                          if 'read' in self.tree.item(item, 'tags')])

        status_text = f"Всего книг: {total} | Прочитано: {read_count} | Не прочитано: {total - read_count}"

        # Проверяем, существует ли уже статусная строка
        if hasattr(self, 'status_bar'):
            self.status_bar.config(text=status_text)
        else:
            self.status_bar = tk.Label(self.root, text=status_text, bd=1, relief=tk.SUNKEN, anchor=tk.W)
            self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def search_books(self, event=None):
        """Поиск книг"""
        query = self.search_entry.get()
        books = self.service.search_books(query)
        self.load_books(books)

    def clear_search(self):
        """Очистка поиска"""
        self.search_entry.delete(0, tk.END)
        self.load_books()

    def filter_by_author(self, event=None):
        """Фильтр по автору"""
        author = self.author_var.get()
        books = self.service.get_books_by_author(author)
        self.load_books(books)

    def update_authors_list(self):
        """Обновление списка авторов в комбобоксе"""
        authors = self.service.get_all_authors()
        self.author_combo['values'] = [''] + authors  # Добавляем пустой элемент для сброса фильтра

    def show_all_books(self):
        """Показать все книги"""
        self.author_var.set('')
        self.search_entry.delete(0, tk.END)
        self.load_books()

    def show_read_books(self):
        """Показать только прочитанные книги"""
        all_books = self.service.get_all_books()
        read_books = [book for book in all_books if book.is_read]
        self.load_books(read_books)

    def show_unread_books(self):
        """Показать только непрочитанные книги"""
        all_books = self.service.get_all_books()
        unread_books = [book for book in all_books if not book.is_read]
        self.load_books(unread_books)

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

        print(f"Редактирование книги: {book.title}, текущий рейтинг: {book.rating}")

        # Открытие диалога редактирования
        dialog = BookDialog(self.root, title="Редактирование книги", book=book)
        self.root.wait_window(dialog)

        if dialog.result:
            try:
                print(f"Новый рейтинг из диалога: {dialog.result['rating']}")

                # Обновляем книгу через сервис
                book_data = {
                    'id': book.id,
                    'title': dialog.result['title'],
                    'author': dialog.result['author'],
                    'year': int(dialog.result['year']),
                    'genre': dialog.result['genre'],
                    'rating': float(dialog.result['rating']),
                    'read': dialog.result['read'],
                    'description': dialog.result['description']
                }

                if self.service.update_book(book_data):
                    self.load_books()
                    messagebox.showinfo("Успех", "Книга успешно обновлена!")
                else:
                    messagebox.showerror("Ошибка", "Не удалось обновить книгу")

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось обновить книгу: {str(e)}")
                print(f"Ошибка: {e}")

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

    def mark_as_read(self):
        """Отметить выбранную книгу как прочитанную"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите книгу")
            return

        item = self.tree.item(selected[0])
        book_id = int(item['values'][0])

        book = self.service.get_book_by_id(book_id)
        if book:
            book.mark_as_read()
            self.service.db.update_book(book)
            self.load_books()
            messagebox.showinfo("Успех", f"Книга '{book.title}' отмечена как прочитанная")

    def set_rating_5(self):
        """Установить рейтинг 5 для выбранной книги"""
        self.set_rating(5.0)

    def set_rating_0(self):
        """Установить рейтинг 0 для выбранной книги"""
        self.set_rating(0.0)

    def set_rating(self, rating):
        """Установить рейтинг для выбранной книги"""
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        book_id = int(item['values'][0])

        if self.service.update_book_rating(book_id, rating):
            self.load_books()
            messagebox.showinfo("Успех", f"Рейтинг установлен на {rating}")
        else:
            messagebox.showerror("Ошибка", "Не удалось установить рейтинг")

    def add_test_book_with_rating(self):
        """Добавить тестовую книгу с рейтингом 5"""
        try:
            book = self.service.add_book(
                title="Тестовая книга",
                author="Тестовый автор",
                year=2024,
                genre="Тест",
                description="Книга для проверки рейтинга"
            )
            # Устанавливаем рейтинг 5
            self.service.update_book_rating(book.id, 5.0)
            self.load_books()
            messagebox.showinfo("Успех", "Добавлена тестовая книга с рейтингом 5")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def show_statistics(self):
        """Показать статистику библиотеки"""
        books = self.service.get_all_books()

        total = len(books)
        read = len([b for b in books if b.is_read])
        unread = total - read

        if total > 0:
            avg_rating = sum(b.rating for b in books) / total
        else:
            avg_rating = 0

        # Статистика по авторам
        authors = {}
        for book in books:
            authors[book.author] = authors.get(book.author, 0) + 1

        top_author = max(authors.items(), key=lambda x: x[1]) if authors else ("Нет", 0)

        stats_text = f"""
        📊 СТАТИСТИКА БИБЛИОТЕКИ

        Всего книг: {total}
        📖 Прочитано: {read}
        📕 Не прочитано: {unread}

        ⭐ Средний рейтинг: {avg_rating:.2f}/5

        👤 Самый популярный автор: {top_author[0]} ({top_author[1]} книг)
        """

        messagebox.showinfo("Статистика", stats_text)

    def show_about(self):
        """Показать информацию о программе"""
        about_text = """
        📚 Менеджер книг v2.0

        Приложение для управления личной библиотекой

        Функции:
        ✓ Добавление/редактирование книг
        ✓ Поиск по названию и автору
        ✓ Фильтрация по авторам
        ✓ Рейтинг книг (0-5)
        ✓ Отметка о прочитанном
        ✓ Статистика библиотеки

        База данных: SQLite
        Интерфейс: Tkinter

        Разработано в учебных целях
        © 2024
        """
        messagebox.showinfo("О программе", about_text)

    def run(self):
        """Запуск приложения"""
        self.root.mainloop()