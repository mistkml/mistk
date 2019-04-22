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

import os
import docker
import time

class Container(object):

    def __init__(self, image):
        self._image = image
        self._client = docker.from_env()
        self._container = None

    def run(self, volumes):
        self._container = self._client.containers.run(self._image, detach=True, volumes=volumes, user=os.getuid(), ports={'8080/tcp': 8080})
        time.sleep(10)
        return self._container.name

    def stop(self):
        self._container.stop()
