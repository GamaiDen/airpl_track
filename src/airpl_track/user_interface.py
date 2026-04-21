"""
Пользовательский интерфейс для взаимодействия с программой.
"""

from typing import List, Optional
from tqdm import tqdm

from airpl_track.api import OpenSkyAPI
from airpl_track.aeroplane import Aeroplane
from airpl_track.file_handler import JSONFileHandler
from airpl_track.utils import (
    filter_aeroplanes_by_country,
    filter_aeroplanes_by_altitude,
    get_top_by_altitude,
)


def parse_altitude_range(range_str: str) -> tuple[Optional[float], Optional[float]]:
    """
    Парсит строку диапазона высот вида 'min - max' или 'min-max'.
    """
    range_str = range_str.replace(" ", "")
    if "-" not in range_str:
        raise ValueError("Диапазон должен быть в формате 'min-max'")

    parts = range_str.split("-")
    min_alt = float(parts[0]) if parts[0] else None
    max_alt = float(parts[1]) if parts[1] else None
    return min_alt, max_alt


def print_aeroplanes(aeroplanes: List[Aeroplane]) -> None:
    """Красивый вывод списка самолётов."""
    if not aeroplanes:
        print("❌ Самолёты не найдены.")
        return

    print(f"\n✈️ Найдено самолётов: {len(aeroplanes)}\n")
    print("-" * 80)
    print(f"{'Позывной':<15} {'Страна':<20} {'Высота (м)':<12} {'Скорость (м/с)':<15}")
    print("-" * 80)
    for a in aeroplanes:
        altitude = f"{a.altitude:.1f}" if a.altitude else "N/A"
        velocity = f"{a.velocity:.1f}" if a.velocity else "N/A"
        print(f"{a.callsign:<15} {a.origin_country:<20} {altitude:<12} {velocity:<15}")


def user_interaction() -> None:
    """Главная функция взаимодействия с пользователем."""
    print("=" * 50)
    print("🛫 ТРЕКЕР САМОЛЁТОВ 🛬")
    print("=" * 50)

    country = input("\n🌍 Введите название страны для поиска самолётов: ").strip()
    if not country:
        print("❌ Страна не указана. Выход.")
        return

    print(f"\n🔍 Ищу самолёты над {country}...")
    api = OpenSkyAPI()
    try:
        raw_data = api.get_data(country)
    except Exception as e:
        print(f"❌ Ошибка при запросе к API: {e}")
        return

    if not raw_data:
        print(f"❌ Над {country} сейчас нет самолётов.")
        return

    # mypy: ignore
    aeroplanes = Aeroplane.cast_to_object_list(raw_data)  # type: ignore
    print(f"✅ Найдено {len(aeroplanes)} самолётов.")

    saver = JSONFileHandler("aeroplanes.json")
    print("💾 Сохраняю данные...")
    for a in tqdm(aeroplanes, desc="Сохранение", unit=" сам."):
        saver.add(a)
    print("✅ Данные сохранены в aeroplanes.json")

    prompt = "\n🛂 Введите страны регистрации для фильтра (через пробел, или Enter): "
    filter_countries_str = input(prompt).strip()
    filter_countries = filter_countries_str.split() if filter_countries_str else []
    filtered = filter_aeroplanes_by_country(aeroplanes, filter_countries)

    altitude_str = input("\n📏 Введите диапазон высот (например '5000-10000') или Enter чтобы пропустить: ").strip()
    if altitude_str:
        try:
            min_alt, max_alt = parse_altitude_range(altitude_str)
            filtered = filter_aeroplanes_by_altitude(filtered, min_alt, max_alt)
        except ValueError as e:
            print(f"⚠️ Ошибка парсинга диапазона: {e}")

    top_n_str = input("\n🏆 Введите N для топа самолётов по высоте (или Enter чтобы пропустить): ").strip()
    if top_n_str:
        try:
            top_n = int(top_n_str)
            filtered = get_top_by_altitude(filtered, top_n)
        except ValueError:
            print("⚠️ Некорректное число, топ не применяется.")

    print_aeroplanes(filtered)


if __name__ == "__main__":
    user_interaction()
