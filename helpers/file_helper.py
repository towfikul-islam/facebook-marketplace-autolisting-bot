import os
import pandas as pd
from loguru import logger

def read_file(file_name, worksheet, data_format='dict'):
	file_dir = os.path.join(os.getcwd(), file_name)
	data = []

	try:
		df = pd.read_excel(file_dir, sheet_name=worksheet) if worksheet else pd.read_excel(file_dir)
		df = df.where(pd.notnull(df), False)
		data = df.to_dict('records') if data_format == 'dict' else df.values.tolist()
	except Exception as e:
		logger.error("You must save and close the excel file while the script is running")
	return data


def write_file(data, file_name, labels=None):
	file_dir = os.path.join(os.getcwd(), file_name)
	file_format = file_name.split('.')[-1]
	header = True if labels else False
    
	try:
		df = pd.DataFrame(data, columns=labels)
		if file_format == 'csv':
			df.to_csv(file_dir, index=False, header=header)
		else:
			df.to_excel(file_dir, index=False, header=header)
	except PermissionError:
		print(f"PermissionError: Your file {file_name} is open with another application, Close the file first.")
		input('Script stopped. Press Anykey to continue execution...')
		write_file(data, file_name, file_format, labels)