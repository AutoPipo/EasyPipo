# setup.py

from setuptools import setup, find_packages

setup(
    name='diy_maker',
    version='0.0.1',
    author='minku-Koo',
    author_email='corleone@kakao.com',
    description='hello flask',
    scripts = ["diy_maker"],
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.x',
        'License :: ',
        'Operating System :: OS Independent',
    ],
)

