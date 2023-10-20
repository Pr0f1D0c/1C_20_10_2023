import os
import pandas as pd
from typing import Optional

from Character import Character


class DatabaseManager:
    def __init__(self, db_file_path: str, characters_file_path: str):
        self._db_file_path = db_file_path
        self._characters_file_path = characters_file_path
        self._locations_number = len(self.get_all_locations())

    @property
    def db_file_path(self) -> str:
        return self._db_file_path

    @property
    def locations_number(self) -> int:
        return self._locations_number

    @locations_number.setter
    def locations_number(self, locations_number: int):
        self._locations_number = locations_number

    @db_file_path.setter
    def db_file_path(self, file_path: str):
        self._db_file_path = file_path

    def save_location(self, character: Character):
        # Проверяем существование директории .data и создаем ее, если она отсутствует
        data_directory = os.path.dirname(self._db_file_path)
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)

        new_location = {
            'LabelNumber': self.locations_number,
            'CharacterID': character.char_id,
            'CharacterName': character.name,
            'Timestamp': character.last_seen_time,
            'Location': character.location,
            'Latitude': character.latitude,
            'Longitude': character.longitude
        }

        # Добавление записи в CSV
        location_df = pd.DataFrame([new_location])
        location_df.to_csv(self._db_file_path, mode='a', index=False, header=not os.path.exists(self._db_file_path))
        self.locations_number += 1

    def get_all_locations(self) -> pd.DataFrame:
        if os.path.exists(self._db_file_path):
            return pd.read_csv(self._db_file_path)
        else:
            return pd.DataFrame()

    def get_locations_by_character(self, character) -> pd.DataFrame:
        all_locations = self.get_all_locations()
        character_locations = all_locations[all_locations['CharacterID'] == character.char_id]
        return character_locations

    def add_character_to_file(self, character: Character):
        with open(self._characters_file_path, 'a') as characters_file:
            characters_file.write(f"{character.char_id} - {character.name}\n")

    def load_characters_from_file(self) -> dict[int, Character]:
        characters = {}
        if os.path.exists(self._characters_file_path):
            with open(self._characters_file_path, 'r') as characters_file:
                for line in characters_file:
                    parts = line.strip().split(' - ')
                    if len(parts) == 2:
                        char_id, char_name = parts
                        characters[int(char_id)] = Character(char_name, int(char_id))
        return characters

    # Метод для получения словаря персонажей с актуальными геометками
    def get_characters_with_latest_locations(self):
        # Загружаем все геометки
        all_locations_df = pd.read_csv(self._db_file_path)

        if all_locations_df.empty:
            return {}

        # Сгруппируйте по 'CharId' и найдите максимальное значение 'timestamp' для каждой группы
        max_timestamp_df = all_locations_df.groupby('CharacterID')['Timestamp'].max().reset_index()

        # Объедините исходный DataFrame с максимальными timestamp'ами, чтобы получить соответствующие координаты
        result_df = all_locations_df.merge(max_timestamp_df, on=['CharacterID', 'Timestamp'], how='inner')

        # Преобразуйте результат в словарь
        result_dict = {}
        for char_id, char_name, timestamp, location, latitude, longitude in result_df[
            ['CharacterID', 'CharacterName', 'Timestamp', 'Location', 'Latitude', 'Longitude']
        ].values:
            result_dict[char_id] = Character(char_name, char_id, last_seen_time=timestamp,
                                             location=location, latitude=latitude, longitude=longitude)

        return result_dict


# Пример использования класса DatabaseManager
if __name__ == '__main__':
    db_file_path = os.path.join(".", "data", "common_db.csv")

    # Создаем объект DatabaseManager
    db_manager = DatabaseManager(db_file_path)

    # Создаем объект Character
    gandalf = Character("Gandalf", 1, location='Moscow')

    # Сохраняем метку для персонажа
    db_manager.save_location(gandalf)

    # Загружаем все метки
    all_locations = db_manager.get_all_locations()
    print("Все метки:")
    print(all_locations)

    # Загружаем метки конкретного персонажа
    gandalf_locations = db_manager.get_locations_by_character(gandalf)
    print("\nМетки Гендальфа:")
    print(gandalf_locations)
