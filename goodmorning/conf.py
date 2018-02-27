"""Configurations."""
from tempfile import gettempdir
from os.path import abspath, dirname, join, isdir
import os

PROJ_DIR = dirname(abspath(__file__))
TEMP_PATH = gettempdir()
OUTPUT_DIR = join(TEMP_PATH, 'shared')
if not isdir(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

FONT_DIR = 'fonts'
