def calc_magic_damage(level, magic_coef, growth_coef, point):
    return level * (magic_coef + 1662) * (1 + growth_coef) / 7500 + point['health'] * 0.3 + point['defend'] * 0.2 + \
        point['attack'] * 0.4 + point['magic'] * 0.7


def calc_magic_damage2(level, magic_coef, growth_coef, point):
    return level * magic_coef * (growth_coef * 3e-4 + 8.56e-5) + point['magic'] * growth_coef * 0.7 + point[
        'defend'] * 0.2 + point[
        'attack'] * 0.4 + point['health'] * 0.3


def calc_magic_damage_from_point(point, growth_coef):
    return point * growth_coef * 0.7 + point * 0.2 + point * 0.4 + point * 0.3

print(calc_magic_damage2(163, 5834, 1.215, {
    'health': 235 + 61,
    'magic': 183 + 29,
    'attack': 183 + 55,
    'defend': 183 + 80,
}), 845) # 实际 845

print(calc_magic_damage2(81, 13789, 1.853, {
    'health': 131,
    'defend': 131,
    'attack': 131,
    'magic': 131,
}), 949) # 实际949

print(calc_magic_damage2(79, 4535, 13.572, {
    'health': 129,
    'defend': 129,
    'attack': 129,
    'magic': 129,
}), 2840) # 实际2840

print(calc_magic_damage2(81, 9235, 11.363, {
    'health': 131,
    'defend': 131,
    'attack': 131,
    'magic': 131,
}), 3750) # 实际3750

print(calc_magic_damage2(163, 14257, 11.409, {
    'health': 213,
    'defend': 213,
    'attack': 213,
    'magic': 891,
}) + 891 * 0.4, 15699) # 实际 15699
