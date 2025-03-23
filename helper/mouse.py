from helper.image import find_img_position
from ascript.windows.action import mouse_move, click

def find_img_click(image_name):
    image_position = find_img_position(image_name)
    mouse_move(image_position[0], image_position[1], duration=0.3)
    click(button='left')