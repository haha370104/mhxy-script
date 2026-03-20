from helper.equipment import strength, strength_pre_check
from time import sleep
from helper.xichong import run_xichong
from helper.image import find_img_position
from helper.auto_fight import auto_fight

def main():
    # strength(equip_count=1, stone_per_equip=713)
    # run_xichong(3000)
    auto_fight()

main()
