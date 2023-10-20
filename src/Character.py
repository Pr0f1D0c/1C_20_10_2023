from datetime import datetime
from typing import Any


class Character:
    def __init__(self, name: str | None = None, char_id: int | None = None,
                 last_seen_time: datetime | None = None, latitude: float | None = None,
                 longitude: float | None = None, location: str | None = None):
        self._name: str = name
        self._char_id: int = char_id
        self._last_seen_time: datetime | None = last_seen_time
        self._latitude: float | None = latitude
        self._longitude: float | None = longitude
        self._location: str | None = location

    # Геттеры и сеттеры для приватных полей
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def char_id(self) -> int:
        return self._char_id

    @char_id.setter
    def char_id(self, char_id: int):
        self._char_id = char_id

    # Геттеры и сеттеры для широты и долготы
    @property
    def latitude(self) -> float:
        return self._latitude

    @latitude.setter
    def latitude(self, latitude: float):
        self._latitude = latitude

    @property
    def longitude(self) -> float:
        return self._longitude

    @longitude.setter
    def longitude(self, longitude: float):
        self._longitude = longitude

    @property
    def location(self) -> str:
        return self._location

    @location.setter
    def location(self, location: str):
        self._location = location

    @property
    def last_seen_time(self) -> datetime:
        return self._last_seen_time

    @last_seen_time.setter
    def last_seen_time(self, last_seen_time: datetime):
        self._last_seen_time = last_seen_time

    # Метод для представления объекта в виде строки
    def __str__(self) -> str:
        return "Character {} (ID: {}) was last seen at {} on {} at latitude {} and longitude {}".format(
            self.name, self.char_id,
            self.location if self.location is not None else 'Unknown',
            self.last_seen_time if self.last_seen_time is not None else 'Unknown',
            self.latitude if self.latitude is not None else 'Unknown',
            self.longitude if self.longitude is not None else 'Unknown')


# Пример использования класса Character
if __name__ == '__main__':
    # Создание объекта Character
    gandalf = Character("Gandalf", 1)

    # Вывод информации о персонаже
    print(gandalf)
