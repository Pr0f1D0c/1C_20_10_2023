import folium
from DatabaseManager import DatabaseManager


class CharacterMap:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def generate_map(self, map_file_path):
        # Создаем карту с начальными координатами
        m = folium.Map(location=[0, 0], zoom_start=1)

        # Получаем актуальных персонажей с их геометками
        latest_characters = self.db_manager.get_characters_with_latest_locations()

        # Перебираем актуальных персонажей и добавляем метки на карту
        for char_id, character in latest_characters.items():
            if character.latitude and character.longitude:
                lat, lon = float(character.latitude), float(character.longitude)
                folium.Marker([lat, lon], popup=character.name).add_to(m)

        # Сохраняем карту в HTML-файл
        m.save(map_file_path)


# Пример использования:
if __name__ == '__main__':
    db_manager = DatabaseManager('../data/common_db.csv', '../data/characters.csv')
    character_map = CharacterMap(db_manager)
    character_map.generate_map('character_map.html')
