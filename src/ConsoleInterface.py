from datetime import datetime

from Character import Character
from DatabaseManager import DatabaseManager


class ConsoleInterface:
    def __init__(self, db_manager: DatabaseManager):
        self._db_manager = db_manager
        self.characters: dict[int, Character] = db_manager.load_characters_from_file()
        self._character_counter: int = len(self.characters) + 1

        # Метод для создания персонажа

    def create_character(self):
        print("Создание нового персонажа:")
        name = input("Имя персонажа: ").strip() or None
        location = input("Локация: ").strip() or None
        latitude = input("Широта: ").strip()
        if latitude:
            latitude = float(latitude)
        else:
            latitude = None
        longitude = input("Долгота: ").strip()
        if longitude:
            longitude = float(longitude)
        else:
            longitude = None
        time = input("Время (YYYY-MM-DD HH:MM:SS): ").strip() or None
        if time:
            time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

        char_id = self._character_counter
        self._character_counter += 1

        new_character = Character(name, char_id, location=location, last_seen_time=time,
                                  latitude=latitude, longitude=longitude)

        # Сохраняем нового персонажа в базу данных и словарь персонажей
        self._db_manager.add_character_to_file(new_character)
        self._db_manager.save_location(new_character)
        self.characters[char_id] = new_character

        return new_character

    # Метод для добавления метки персонажу
    def add_location(self):
        print("Выберите персонажа для добавления метки:")
        for char_id, char_name in self.characters.items():
            print(f"{char_id}: {char_name}")
        try:
            char_id_to_update = int(input("Введите номер персонажа для обновления его локации: "))
        except:
            print('Некорректный формат ввода!')
            return

        if char_id_to_update in self.characters:
            selected_character = self.characters[char_id_to_update]  # Персонаж, для которого обновляем локацию
            print(f"Добавление метки для персонажа {selected_character.name} (ID: {selected_character.char_id}):")
            location = input("Локация: ").strip() or None
            latitude = input("Широта: ").strip()
            if latitude:
                latitude = float(latitude)
            else:
                latitude = None
            longitude = input("Долгота: ").strip()
            if longitude:
                longitude = float(longitude)
            else:
                longitude = None
            time = input("Время (YYYY-MM-DD HH:MM:SS): ").strip() or None
            if time:
                time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

            selected_character.location = location
            selected_character.latitude = latitude
            selected_character.longitude = longitude
            selected_character.last_seen_time = time

            # Сохраняем метку в базу данных
            self._db_manager.save_location(selected_character)
        else:
            print(f"Персонаж с номером {char_id_to_update} не найден.")

    def run(self):
        while True:
            print("\nВыберите действие:")
            print("1. Создать персонажа")
            print("2. Добавить метку персонажу")
            print("3. Выйти")

            choice = input("Введите номер действия: ")
            if choice == "1":
                new_character = self.create_character()
                print(f"Персонаж {new_character.name} (ID: {new_character.char_id}) создан.")
            elif choice == "2":
                self.add_location()
            elif choice == "3":
                break
            else:
                print("Неверный выбор. Пожалуйста, выберите действие снова.")
