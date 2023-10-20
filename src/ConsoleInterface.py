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

    def display_all_locations(self):
        locations_df = self._db_manager.get_all_locations()
        if not locations_df.empty:
            print("Все геометки:")
            print(locations_df)
        else:
            print("Нет доступных геометок.")

    def display_character_locations(self, character_number):
        if character_number in self.characters:
            character = self.characters[character_number]
            locations_df = self._db_manager.get_locations_by_character(character)
            if not locations_df.empty:
                print(f"Геометки для персонажа {character.name} (ID: {character.char_id}):")
                print(locations_df)
            else:
                print(f"Нет доступных геометок для персонажа {character.name} (ID: {character.char_id}).")
        else:
            print(f"Персонаж с номером {character_number} не найден.")

    def display_character_list(self):
        if self.characters:
            print("Список персонажей:")
            for char_id, char_name in self.characters.items():
                print(f"{char_id}: {char_name}")
        else:
            print("Список персонажей пуст.")

    # Метод для вывода списка актуальных персонажей
    def display_latest_characters(self):
        self.characters = latest_characters = self._db_manager.get_characters_with_latest_locations()
        if latest_characters:
            print("Список актуальных меток персонажей:")
            for char_id, char_name in latest_characters.items():
                print(f"{char_id}: {char_name}")
        else:
            print("Нет актуальных персонажей с геометками.")

    def run(self):
        while True:
            print("\nВыберите действие:")
            print("1. Создать персонажа")
            print("2. Добавить метку персонажу")
            print("3. Вывести все геометки")
            print("4. Вывести геометки персонажа")
            print("5. Вывести список персонажей")
            print("6. Вывести актуальных персонажей")
            print("7. Выйти")

            choice = input("Введите номер действия: ")
            if choice == "1":
                new_character = self.create_character()
                print(f"Персонаж {new_character.name} (ID: {new_character.char_id}) создан.")
            elif choice == "2":
                self.add_location()
            elif choice == "3":
                self.display_all_locations()
            elif choice == "4":
                character_number = int(input("Введите номер персонажа: "))
                self.display_character_locations(character_number)
            elif choice == "5":
                self.display_character_list()
            elif choice == "6":
                self.display_latest_characters()
            elif choice == "7":
                break
            else:
                print("Неверный выбор. Пожалуйста, выберите действие снова.")
