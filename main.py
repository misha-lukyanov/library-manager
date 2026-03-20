#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер книг - приложение для управления личной библиотекой
Версия: 2.0
"""

import sys
import os
from gui.main_window import MainWindow


def setup_environment():
    """Настройка окружения"""
    # Создание необходимых папок
    os.makedirs("data", exist_ok=True)

    # Проверка наличия базы данных
    db_path = "data/library.db"
    if not os.path.exists(db_path):
        print(f"База данных будет создана: {db_path}")


def main():
    """Главная функция"""
    try:
        # Настройка окружения
        setup_environment()

        print("=" * 50)
        print("📚 Менеджер книг")
        print("=" * 50)
        print("Запуск приложения...")

        # Запуск приложения
        app = MainWindow()
        app.run()

    except Exception as e:
        print(f"❌ Ошибка при запуске приложения: {e}")
        import traceback
        traceback.print_exc()
        input("Нажмите Enter для выхода...")
        sys.exit(1)


if __name__ == "__main__":
    main()