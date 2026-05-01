import os
import sys
import logging
from pathlib import Path


def set_logger():
	"""Function sets up a logging object which also constructs a logging file """
	# construct the logging object 'logger'
	logger = logging.getLogger("clean-log-test_logger")
	
	# define the path of 'log.txt' file oriented from project root
	project_root = Path(__file__).resolve().parent.parent
	if not os.path.exists(f"{project_root}/logs/"):
		os.mkdir(f"{project_root}/logs/")
	file_name = project_root / "logs" / "logs.txt"
	
	# construct file handler for 'log.txt' file
	file_handler = logging.FileHandler(
		filename=file_name,
		mode="w",
		encoding="utf-8"
	)
	file_format = logging.Formatter(
		fmt="%(lineno)s - %(asctime)s - %(levelname)s - %(funcName)s - %(message)s\n",
		datefmt="%d-%m-%Y %H.%M:%S"
	)
	file_handler.setFormatter(file_format)

	# construct stream handler for notebooks that import python files that incorporate logging object
	stream_handler = logging.StreamHandler(sys.stdout)

	stream_format = logging.Formatter(
		fmt="%(lineno)s - %(asctime)s - %(levelname)s - %(funcName)s - %(message)s",
		datefmt="%d-%m-%Y %H.%M:%S"
	)

	stream_handler.setFormatter(stream_format)

	# add file and stream handlers to the logging object
	logger.addHandler(file_handler)
	logger.addHandler(stream_handler)

	# define logging level of the object
	logger.setLevel(logging.DEBUG)

	return logger


logger = set_logger()