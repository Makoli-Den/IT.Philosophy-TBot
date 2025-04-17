import logging
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from config.settings import LOG_DIR, LOG_LEVEL, LOG_RETENTION_DAYS

load_dotenv()

class Logger:
	_logger = None

	@classmethod
	def get_logger(cls):
		if cls._logger:
			return cls._logger

		log_level = getattr(logging, LOG_LEVEL, logging.INFO)

		if not os.path.exists(LOG_DIR):
			os.makedirs(LOG_DIR)

		cls._delete_old_logs()

		today = datetime.now().strftime("%Y-%m-%d")
		log_filename = os.path.join(LOG_DIR, f"{today}.log")

		logger = logging.getLogger("AppLogger")
		logger.setLevel(log_level)

		formatter = logging.Formatter(
			'[%(asctime)s] [%(levelname)s] [%(module)s.%(funcName)s] %(message)s',
			datefmt='%Y-%m-%d %H:%M:%S'
		)

		file_handler = logging.FileHandler(log_filename)
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)

		stream_handler = logging.StreamHandler()
		stream_handler.setFormatter(formatter)
		logger.addHandler(stream_handler)

		cls._logger = logger
		return cls._logger

	@staticmethod
	def _delete_old_logs():
		cutoff_date = datetime.now() - timedelta(days=LOG_RETENTION_DAYS)

		for filename in os.listdir(LOG_DIR):
			if filename.endswith(".log"):
				filepath = os.path.join(LOG_DIR, filename)
				try:
					file_date_str = filename.replace(".log", "")
					file_date = datetime.strptime(file_date_str, "%Y-%m-%d")
					if file_date < cutoff_date:
						os.remove(filepath)
				except ValueError:
					continue