from setuptools import setup
from setuptools import version

args = {
    'name': 'macro_for_maple', 
    'version': '0.1',
    'description': '',
    'url': 'https://github.com/GyuCheol/macro_for_maple',
    'author': 'GyuCheol Lee',
    'author_email': 'rbcjf0219@gmail.com',
    'license': 'MIT',
    'packages': [],
    'install_requires': [
        'pywin32',
        'opencv-python',
        'numpy',
        'pillow'
    ],
    'zip_safe': False
}


setup(**args)

