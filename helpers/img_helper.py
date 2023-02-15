import os
import random
from PIL import Image as PIL_IMAGE
from PIL import ImageDraw, ImageFont
from exif import Image as EXIF_IMAGE
from loguru import logger

def check_format(filename):
    img_formats = ['png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG']
    file_format = filename.split('.')[-1]

    if file_format not in img_formats:
        logger.error(f"Image: {filename} | {file_format} is not supported in editing mode")

def add_img_watermark(images, text, font_size, f_in=os.path.join(os.getcwd(), 'inputs', 'photos', 'edited'), f_out=os.path.join(os.getcwd(), 'inputs', 'photos', 'edited')):
    if not os.path.exists(f_out):
        os.mkdir(f_out)

    image_names = images.split(';')
    edited = []

    for image_name in image_names:
        image_name = image_name.strip()
        photo_path = os.path.join(f_in, image_name)
        
        #Create an Image Object from an Image
        im = PIL_IMAGE.open(photo_path)
        width, height = im.size

        draw = ImageDraw.Draw(im)

        font = ImageFont.truetype(os.path.join(os.getcwd(), 'inputs', 'fonts', 'DancingScript-Medium.ttf'), font_size)
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

        output_name = f"{'.'.join(image_name.split('.')[:-1])}.jpg"

        #Save watermarked image
        img.save(os.path.join(f_out, output_name))

        edited.append(output_name)

        logger.success(f"{image_name} | watermark applied | saved as JPG")

    return ';'.join(edited)   


def crop_img(images, f_in=os.path.join(os.getcwd(), 'inputs', 'photos'), f_out=os.path.join(os.getcwd(), 'inputs', 'photos', 'edited')):
    if not os.path.exists(f_out):
        os.mkdir(f_out)

    image_names = images.split(';')
    edited = []

    for image_name in image_names:
        image_name = image_name.strip()
        photo_path = os.path.join(f_in, image_name)
        
        #Create an Image Object from an Image
        im = PIL_IMAGE.open(photo_path)
        width, height = im.size

        # generate random cropping co-ordinates
        margin = round((width/random.randrange(10,15))+(height/random.randrange(10,15))/2)
        left = random.randrange(0, margin)
        right = width - random.randrange(0, margin)
        top = random.randrange(0, margin)
        bottom = height - random.randrange(0, margin)

        # crop the image
        cropped = im.crop((left, top, right, bottom))

        #Save cropped image
        cropped.save(os.path.join(f_out, image_name))

        edited.append(image_name)

        logger.success(f"{image_name} | cropped | saved")

    return ';'.join(edited)   


def remove_img_meta(images, f_in=os.path.join(os.getcwd(), 'inputs', 'photos', 'edited'), f_out=os.path.join(os.getcwd(), 'inputs', 'photos', 'edited')):
    image_names = images.split(';')

    for image_name in image_names:
        photo_path = os.path.join(f_in, image_name.strip())
        check_format(photo_path)

        with open(photo_path, "rb") as f:
            photo = EXIF_IMAGE(f)
        
        if photo.has_exif:
            photo.delete_all()

            with open(f_out, 'wb') as f:
                f.write(photo.get_file())
        
        logger.success(f"{image_name} | metadata removed | saved")

    return images

def generate_multiple_images_path(images, multiple_feature, f_out=os.path.join(os.getcwd(), 'inputs', 'photos')):
    image_names = []

    # Split image names into array by this symbol ";" and make a list
    for image_name in images.split(';'):
        image_names.append(os.path.join(f_out, image_name))

    return image_names
    