# -*- coding: utf-8 -*-
import os
import sys
import warnings
from tqdm import tqdm
import logging

root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../..')
dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(root_path)

logging.basicConfig(level=logging.DEBUG)


class PDFOCR(object):
    """
    将PDF文本转换为txt或者word
    """
    def __init__(self):
        """
        Initialization.
        """
        # Set file path.
        self.data_path = os.path.join(dir_path, 'data')

    def run(self):
        """
        执行OCR转换

        :return:
        """

