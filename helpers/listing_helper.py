import os
import shutil
import random
from loguru import logger
from helpers.file_helper import read_file
from helpers.img_helper import add_img_watermark, remove_img_meta, generate_multiple_images_path, crop_img
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

def upload(images, page):
	if not images:
		logger.warning('Product does not contain any image')
	
	# upload files
	page.wait_for_timeout(random.randint(1000, 3000))
	page.locator('css=input[accept="image/*,image/heif,image/heic"]').set_input_files(images)


def publish_listing(data, page, user, account, settings):
	
	if data['photos']:
		edited_img_dir = os.path.join(os.getcwd(), 'inputs', 'photos', 'edited')

		if user['duplicate_img']:
			watermark_text = settings['watermark_text'] if settings['watermark_text'] else account['mail']
			watermark_font_size = settings['watermark_font_size'] if settings['watermark_font_size'] else 40

			# crop images
			imgs_cropped = crop_img(data['photos'])

			# # add a watermark in images
			# imgs_watermarked = add_img_watermark(imgs_cropped, text=watermark_text, font_size=watermark_font_size)

			# # remove the infomation that remains attached to the image
			# imgs_exif_removed = remove_img_meta(imgs_watermarked) 

			# Create string that contains all of the image paths separeted by \n
			images_path = generate_multiple_images_path(imgs_cropped, user['multiple_img'], f_out=edited_img_dir)
		else:
			# Create string that contains all of the image paths separeted by \n
			images_path = generate_multiple_images_path(data['photos'], user['multiple_img'])


		# Add images to the the listing
		upload(images_path, page)
		page.wait_for_timeout(random.randint(1000, 3000))

		# deleting edited img folder, since it'll not be used anymore
		if user['duplicate_img']:
			shutil.rmtree(edited_img_dir)
	
	# Title
	page.wait_for_timeout(random.randint(1000, 3000))
	page.type('label[aria-label="Title"] input', str(data['title']))
	
	# Scroll to "Category" select field
	page.wait_for_timeout(random.randint(1000, 3000))
	select_category(selector='label[aria-label="Category"]', data=data, page=page)	
	
	# Scroll and select to "Condition"
	page.wait_for_timeout(random.randint(1000, 3000))
	page.click('label[aria-label="Condition"]')
	page.wait_for_timeout(random.randint(1000, 3000))
	page.click(f'div[role="option"]:has-text("{data["condition"].strip()}")')
	
	# price
	page.wait_for_timeout(random.randint(1000, 3000))
	page.type('label[aria-label="Price"] input', str(data['price']))

	# description (optional)
	if data['description']:
		page.wait_for_timeout(random.randint(1000, 3000))
		page.type('label[aria-label="Description"] textarea', data['description'])

	# tags (optional)
	if data['tags']:
		page.wait_for_timeout(random.randint(1000, 3000))
		for tag in data['tags'].split(';'):
			page.type('css=label[aria-label="Product tags"] textarea', tag)
			page.click('css=div[aria-label="Click to submit current value"]')

	# sku (optional)
	if data['sku_id']:
		page.wait_for_timeout(random.randint(1000, 3000))
		page.type('css=label[aria-label="SKU"] input', str(data['sku_id']))

	# location (optional)
	if data['location']:
		page.wait_for_timeout(random.randint(1000, 3000))
		page.fill('label[aria-label="Location"] input', '')
		page.type('label[aria-label="Location"] input', str(data['location']))
		page.wait_for_load_state('networkidle')
		page.wait_for_timeout(random.randint(3000, 5000))
		page.click('ul[role="listbox"] li:first-child > div')

	if not selector_exists(page, 'div[aria-label="Next"]'):
		page.wait_for_timeout(random.randint(1000, 3000))
		select_category(selector='label[aria-label="Category"]', data=data, page=page)	

	# Go to the next step
	page.wait_for_timeout(random.randint(1000, 3000))
	page.click('div[aria-label="Next"]')
	page.wait_for_load_state('networkidle')

	# few category items has 2nd Next button
	# if selector_exists(page, 'div[aria-label="Next"]'):
	# 	page.wait_for_timeout(random.randint(1000, 3000))
	# 	page.click('div[aria-label="Next"]')
	# 	page.wait_for_load_state('networkidle')

	# Add listing to multiple groups
	if data['groups']:
		if user['group_posting']:
			add_listing_to_multiple_groups(data['groups'], page)
		else:
			logger.warning('You are not allowed to use GROUP_POSTING feature. Buy to activate!')

	# Publish the listing
	page.wait_for_timeout(random.randint(1000, 3000))
	page.click('div[aria-label="Publish"]')
	page.wait_for_load_state('networkidle')


def add_listing_to_multiple_groups(groups_text, page):
	# Create an array for group names by spliting the string by this symbol ";"
	group_names = groups_text.split(';')

	# Post in different groups
	for group_name in group_names:
		# Remove whitespace before and after the name
		group_name = group_name.strip()

		page.click(f'span:text-is("{group_name}")')
		page.wait_for_timeout(random.randint(1000, 3000))

		
def select_category(selector, data, page):
	category_label = page.locator(selector)
	category_label.scroll_into_view_if_needed()
	category_label.click()

	# Scroll to "Category" value
	page.wait_for_timeout(random.randint(1000, 3000))
	categories = data['category'].split(';')

	for cat in categories:
		# try:
		# 	page.click(f'div[role="button"] span:text-is("{cat.strip()}")')
		# except:
		# 	page.click(f'div[role="radio"] span:text-is("{cat.strip()}")')

		page.click(f'span:text-is("{cat.strip()}")')
		page.wait_for_timeout(random.randint(1000, 3000))
		


def selector_exists(page, selector, timeout=3000):
	try:
		sel = page.locator(selector).is_visible(timeout=timeout)
		return sel
	except:
		return False
