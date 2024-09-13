# helpers.py

import os
import platform
import io
import sys
import re

def set_encoding():
    """Устанавливает кодировку для стандартного ввода и вывода."""
    if sys.version_info >= (3, 6):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

def clear_screen():
    """Очистка экрана консоли."""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def format_url(url):
    # Удаление пробелов с начала и конца строки
    url = url.strip()

    # Проверка и добавление протокола, если его нет
    if not re.match(r'^https?://', url):
        url = f"https://{url}"
    
    # Убедимся, что URL заканчивается на '/'
    if not url.endswith('/'):
        url += '/'
    
    return url