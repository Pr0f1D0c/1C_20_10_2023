import os
from DatabaseManager import DatabaseManager
from ConsoleInterface import ConsoleInterface


def main():
    db_file_path = os.path.join("../data", "common_db.csv")
    characters_file_path = os.path.join("../data", "characters.csv")

    # Создаем объект DatabaseManager
    db_manager = DatabaseManager(db_file_path, characters_file_path)

    # Создаем объект ConsoleInterface
    console = ConsoleInterface(db_manager)

    # Запускаем консольный интерфейс
    console.run()


if __name__ == '__main__':
    main()
