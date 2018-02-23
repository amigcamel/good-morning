"""Setup."""
from setuptools import setup, find_packages

external_modules = [
    'ajilog==0.0.3',
    'nider==0.4.1',
    'requests==2.18.4',
]

if __name__ == '__main__':
    setup(
        name='goodmorning',
        version='0.0.0',
        packages=find_packages(),
        install_requires=external_modules,
        description='Random generator of "good-morning picture"',
        author='Aji Liu',
        author_email='amigcamel@gmail.com',
    )
