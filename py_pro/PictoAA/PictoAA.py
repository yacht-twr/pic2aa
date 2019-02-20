from PIL import Image, ImageFilter, ImageDraw, ImageFont
from tqdm import tqdm
import sys

config = open("ptaa_config.txt", "r")
configtextlist = config.readlines()
configlist = [configtextlist[i].strip() for i in range(len(configtextlist)) if not "#" in configtextlist[i]]

fontsize = int(configlist[0])
name = configlist[1]
name_parts = list(name)
num_of_chars_in_name = len(name_parts)

args = sys.argv
arg1 = args[1]

im_instance = Image.open(arg1)
im = im_instance.convert("L")

print(im.format, im.size, im.mode)

image_row = im.size[0]
image_column = im.size[1]
image_array = [["" for i in range(image_row)] for j in range(image_column)]

def num_transform_into_char(gray):
    divided_8bit = 255/(num_of_chars_in_name + 1)
    for i in range(num_of_chars_in_name):
        if gray > i * divided_8bit and gray <= (i+1) * divided_8bit:
            return name_parts[i]
    return "　"
"""
def output(aa_array, num_column, num_row):
    for j in range(num_column):
        for i in range(num_row):
            print(aa_array[j][i], end="")
        print("\n")
"""

for j in range(image_column):
    for i in range(image_row):
        gotpixel = im.getpixel((i,j))
        #gray = rgb_transform_into_gray(gotpixel)
        transformed_char = num_transform_into_char(gotpixel)
        image_array[j][i] = transformed_char
# output(image_array, image_column, image_row)

fixed_image_size = list(im.size)
fixed_image_size[0] += (fontsize-1)*im.size[0]
fixed_image_size[1] += (fontsize-1)*im.size[1]

white_canvas = Image.new("RGB", fixed_image_size, (255,255,255))
draw = ImageDraw.Draw(white_canvas)

place_of_font = configlist[2]
font = ImageFont.truetype(place_of_font, fontsize)

for i in tqdm(range(image_column)):
    jointed_char = "".join(image_array[i])
    draw.text((0, fontsize*i), jointed_char, fill=(0,0,0), font=font)

print("Picture name? : ", end="")
final_name = input().strip() + ".jpg"

white_canvas.save(final_name, "JPEG", quarity=100, optimize=True)

print("Completed!")
