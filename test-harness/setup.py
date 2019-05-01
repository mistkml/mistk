##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################

import setuptools

REQUIRES=[
    'pandas == 0.20.3',
    'scikit-learn  == 0.19.1',
    'numpy == 1.13.3',
    'docker == 2.7.0',
    'scipy == 1.0.0',
    'mistk'
]


setuptools.setup(
    name='mistk-test-harness',
    packages=setuptools.find_packages(),
    package_data={'mistk_test_harness': ['*.json']},
    install_requires=REQUIRES,
    version='0.3.5'
    #use_scm_version = {"root": "..", "relative_to": __file__},
    #setup_requires=['setuptools_scm']
)
