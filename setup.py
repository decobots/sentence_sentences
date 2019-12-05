from distutils.core import setup

from setuptools import find_packages

setup(
    name='sentence_sentences',
    version='1.6',
    description='An old hangman game with a new twist.',
    author='Maria Pritchina',
    author_email='pritchina.m.i@gmail.com',
    packages=find_packages(where="src"),
    package_dir={"": "src"},

)