"""Handle image."""
from datetime import datetime
from base64 import b64encode
import shutil
import os
from os.path import join, isfile
import random

from nider.core import Font, Outline
from nider.models import Header, Content, Linkback, Paragraph, Image
import requests
from ajilog import logger

from .pixabay import get_random_pic
from .conf import PROJ_DIR, TEMP_PATH, FONT_DIR, OUTPUT_DIR


weekday_trans = {
    0: '一', 1: '二', 2: '三', 3: '四', 4: '五', 5: '六', 6: '日'}


def _gen_quotes():
    with open(join(PROJ_DIR, 'data', 'quotes.txt')) as f:
        return random.choice(f.readlines()).strip('\n')


def _calc_font_size(text):
    if len(text) < 9:
        font_size = 38
    elif len(text) >= 9:
        font_size = 38 - (len(text) - 9)
    if font_size < 20:
        font_size = 20
    return font_size


def generate(font,
             title='',
             content='',
             author='',
             header_template=True,
             img_path=None):
    """Generate good-morning picture.

    Args:
    - font: Font name.
    - title: title text.
    - content: content text.
    - author: author name.
    - header_template: If set true, '週x好' will be append to the header.
    - img_path: Image path. If not provide, random picture will be downloaded
                via "pixabay" API. (`pixabay_api` must be set in the system
                environment variables).

    Usage:
        # completely generate random good-morning picture
        generate(font='SourceHanSansTC-Medium.otf')
        # with custom settings
        generate(font='SourceHanSansTC-Medium.otf',
                 title='爹娘早安！',
                 author='阿吉')
    """
    font_path = join(FONT_DIR, font)
    if not isfile(font_path):
        raise FileNotFoundError(font_path)
    logger.debug('download random picture')
    pic_url = get_random_pic()
    if img_path:
        filepath = img_path
    else:
        filepath = join(
            TEMP_PATH, b64encode(pic_url.encode('utf-8')).decode('utf-8'))
        logger.debug('downloading pic from %s' % pic_url)
        resp = requests.get(pic_url, stream=True)
        logger.debug('writing img to disk: %s' % filepath)
        with open(filepath, 'wb') as f:
            shutil.copyfileobj(resp.raw, f)
    logger.debug('generating good-morning picture')
    text_outline = Outline(2, '#FFFFFF')

    if header_template:
        template = '週%s好！' % weekday_trans[datetime.now().weekday()]
        title += ' ' + template
    header = Header(text=title,
                    font=Font(font_path, 40),
                    text_width=30,
                    align='left',
                    color='#FF0000',
                    outline=text_outline,
                    )
    if not content:
        content = _gen_quotes()
    font_size = _calc_font_size(content)
    # add white space between each characters to make it break lines
    content = ' '.join(list(content))
    logger.debug('content: ' + content)
    para = Paragraph(text=content,
                     font=Font(font_path, font_size),
                     text_width=15,
                     align='center',
                     color='#FF0000',
                     outline=text_outline,
                     )

    linkback = Linkback(text=('%s %s' % (author, str(datetime.now().date()))),
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

    if not img_path:
        logger.debug('deleting source image: %s' % filepath)
        os.remove(filepath)

    logger.debug('chmod output file to 777')
    os.chmod(output_path, 0o777)
    return output_path
