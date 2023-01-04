import os

photos = ['1.png', '2.png', '3.png', ' 4.png']

items = ('\n').join([os.path.join(os.getcwd(), 'photos', item) for item in photos])

# a = 

print(items)