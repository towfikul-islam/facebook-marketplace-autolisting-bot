import random
import os

def upload(images, page):
	if not images:
		raise Exception('No images to upload!')
	
	# upload files
	page.wait_for_timeout(random.randint(1000, 3000))
	page.locator('css=input[accept="image/*,image/heif,image/heic"]').set_input_files(images)

	page.wait_for_timeout(10000)

def generate_multiple_images_path(path, images):
	# Last character must be '/' because after that we are adding the name of the image
	if path[-1] != '\\':
		path += '\\'

	images_path = ''

	# Split image names into array by this symbol ";"
	image_names = images.split(';')

	# Create string that contains all of the image paths separeted by \n
	if image_names:
		for image_name in image_names:
			# Remove whitespace before and after the string
			image_name = image_name.strip()

			# Add "\n" for indicating new file
			if images_path != '':
				images_path += '\n'

			images_path += path + image_name

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
	images_path = generate_multiple_images_path('photos', data['photos'])
	# Add images to the the listing
	upload(images_path, page)
	page.wait_for_timeout(random.randint(1000, 3000))
	

	# Add specific fields based on the listing_type
	function_name = 'add_fields_for_' + listing_type
	# Call function by name dynamically
	globals()[function_name](data, page)
	
	# scraper.element_send_keys('label[aria-label="Price"] input', data['Price'])
	# scraper.element_send_keys('label[aria-label="Description"] textarea', data['Description'])
	# scraper.element_send_keys('label[aria-label="Location"] input', data['Location'])
	# scraper.element_click('ul[role="listbox"] li:first-child > div')

	# # Go to the next step
	# scraper.element_click('div [aria-label="Next"] > div')

	# # Add listing to multiple groups
	# # add_listing_to_multiple_groups(data, scraper)

	# # Publish the listing
	# scraper.element_click('div[aria-label="Publish"]')


def add_fields_for_item(data, page):
	# Title
	page.wait_for_timeout(random.randint(1000, 3000))
	title_input = page.locator('css=label[aria-label="Title"] input')
	title_input.fill('')
	title_input.type(data['title'], delay=200)

	# Price
	page.wait_for_timeout(random.randint(1000, 3000))
	title_input = page.locator('css=label[aria-label="Price"] input')
	title_input.fill('')
	title_input.type(str(data['price']), delay=200)
	
	# Scroll to "Category" select field
	page.wait_for_timeout(random.randint(1000, 3000))
	category_label = page.locator('label[aria-label="Category"]')
	category_label.scroll_into_view_if_needed()
	category_label.click()

	# Scroll to "Category" value
	page.wait_for_timeout(random.randint(1000, 3000))
	for cat in data['category'].split(';'):
		try:
			cat_selector = page.locator('css=div[role="button"] span', has_text=cat.strip())
		except:
			cat_selector = page.locator('css=div[role="radio"] span', has_text=cat.strip())
			cat_selector.last()

		cat_selector.scroll_into_view_if_needed()
		cat_selector.click()
		page.wait_for_timeout(random.randint(1000, 3000))

	os.system('pause')
	# page.wait_for_timeout(random.randint(1000, 3000))
	# category_value = page.locator('xpath=//span[contains(text(),"'+ data['category'] + '")]')
	# category_value.scroll_into_view_if_needed()
	# category_value.click()

	# # Expand category select
	# scraper.element_click('label[aria-label="Condition"]')
	# # Select category
	# scraper.element_click_by_xpath('//span[@dir="auto"][text()="' + data['Condition'] + '"]')

	# if data['Category'] == 'Sports & Outdoors':
	# 	scraper.element_send_keys('label[aria-label="Brand"] input', data['Brand'])

# def remove_listing(page):	
# 	title = generate_title_for_listing_type(data, listing_type)
	
# 	page.goto("https://www.facebook.com/marketplace/you/selling", wait_until="networkidle")

# 	page.wait_for_timeout(random.randint(1000, 3000))
# 	searchInput = page.locator('input[placeholder="Search your listings"]')

# 	# Search input field is not existing	
# 	if not searchInput:
# 		return

	
# 	# Clear input field for searching listings before entering title
# 	searchInput.fill('')

# 	# Enter the title of the listing in the input for search
# 	searchInput.type(title, delay=200)

# 	# Search for the listing by the title
# 	listing_title = page.locator('//span[text()="' + title + '"]', False, 3)

# 	# Listing not found so stop the function
# 	if not listing_title:
# 		return

# 	listing_title.click()

# 	# Click on the delete listing button
# 	scraper.element_click('div[aria-label="Delete"]')
# 	# Click on confirm button to delete
# 	scraper.element_click('div[aria-label="Delete Listing"] div[aria-label="Delete"][tabindex="0"]')
# 	# Wait until the popup is closed
# 	scraper.element_wait_to_be_invisible('div[aria-label="Your Listing"]')

# Add specific fields for listing from type vehicle
def add_fields_for_vehicle(data, scraper):
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