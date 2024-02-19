import math

import numpy as np
from numpy import genfromtxt
import logging


class LogParser:
    def __init__(self, logger: logging.Logger):
        self.__logger = logger
        self.data = None
        self.__headers = []

    @property
    def headers(self):
        return self.__headers

    def get_data(self, name: str):
        if name in self.__headers:
            return self.data[name]
        return []

    def parse(self, filename: str):
        filename = filename
        self.data = genfromtxt(filename, delimiter=';', names=True)
        self.__headers = self.data.dtype.names
