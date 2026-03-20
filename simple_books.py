import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


class SimpleBookManager:
    """Простая версия - книги хранятся в списке в памяти"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Менеджер книг - BASIC версия")
        self.root.geometry("700x500")

        # Список книг в памяти (при закрытии всё исчезнет)
        self.books = []
        self.next_id = 1

        self.create_widgets()
        self.update_list()

    def create_widgets(self):
        # Панель ввода
        input_frame = tk.LabelFrame(self.root, text="Добавить книгу", padx=10, pady=10)
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky='w')
        self.title_entry = tk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Автор:").grid(row=1, column=0, sticky='w')
        self.author_entry = tk.Entry(input_frame, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Год:").grid(row=2, column=0, sticky='w')
        self.year_entry = tk.Entry(input_frame, width=30)
        self.year_entry.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Рейтинг:").grid(row=3, column=0, sticky='w')
        self.rating_var = tk.StringVar(value="0")
        rating_frame = tk.Frame(input_frame)
        rating_frame.grid(row=3, column=1, sticky='w')
        for i in range(6):
            tk.Radiobutton(rating_frame, text=str(i), variable=self.rating_var, value=str(i)).pack(side=tk.LEFT)

        tk.Button(input_frame, text="➕ Добавить книгу", command=self.add_book,
                  bg='#4CAF50', fg='white').grid(row=4, column=0, columnspan=2, pady=10)

        # Таблица книг
        table_frame = tk.LabelFrame(self.root, text="Список книг", padx=10, pady=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(table_frame, columns=('ID', 'Название', 'Автор', 'Год', 'Рейтинг'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Название', text='Название')
        self.tree.heading('Автор', text='Автор')
        self.tree.heading('Год', text='Год')
        self.tree.heading('Рейтинг', text='Рейтинг')

        self.tree.column('ID', width=50)
        self.tree.column('Название', width=200)
        self.tree.column('Автор', width=150)
        self.tree.column('Год', width=80)
        self.tree.column('Рейтинг', width=80)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Кнопки управления
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(button_frame, text="🗑️ Удалить книгу", command=self.delete_book,
                  bg='#f44336', fg='white').pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="🔍 Поиск по автору", command=self.search_by_author,
                  bg='#2196F3', fg='white').pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="🔄 Показать все", command=self.show_all,
                  bg='#FF9800', fg='white').pack(side=tk.LEFT, padx=5)

        # Статус
        self.status = tk.Label(self.root, text="Готово", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        year = self.year_entry.get().strip()
        rating = self.rating_var.get()

        if not title or not author:
            messagebox.showwarning("Ошибка", "Введите название и автора!")
            return

        try:
            year = int(year) if year else 0
        except ValueError:
            year = 0

        book = {
            'id': self.next_id,
            'title': title,
            'author': author,
            'year': year,
            'rating': int(rating)
        }
        self.books.append(book)
        self.next_id += 1

        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_var.set("0")

        self.update_list()
        self.status.config(text=f"Добавлена книга: {title}")

    def delete_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите книгу для удаления")
            return

        item = self.tree.item(selected[0])
        book_id = int(item['values'][0])

        for i, book in enumerate(self.books):
            if book['id'] == book_id:
                del self.books[i]
                break

        self.update_list()
        self.status.config(text="Книга удалена")

    def search_by_author(self):
        author = simpledialog.askstring("Поиск", "Введите имя автора:")
        if author:
            filtered = [b for b in self.books if author.lower() in b['author'].lower()]
            self.update_list(filtered)
            self.status.config(text=f"Найдено книг: {len(filtered)}")

    def show_all(self):
        self.update_list()
        self.status.config(text=f"Всего книг: {len(self.books)}")

    def update_list(self, books=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if books is None:
            books = self.books

        for book in books:
            self.tree.insert('', 'end', values=(
                book['id'],
                book['title'],
                book['author'],
                book['year'],
                f"{book['rating']}/5"
            ))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SimpleBookManager()
    app.run()