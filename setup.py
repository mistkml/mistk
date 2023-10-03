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
    'Werkzeug >= 0.16.1',
    'connexion >= 1.1.15',
    'certifi >= 2019.6.16',
    'python-dateutil >= 2.6.1',
    'setuptools >= 21.0.0',
    'transitions == 0.6.4',
    'pypubsub == 4.0.0',
    'rwlock == 0.0.7',
    'wsgiserver == 1.3',
    'autologging >= 1.2.1',    
    'PyYAML >= 5.1.0',
    'urllib3 >= 1.25.3',
    'six >= 1.12.0',
    'gevent == 23.9.1',
    'bottle >= 0.12.16',
    'flask >= 1.0.2',
    'csvvalidator >= 1.2'
]

version_args = {"version": "1.0.2"}

setuptools.setup(
    name='mistk',
    packages=setuptools.find_packages() + ['conf'],
    package_data={'conf': ['*.ini', 'log_config.json']},
    include_package_data=True,
    install_requires=REQUIRES,
    **version_args)
