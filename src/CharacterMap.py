import folium
import pandas as pd

from DatabaseManager import DatabaseManager


class CharacterMap:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def generate_map(self, map_file_path):
        m = folium.Map(location=[0, 0], zoom_start=3)

        latest_characters = self.db_manager.get_characters_with_latest_locations()

        for char_id, character in latest_characters.items():
            location = self.db_manager.get_locations_by_character(character)
            if not location.empty:
                latitudes = location['Latitude']
                longitudes = location['Longitude']
                timestemps = location['Timestamp']
                df = pd.DataFrame({'lat': latitudes, 'long': longitudes, 'time': timestemps})
                print(character.name, df, sep='\n')
                df.dropna(how='any', inplace=True)
                if len(df) > 1:
                    sorted_df = df.sort_values(by='time')
                    folium.PolyLine(list(zip(sorted_df['lat'], sorted_df['long'])), color="blue", weight=2.5, opacity=1).add_to(m)
                    for lat, lon in zip(sorted_df['lat'], sorted_df['long']):
                        folium.Marker([lat, lon], popup=character.name).add_to(m)

        m.save(map_file_path)


# Пример использования:
if __name__ == '__main__':
    db_manager = DatabaseManager('../data/Ф/common_db.csv', '../data/characters.csv')
    character_map = CharacterMap(db_manager)
    character_map.generate_map('character_map.html')
