from helper.mouse import find_img_click
from helper.image import find_img_position
from time import sleep


def auto_fight():
    while True:
        try:
            find_img_click('picture/npc.png')
            sleep(1)
            find_img_click('picture/confirm_fight.png')

            fail_fight_dialog = find_img_click('picture/fail_fight.png')
        except:
            print('失败了，等待重试')
            sleep(5)
