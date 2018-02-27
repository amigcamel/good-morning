"""Configurations."""
from tempfile import gettempdir
from os.path import abspath, dirname, join, isdir
import os

PROJ_PATH = dirname(abspath(__file__))
TEMP_PATH = gettempdir()
OUTPUT_PATH = join(TEMP_PATH, 'shared')
if not isdir(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)

FONT_PATH = 'fonts'
