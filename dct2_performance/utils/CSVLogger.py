import csv
import os
from datetime import datetime


class CSVLogger:
    """
    Class to simplify logging the runs data to .csv files.
    """
    def __init__(self, filename: str = None, path: str = "") -> None:
        """
        CSVLogger constructor.
        :param filename: Log file name
        :param path: Path to save the file to
        """
        self._log_file = self._create_log_file_path(filename, path)

    @property
    def log_file(self) -> str:
        return self._log_file

    def _create_log_file_path(self, filename: str, path: str) -> str:
        """
        Method to create the logs file path.
        :param filename: Name of the log file
        :param path: Path to save the file to
        :return: Full path file
        """
        if filename is None:
            filename = 'dct2_benchmark'

        filename += "_" + datetime.now().strftime("%Y_%m_%d_%H%M%S") + ".csv"
        log_file = os.path.join(path, filename)

        os.makedirs(path, exist_ok=True)
        return log_file

    def write_row(self, data: dict) -> None:
        """
        Method to write a row to the logs file. If the file is empty, it writes the header first
        :param data: dict of data to write
        """
        with open(self._log_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            if os.stat(self._log_file).st_size == 0:
                writer.writeheader()
            writer.writerow(data)
