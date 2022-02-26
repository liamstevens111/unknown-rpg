from .constants import base_stats


def max_hp_from_character_level(*, level: int) -> int:
    return base_stats['hp'] + int((level / base_stats['hp_gain'] + base_stats['hp_gain_rate']) * level)
