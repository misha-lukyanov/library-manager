#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер книг - INTERMEDIATE версия
Приложение для управления личной библиотекой с сохранением в JSON
"""

import sys
import os
from gui.main_window import MainWindow


def setup_environment():
    """Настройка окружения"""
    # Создаём папку data, если её нет
    os.makedirs("data", exist_ok=True)


def main():
    """Главная функция"""
    try:
        setup_environment()

        print("=" * 50)
        print("📚 Менеджер книг - INTERMEDIATE версия")
        print("Хранение данных: JSON файл")
        print("=" * 50)
        print()

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