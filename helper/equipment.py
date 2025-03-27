from helper.image import find_img_position, template_matching, get_image
from helper.mouse import find_img_click
from ascript.windows.action import mouse_move, click, key_down, key_up, input
from time import sleep
from ascript.windows.screen import capture


def move_inventory_position(base_coordinate, item_order):
    grid_size = 50
    base_x, base_y = base_coordinate
    item_x = item_order % 5
    item_y = int(item_order / 5)
    mouse_move(base_x + item_x * grid_size, base_y + item_y * grid_size, duration=0.3)


def move_equipment_position(equipment_order):
    [basic_x, basic_y] = find_img_position('picture\\inventory_title.png')
    x_offset, y_offset = -105, 202
    move_inventory_position([basic_x + x_offset, basic_y + y_offset], equipment_order)


def split_stone(stone_position, times):
    for i in range(times):
        move_equipment_position(stone_position)
        key_down('alt')
        sleep(0.3)
        click(button='left')
        sleep(0.3)
        key_up('alt')
        input('1')
        find_img_click('picture\\confirm.png')
        print(f'完成第{i}次拆分')


def strength_pre_check(x, y):
    x_offset, y_offset = -193, 98
    basic_x, basic_y = x + x_offset, y + y_offset

    first_plot = capture(rect=[basic_x, basic_y, basic_x + 50, basic_y + 50])
    stone = get_image('picture\\strengthen_stone.png')
    match_result = template_matching(first_plot, stone)[0].size > 0
    return match_result


def strengthen_equip(equip_position, stone_position, basic_coordinate):
    basic_x, basic_y = basic_coordinate

    x_offset, y_offset = -8, 108
    confirm_x_offset, confirm_y_offset = -158, 291

    base_coordinate = [basic_x + x_offset, basic_y + y_offset]
    move_inventory_position(base_coordinate, stone_position)
    click(button='left')
    sleep(0.3)
    move_inventory_position(base_coordinate, equip_position)
    click(button='left')
    sleep(0.3)
    check_result = strength_pre_check(basic_x, basic_y)
    if not check_result:
        click(x=basic_x - 163, y=basic_y + 130)
        sleep(0.2)
        click(x=basic_x - 78, y=basic_y + 130)
        return strengthen_equip(equip_position, stone_position, basic_coordinate)

    click(basic_x + confirm_x_offset, basic_y + confirm_y_offset, button='left')
    sleep(0.3)


def strength(equip_count=4, stone_per_equip=15):
    basic_x, basic_y = find_img_position('picture\\strengthen_title.png')

    equip_range = list(range(0, equip_count))
    stone_position = equip_count
    print('请保证装备从第一格开始连续放置，随后一格放强化石，程序于3秒后运行')
    sleep(3)

    for equip in equip_range:
        for i in range(stone_per_equip):
            strengthen_equip(equip, stone_position, [basic_x, basic_y])
            print(f'对第{equip}件装备完成第{i}次镶嵌')
