import os
import random
import json
import argparse
from PIL import Image, ImageDraw, ImageFont
from colorutils import Color


def get_rnd_color():
    with open('colornames.json', 'r') as color_file:
        color_list = json.load(color_file)
        color_dict = dict()
        for c in color_list:
            color_dict[list(c.values())[1]] = list(c.values())[0]
        color_hex = random.choice(list(color_dict.keys()))
        color_name = color_dict[color_hex]
    color_obj = Color(hex=color_hex)
    color_rgb = (color_obj.red, color_obj.green, color_obj.blue)
    return (color_name, color_hex, color_rgb)


def create_wallpaper(color_info, width, height):
    os.makedirs('Wallpapers', exist_ok=True)
    img = Image.new('RGB', (width, height), color_info[2])
    draw = ImageDraw.Draw(img)
    if height < width:
        font = ImageFont.truetype(
            'NotoSansMono-Regular.ttf', int(height*0.03))
    else:
        font = ImageFont.truetype(
            'NotoSansMono-Regular.ttf', int(width*0.03))
    ancor = (int(width*0.3), int(height*0.3))
    text = str(color_info[0] +
               '\nhex ' + color_info[1] +
               '\nrgb ('+str(color_info[2][0]) +
               ', ' + str(color_info[2][1]) +
               ', ' + str(color_info[2][2]) + ')')
    if (sum(list(color_info[2]))/3 < 128):
        text_color = (255, 255, 255)
    else:
        text_color = (0, 0, 0)
    draw.text(xy=ancor, text=text, font=font, fill=text_color)
    text_bbox = draw.multiline_textbbox(xy=ancor, text=text, font=font)
    draw.rectangle(
        ((text_bbox[0]-int((text_bbox[2]-text_bbox[0])*0.10),
          text_bbox[1]-int((text_bbox[3]-text_bbox[1])*0.10)),
         (text_bbox[2]+int((text_bbox[2]-text_bbox[0])*0.10),
          text_bbox[3]+int((text_bbox[3]-text_bbox[1])*0.10))),
        outline=text_color, width=int((text_bbox[3]-text_bbox[1])*0.03))
    img.save('./Wallpapers/'+color_info[0]+'.png', 'png')


def main():
    parser = argparse.ArgumentParser(
        prog='ColorWallpaperGenerator', description='Generate random color wallpaper from selection of up to 30k named colors.')
    parser.add_argument('-c', '--count', action='store',
                        default=1, dest='count', type=int)
    parser.add_argument('--width', action='store',
                        default=3840, type=int)
    parser.add_argument('--height', action='store',
                        default=2160, type=int)
    args = parser.parse_args()
    for i in range(0, args.count):
        create_wallpaper(get_rnd_color(), args.width, args.height)


if __name__ == "__main__":
    main()
