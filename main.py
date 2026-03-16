#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер книг - приложение для управления личной библиотекой
Версия: 1.0
"""

import sys
import os
from gui.main_window import MainWindow


def setup_environment():
    """Настройка окружения"""
    # Создание необходимых папок
    os.makedirs("data", exist_ok=True)


def main():
    """Главная функция"""
    try:
        # Настройка окружения
        setup_environment()

        # Запуск приложения
        app = MainWindow()
        app.run()

    except Exception as e:
        print(f"Ошибка при запуске приложения: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()