#!/usr/bin/env python3

'''
' setup.py
'
' Winston III package metadata.
'
' Will Badart <wbadart@nd.edu>
' created: OCT 2017
'''

from setuptools import setup


setup(name='winston',
      version='0.0.1-alpha',
      description='Simple virtual assistant',
      url='https://github.com/wbadart/Winston-III',
      author='Will Badart',
      author_email='wbadart@nd.edu',
      license='MIT',
      packages=['winston'],
      install_requires=[
          'pygame',
          'SpeechRecognition',
          'pyaudio',
          # 'pyyaml',
      ],
      zip_safe=False)
