import os
import pandas as pd

def read_file(file_name, data_format='list'):
	file_dir = os.path.join(os.getcwd(), file_name)
	file_format = file_name.split('.')[-1]
	data = []

	try:
		df = pd.read_csv(file_dir) if file_format == "csv" else pd.read_excel(file_dir)
		data = df.to_dict('records') if data_format == 'dict' else df.values.tolist()
	except Exception as e:
		print(e)
        
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