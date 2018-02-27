"""Handle image."""
from datetime import datetime
from base64 import b64encode
from tempfile import gettempdir
import shutil
import os
from os.path import join, abspath, dirname, isdir
import random

from nider.core import Font, Outline
from nider.models import Header, Content, Linkback, Paragraph, Image
import requests
from ajilog import logger

from goodmorning.pixabay import get_random_pic

PROJ_DIR = dirname(abspath(__file__))
TEMPDIR = gettempdir()
OUTPUT_DIR = join(TEMPDIR, 'shared')
if not isdir(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)


def _random_quotes():
    with open(join(PROJ_DIR, 'data', 'quotes.txt')) as f:
        sent = random.choice(f.readlines()).strip('\n')
    # add white space between each characters to make it break lines
    output = ' '.join(list(sent))
    if len(sent) < 9:
        font_size = 38
    elif len(sent) >= 9:
        font_size = 38 - (len(sent) - 9)
    if font_size < 20:
        font_size = 20
    return output, 40


def generate(text, font_path):
    """Generate good-morning picture."""
    logger.debug('download random picture')
    pic_url = get_random_pic()
    filepath = join(
        TEMPDIR, b64encode(pic_url.encode('utf-8')).decode('utf-8'))
    logger.debug('downloading pic from %s' % pic_url)
    resp = requests.get(pic_url, stream=True)
    logger.debug('writing img to disk: %s' % filepath)
    with open(filepath, 'wb') as f:
        shutil.copyfileobj(resp.raw, f)

    logger.debug('generating good-morning picture')
    text_outline = Outline(2, '#FFFFFF')

    header = Header(text=text,
                    font=Font(font_path, 40),
                    text_width=30,
                    align='left',
                    color='#FF0000',
                    outline=text_outline,
                    )
    quote, font_size = _random_quotes()
    para = Paragraph(text=quote,
                     font=Font(font_path, font_size),
                     text_width=15,
                     align='center',
                     color='#FF0000',
                     outline=text_outline,
                     )

    linkback = Linkback(text=('阿吉 %s' % str(datetime.now().date())),
                        font=Font(font_path, 20),
                        color='#FFFFFF',
                        # outline=text_outline,
                        )

    content = Content(header=header, paragraph=para, linkback=linkback)

    output_path = join(OUTPUT_DIR, 'good-morning.jpg')
    img = Image(content,
                fullpath=output_path,
                width=500,
                height=750
                )

    logger.debug('drawing')
    img.draw_on_image(filepath)

    logger.debug('deleting source image: %s' % filepath)
    os.remove(filepath)

    logger.debug('chmod output file to 777')
    os.chmod(output_path, 0o777)
    return output_path
