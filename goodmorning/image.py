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
from .conf import PROJ_PATH, TEMP_PATH, FONT_PATH, OUTPUT_PATH


weekday_trans = {
    0: '一', 1: '二', 2: '三', 3: '四', 4: '五', 5: '六', 6: '日'}


def _random_quotes():
    with open(join(PROJ_PATH, 'data', 'quotes.txt')) as f:
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


def generate(text, font, header_template=False, img_path=None):
    """Generate good-morning picture.

    Args:
    - text: Header text.
    - font: Font name.
    - header_template: If set true, '週x好' will be append to the header.
    - img_path: Image path. If not provide, random picture will be downloaded
                via "pixabay" API. (`pixabay_api` must be set in the system
                environment variables).

    Usage:
        generate('爹娘早安！', font='SourceHanSansTC-Medium.otf',
                               header_template=True,
                               img_path=None)
    """
    font_path = join(FONT_PATH, font)
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
        text += ' ' + template
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

    output_path = join(OUTPUT_PATH, 'good-morning.jpg')
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
