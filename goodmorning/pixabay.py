"""Retrieve image from pixabay.com."""
import os
import random

import requests


def get_random_pic():
    """Get random pictures."""
    url = 'https://pixabay.com/api/'
    params = {
        'key': os.environ['pixabay_key'],
        'q': 'flower',
        'image_type': 'photo',
        'orientation': 'horizontal',
        'per_page': 3,
        'page': random.choice(range(1, 151)),
    }
    resp = requests.get(url, params)
    data = resp.json()
    img_url = data['hits'][random.choice(range(3))]['webformatURL']
    return img_url
