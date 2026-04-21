"""
Вспомогательные функции для проекта Airplane Tracker.
"""

from typing import List, Optional
from airpl_track.aeroplane import Aeroplane


def filter_aeroplanes_by_country(
    aeroplanes: List[Aeroplane], countries: List[str]
) -> List[Aeroplane]:
    """
    Фильтрует список самолётов по стране регистрации.

    Args:
        aeroplanes: Список объектов Aeroplane.
        countries: Список названий стран для фильтрации.

    Returns:
        Отфильтрованный список самолётов.
    """
    if not countries:
        return aeroplanes

    countries_lower = [c.lower().strip() for c in countries]
    result = []
    for a in aeroplanes:
        if a.origin_country.lower().strip() in countries_lower:
            result.append(a)
    return result


def filter_aeroplanes_by_altitude(
    aeroplanes: List[Aeroplane], min_alt: Optional[float], max_alt: Optional[float]
) -> List[Aeroplane]:
    """
    Фильтрует список самолётов по диапазону высот.

    Args:
        aeroplanes: Список объектов Aeroplane.
        min_alt: Минимальная высота (включительно).
        max_alt: Максимальная высота (включительно).

    Returns:
        Отфильтрованный список самолётов.
    """
    result = []
    for a in aeroplanes:
        if a.altitude is None:
            continue
        if min_alt is not None and a.altitude < min_alt:
            continue
        if max_alt is not None and a.altitude > max_alt:
            continue
        result.append(a)
    return result


def get_top_by_altitude(aeroplanes: List[Aeroplane], top_n: int) -> List[Aeroplane]:
    """
    Возвращает топ-N самолётов по высоте (по убыванию).

    Args:
        aeroplanes: Список объектов Aeroplane.
        top_n: Количество самолётов в топе.

    Returns:
        Список из top_n самолётов с наибольшей высотой.
    """
    valid = [a for a in aeroplanes if a.altitude is not None]
    sorted_aeroplanes = sorted(valid, key=lambda a: a.altitude if a.altitude is not None else 0.0, reverse=True)
    return sorted_aeroplanes[:top_n]
