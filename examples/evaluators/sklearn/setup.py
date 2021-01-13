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
    'setuptools == 21.0.0',
    'pandas == 0.20.3',
    'numpy == 1.13.3',
    'scikit-learn  == 0.19.1',
    'SciPy == 1.1.0',
    'mistk'
]

setup(
    name='sklearn-evaluations',
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'sklearn_evaluations': ['*.json']},
    include_package_data=True
)