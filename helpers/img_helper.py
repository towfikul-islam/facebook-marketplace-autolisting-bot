import os
import random
from exif import Image
from loguru import logger
from PIL import Image, ImageDraw, ImageFont

logger.add('logs.txt')

def check_format(filename):
    img_formats = ['png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG']
    file_format = filename.split('.')[-1]

    if file_format not in img_formats:
        logger.error(f"Image: {filename} | {file_format} is not supported in editing mode")

def add_img_watermark(photo_title, text, f_in=os.path.join(os.getcwd(), 'photos'), f_out=os.path.join(os.getcwd(), 'photos', 'modified')):
    if not os.path.exists(f_out):
        os.mkdir(f_out)

    photo_path = os.path.join(f_in, photo_title)
    check_format(photo_path)

    #Create an Image Object from an Image
    im = Image.open(photo_path)
    width, height = im.size

    draw = ImageDraw.Draw(im)

    font = ImageFont.truetype('fonts/DancingScript-Medium.ttf', 50)
    textwidth, textheight = draw.textsize(text, font)

    # calculate the x,y coordinates of the text
    free_width = width - textwidth
    free_height = height - textheight

    margin = 10
    x = random.randrange(margin, free_width)
    y = random.randrange(margin, free_height)

    draw.text((x, y), text, font=font)

    # convert png to jpg since exif supports only JPG
    img = im.convert('RGB')

    #Save watermarked image
    img.save(os.path.join(f_out, f"{'.'.join(photo_title.split('.')[:-1])}.jpg"))

    logger.success(f"image: {photo_title} | watermark applied | saved as {photo_title}.jpg")


def remove_img_meta(photo_title, f_in=os.path.join(os.getcwd(), 'photos', 'modified'), f_out=os.path.join(os.getcwd(), 'photos', 'modified')):
    photo_path = os.path.join(f_in, photo_title)
    check_format(photo_path)

    with open(photo_path, "rb") as f:
        photo = Image(f)
    
    photo.delete_all()

    with open(f_out, 'wb') as f:
        f.write(photo.get_file())
    
    logger.success(f"image: {photo_title} | metadata removed | image saved")