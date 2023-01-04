from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import random
import os
import pathlib

def upload(images, page):
	if not images:
		raise Exception('No images to upload!')
	
	# upload files
	page.wait_for_timeout(random.randint(1000, 3000))
	page.locator('css=input[accept="image/*,image/heif,image/heic"]').set_input_files(images)

	page.wait_for_timeout(10000)

def generate_multiple_images_path(images):
	# Last character must be '/' because after that we are adding the name of the image
	# if path[-1] != '\\':
	# 	path += '\\'

	images_path = ''

	# Split image names into array by this symbol ";"
	image_names = images.split(';')

	# Create string that contains all of the image paths separeted by \n
	if image_names:
		# images_path = ('\n').join([os.path.join(path, item.strip()) for item in image_names])
		for image_name in image_names:
			# Remove whitespace before and after the string
			image_name = image_name.strip()

			# Add "\n" for indicating new file
			if images_path != '':
				images_path += '\n'

			images_path += os.getcwd().replace("\\", "/") + "/photos/" + image_name

	return images_path

# Remove and then publish each listing
def update_listings(listings, type, page):
	# Check if listing is already listed and remove it then publish it like a new one
	for listing in listings:
		# Remove listing if it is already published
		# remove_listing(listing, type, scraper)

		# Publish the listing in marketplace
		publish_listing(listing, type, page)

def publish_listing(data, listing_type, page):
	# go to listing page
	page.goto('https://www.facebook.com/marketplace/?ref=app_tab', wait_until='networkidle')

	# click on new listing 
	page.locator('css=a[aria-label="Create new listing"]').click()
	page.wait_for_load_state('networkidle')

	# click on new listing item
	page.wait_for_timeout(random.randint(1000, 3000))
	page.locator('css=span:has-text("Item for Sale") >> nth=1').click()
	page.wait_for_load_state('networkidle')

	# Create string that contains all of the image paths separeted by \n
	images_path = generate_multiple_images_path(data['photos'])
	# Add images to the the listing
	upload(images_path, page)
	page.wait_for_timeout(random.randint(1000, 3000))
	

	# Add specific fields based on the listing_type
	function_name = 'add_fields_for_' + listing_type
	# Call function by name dynamically
	globals()[function_name](data, page)
	
	page.wait_for_timeout(random.randint(1000, 3000))
	page.type('label[aria-label="Price"] input', str(data['price']), delay=200)
	page.wait_for_timeout(random.randint(1000, 3000))
	page.type('label[aria-label="Description"] textarea', data['description'], delay=200)

	#tags
	page.wait_for_timeout(random.randint(1000, 3000))
	for tag in data['tags'].split(';'):
		page.type('css=label[aria-label="Product tags"] textarea', tag, delay=200)
		page.click('css=div[aria-label="Click to submit current value"]')

	page.wait_for_timeout(random.randint(1000, 3000))
	page.fill('label[aria-label="Location"] input', '')
	page.type('label[aria-label="Location"] input', str(data['location']), delay=200)
	page.click('ul[role="listbox"] li:first-child > div', delay=3000)

	# Go to the next step
	page.click('div[aria-label="Next"]', delay=1000)

	# Publish the listing
	page.click('div[aria-label="Publish"]')

    # wait for network to finish loading
	page.wait_for_load_state('networkidle')


	# # Add listing to multiple groups
	# # add_listing_to_multiple_groups(data, scraper)


def selector_exists(page, selector, timeout=500):
    try:
        sel = page.wait_for_selector(selector, timeout=timeout, state='attached')
        return sel
    except PlaywrightTimeoutError:
        return False


def add_fields_for_items(data, page):
	# Title
	page.wait_for_timeout(random.randint(1000, 3000))
	page.type('label[aria-label="Title"] input', str(data['title']), delay=200)
	
	# Scroll to "Category" select field
	page.wait_for_timeout(random.randint(1000, 3000))
	category_label = page.locator('label[aria-label="Category"]')
	category_label.scroll_into_view_if_needed()
	category_label.click()

	# Scroll to "Category" value
	page.wait_for_timeout(random.randint(1000, 3000))
	categories = data['category'].split(';')

	for cat in categories:
		try:
			cat_selector = selector_exists(page, f'div[role="button"]:has-text("{cat.strip()}")')
			if cat_selector:
				cat_selector.click()
			else:
				page.click(f'div[role="radio"]:has-text("{cat.strip()}")')

			page.wait_for_timeout(random.randint(2000, 4000))
		except:
			page.fill('input[aria-label="Category"]', '')
			page.fill('input[aria-label="Category"]', categories[-1].strip())
	
	
	# Scroll and select to "Condition"
	page.wait_for_timeout(random.randint(1000, 3000))
	page.click('label[aria-label="Condition"]')
	page.click(f'div[role="option"]:has-text("{data["condition"].strip()}")')


# Add specific fields for listing from type vehicle
def add_fields_for_vehicles(data, scraper):
	# Expand vehicle type select
	scraper.element_click('label[aria-label="Vehicle type"]')
	# Select vehicle type
	scraper.element_click_by_xpath('//span[text()="' + data['Vehicle Type'] + '"]')

	# Scroll to years select
	scraper.scroll_to_element('label[aria-label="Year"]')
	# Expand years select
	scraper.element_click('label[aria-label="Year"]')
	scraper.element_click_by_xpath('//span[text()="' + data['Year'] + '"]')

	scraper.element_send_keys('label[aria-label="Make"] input', data['Make'])
	scraper.element_send_keys('label[aria-label="Model"] input', data['Model'])

	# Scroll to mileage input
	scraper.scroll_to_element('label[aria-label="Mileage"] input')	
	# Click on the mileage input
	scraper.element_send_keys('label[aria-label="Mileage"] input', data['Mileage'])

	# Expand fuel type select
	scraper.element_click('label[aria-label="Fuel type"]')
	# Select fuel type
	scraper.element_click_by_xpath('//span[text()="' + data['Fuel Type'] + '"]')

# Add specific fields for listing from type item


def generate_title_for_listing_type(data, listing_type):
	title = ''

	if listing_type == 'item':
		title = data['title']

	if listing_type == 'vehicle':
		title = data['Year'] + ' ' + data['Make'] + ' ' + data['Model']

	return title

def add_listing_to_multiple_groups(data, scraper):
	# Create an array for group names by spliting the string by this symbol ";"
	group_names = data['Groups'].split(';')

	# If the groups are empty do not do nothing
	if not group_names:
		return

	# Post in different groups
	for group_name in group_names:
		# Remove whitespace before and after the name
		group_name = group_name.strip()

		scraper.element_click_by_xpath('//span[text()="' + group_name + '"]')