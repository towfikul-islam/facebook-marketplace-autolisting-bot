import csv

def get_data_from_csv(csv_file_name):
	data = []

	try:
		with open(csv_file_name, encoding="UTF-8-SIG") as csv_file:
			csv_dictionary = csv.DictReader(csv_file, delimiter=',')

			for dictionary_row in csv_dictionary:
				data.append(dictionary_row)
	except:
		print('File was not found:' + csv_file_name)
		return None

	return data