import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class BookDialog(tk.Toplevel):
    def __init__(self, parent, title="Книга", book=None):
        super().__init__(parent)

        self.parent = parent
        self.book = book
        self.result = None

        # Настройка окна
        self.title(title)
        self.geometry("400x500")
        self.resizable(False, False)

        # Делаем окно модальным
        self.transient(parent)
        self.grab_set()

        # Центрируем окно
        self.center_window()

        # Создаем интерфейс
        self.create_widgets()

        # Если редактируем книгу, заполняем поля
        if book:
            self.fill_fields()

    def center_window(self):
        """Центрирование окна относительно родителя"""
        self.update_idletasks()

        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (self.winfo_height() // 2)

        self.geometry(f'+{x}+{y}')

    def create_widgets(self):
        """Создание виджетов"""
        # Основной фрейм
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Название
        ttk.Label(main_frame, text="Название:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w',
                                                                                 pady=(0, 5))
        self.title_entry = ttk.Entry(main_frame, width=40, font=('Arial', 10))
        self.title_entry.grid(row=0, column=1, sticky='ew', pady=(0, 10))

        # Автор
        ttk.Label(main_frame, text="Автор:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='w', pady=(0, 5))
        self.author_entry = ttk.Entry(main_frame, width=40, font=('Arial', 10))
        self.author_entry.grid(row=1, column=1, sticky='ew', pady=(0, 10))

        # Год
        ttk.Label(main_frame, text="Год издания:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='w',
                                                                                    pady=(0, 5))
        self.year_entry = ttk.Entry(main_frame, width=40, font=('Arial', 10))
        self.year_entry.grid(row=2, column=1, sticky='ew', pady=(0, 10))

        # Жанр
        ttk.Label(main_frame, text="Жанр:", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky='w', pady=(0, 5))
        self.genre_entry = ttk.Entry(main_frame, width=40, font=('Arial', 10))
        self.genre_entry.grid(row=3, column=1, sticky='ew', pady=(0, 10))

        # Рейтинг
        ttk.Label(main_frame, text="Рейтинг (0-5):", font=('Arial', 10, 'bold')).grid(row=4, column=0, sticky='w',
                                                                                      pady=(0, 5))
        self.rating_var = tk.IntVar(value=0)
        rating_frame = ttk.Frame(main_frame)
        rating_frame.grid(row=4, column=1, sticky='w', pady=(0, 10))

        for i in range(6):
            rb = ttk.Radiobutton(rating_frame, text=str(i), variable=self.rating_var, value=i)
            rb.pack(side=tk.LEFT, padx=2)

        # Прочитано
        self.read_var = tk.BooleanVar()
        ttk.Checkbutton(main_frame, text="Книга прочитана", variable=self.read_var).grid(row=5, column=1, sticky='w',
                                                                                         pady=(0, 10))

        # Описание
        ttk.Label(main_frame, text="Описание:", font=('Arial', 10, 'bold')).grid(row=6, column=0, sticky='nw',
                                                                                 pady=(0, 5))

        # Текстовое поле с прокруткой
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=6, column=1, sticky='ew', pady=(0, 10))

        self.desc_text = tk.Text(text_frame, width=30, height=8, font=('Arial', 10))
        self.desc_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        desc_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.desc_text.yview)
        desc_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.desc_text.config(yscrollcommand=desc_scrollbar.set)

        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Сохранить", command=self.save, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена", command=self.cancel, width=15).pack(side=tk.LEFT, padx=5)

        # Настройка весов колонок
        main_frame.columnconfigure(1, weight=1)

    def fill_fields(self):
        """Заполнение полей данными книги"""
        self.title_entry.insert(0, self.book.title)
        self.author_entry.insert(0, self.book.author)
        self.year_entry.insert(0, str(self.book.year))
        self.genre_entry.insert(0, self.book.genre)
        self.rating_var.set(int(self.book.rating))
        self.read_var.set(self.book.is_read)
        self.desc_text.insert('1.0', self.book.description)

    def validate(self):
        """Валидация полей"""
        if not self.title_entry.get().strip():
            messagebox.showerror("Ошибка", "Введите название книги")
            return False

        if not self.author_entry.get().strip():
            messagebox.showerror("Ошибка", "Введите автора книги")
            return False

        year = self.year_entry.get().strip()
        if year:
            try:
                year_int = int(year)
                current_year = datetime.now().year
                if year_int < 0 or year_int > current_year + 10:
                    messagebox.showerror("Ошибка", "Некорректный год")
                    return False
            except ValueError:
                messagebox.showerror("Ошибка", "Год должен быть числом")
                return False

        return True

    def save(self):
        """Сохранение данных"""
        if not self.validate():
            return

        self.result = {
            'title': self.title_entry.get().strip(),
            'author': self.author_entry.get().strip(),
            'year': self.year_entry.get().strip() or '0',
            'genre': self.genre_entry.get().strip(),
            'rating': self.rating_var.get(),
            'read': self.read_var.get(),
            'description': self.desc_text.get('1.0', 'end-1c').strip()
        }

        self.destroy()

    def cancel(self):
        """Отмена"""
        self.destroy()