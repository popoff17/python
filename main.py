import sys
import time
import requests

from helpers import set_encoding, clear_screen, format_url

""" Сайт, с которым будем работать """
work_site = ""

# Функции для пунктов меню
def info():
    print("===================================")
    print("\n")
    if(work_site != ""):
        print("Страница для анализа: " + work_site)
    print("\n")
    print("===================================")
    print("\n")
    print("\n")


def analyze_css():
    global work_site
    if(work_site == ""):
        print("Страница для анализа не установлена")
    else:
        print("Анализ CSS начат...")
        progress_bar(5)
        print("Анализ CSS завершён.")

def analyze_js():
    print("Анализ JS начат...")
    time.sleep(2)
    print("Анализ JS завершён.")

def process_site():
    print("Обрабатываем сайт полностью...")
    time.sleep(3)
    print("Обработка завершена.")

def view_logs():
    print("Просмотр логов...")
    time.sleep(2)
    print("Логи показаны.")

def set_page():
    global work_site
    try:
        while True:
            url = input("Введите url сайта: ")
            if url:
                break
        formatted_url = format_url(url)
        response = requests.get(formatted_url)
        if response.status_code == 200:
            print("Введенный адрес возвращает код 200")
            work_site = formatted_url
        else:
            print("Введенный адрес НЕ возвращает код 200")
    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем.")
        sys.exit(0)


# Классы для динамического меню
class MenuItem:
    def __init__(self, name, action=None, sub_menu=None):
        self.name = name
        self.action = action  # Функция, которую нужно вызвать, если это не подменю
        self.sub_menu = sub_menu  # Список дочерних MenuItem

    def is_leaf(self):
        """Проверяем, есть ли подменю"""
        return self.sub_menu is None

    def run(self):
        """Запуск действия или отображение подменю"""
        if self.is_leaf():
            if self.action:
                self.action()  # Выполнить действие
        else:
            self.show_sub_menu()  # Показать подменю

    def show_sub_menu(self, is_root=False):
        """Отображение подменю"""
        clear_screen()  # Очищаем экран перед отображением подменю
        info()  # Всегда выводим info() перед меню
        for i, item in enumerate(self.sub_menu):
            print(f"{i + 1}. {item.name}")
        if is_root:
            print(f"0. Выход")
        else:
            print(f"0. Назад")

class Menu:
    def __init__(self, root_menu, is_root=True):
        self.root_menu = root_menu
        self.current_menu = root_menu
        self.is_root = is_root  # Определяем, является ли это корневое меню

    def navigate(self):
        """Рекурсивная навигация по меню"""
        while True:
            clear_screen()
            info()  # Вызов функции info() перед отображением меню
            self.current_menu.show_sub_menu(is_root=self.is_root)
            choice = input("Введите номер пункта: ")

            if choice.isdigit():
                choice = int(choice)

                if choice == 0:
                    if self.is_root:
                        print("Выход из программы.")
                        sys.exit(0)  # Завершаем программу, если это корневое меню
                    else:
                        return  # Возврат на уровень выше
                elif 0 < choice <= len(self.current_menu.sub_menu):
                    selected_item = self.current_menu.sub_menu[choice - 1]
                    if selected_item.is_leaf():
                        selected_item.run()  # Выполнить действие, если это лист
                    else:
                        submenu = Menu(selected_item, is_root=False)
                        submenu.navigate()  # Рекурсивно зайти в подменю
                else:
                    print("Неверный выбор. Пожалуйста, попробуйте снова.")
            else:
                print("Пожалуйста, введите число.")


# Функция для имитации прогресс-бара
def progress_bar(seconds):
    """Функция для имитации прогресс-бара"""
    for i in range(seconds):
        time.sleep(1)
        progress = int((i + 1) / seconds * 100)
        sys.stdout.write(f"\rПрогресс: {progress}%")
        sys.stdout.flush()  # Обновляем вывод
    print("\nПрогресс: 100% Завершено.")

# Определение дерева меню
main_menu = MenuItem("Главное меню", sub_menu=[
    MenuItem("Анализ сайта", sub_menu=[
        MenuItem("Оптимизировать страницу", sub_menu=[
            MenuItem("Установить страницу", set_page),
            MenuItem("Анализ CSS", action=analyze_css),
            MenuItem("Анализ JS", action=analyze_js)
        ]),
        MenuItem("Обработать сайт полностью", action=process_site)
    ]),
    MenuItem("Просмотр логов", action=view_logs)
])

def main():
    """Основная функция для работы меню"""
    set_encoding()  # Устанавливаем кодировку
    try:
        menu = Menu(main_menu)  # Инициализация меню
        menu.navigate()  # Навигация по меню
    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем.")
        sys.exit(0)

if __name__ == "__main__":
    main()
