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


from setuptools import setup, find_packages


REQUIRES=[
    'setuptools == 21.0.0',
    'pandas == 0.20.3',
    'numpy == 1.22.0',
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