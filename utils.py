import os
import logging


logger = logging.getLogger()


def remove_file(file_path):
	if os.path.exists(file_path):
		os.remove(file_path)


def create_folder(folder_path):
	try:
		if not os.path.exists(folder_path):
			os.makedirs(folder_path)
	except Exception:
		logger.exception(f'could not create {folder_path}')


def add_padding(padee, length):
	padee = str(padee)
	while len(padee) < length:
		padee = '0' + padee
	return padee
