# -*- coding: utf-8 -*-
#
# Content developed by Lockheed Martin ATL for AFRL/RIS 
# Contract #: FA8750-17-C-0282.
#
# Unlimited Government Rights
#
# Distribution C.  Distribution authorized to US Government agencies and
# their contractors Administrative or Operational Use, October 2017.
# Other requests for this document shall be referred to AFRL/RIS.


from setuptools import setup, find_packages

REQUIRES=[
    'mistk'
]

setup(
    install_requires=REQUIRES,
    name='mnist-logistic-regression',
    packages=find_packages()
)
