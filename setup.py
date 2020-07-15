import setuptools
from setuptools import setup

setup(name='twitter_word_cloud',
      version='1.2',
      author="Ayman Sherief",
      author_email="aymanf.sherief@gmail.com",
      description='Generate word cloud charts from twitter',
      long_description=open("README.md").read().replace('#', ''),
      url="https://github.com/Aymanf-sherief/TwitterWordCloud",
      packages=setuptools.find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      zip_safe=False)
