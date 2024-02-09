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
    """
    A wrapper class for running docker containers
    """

    def __init__(self, image):
        """
        Initializes the container
        """
        self._image = image
        self._client = docker.from_env()
        self._container = None
        
    def remove(self, name):
        """
        Forcefully removes the docker container based on its name
        
        :param name: The name of the container
        
        :return: True if stopped and removed, False if container not found
        :rtype: bool
        """
        # container already running with specified name; stop it
        try:
            container = self._client.containers.get(name)
            # container exists when it should not
            container.remove(force=True)
            return True
        except docker.errors.NotFound:
            # container does not exist
            return False
        

    def run(self, volumes, port="8080", name=None):
        """
        Starts the docker container and mounts the volumes provided
        
        :param volumes: The data mount volumes that will be mounted in the container
        :param port: The port to expose on host to map to container's port 8080
        :param name: The name of the container
        """
        
        # remove container after exiting 
        rm = False
        if name:
            rm = True

        self._container = self._client.containers.run(self._image, detach=True, volumes=volumes, user=os.getuid(), ports={f'{port}/tcp': port},
                                                      name=name, auto_remove=rm)
        time.sleep(10)
        return self._container.name

    def stop(self):
        """
        Stop the docker container
        """
        self._container.stop()

    def save_logs(self, dirpath):
        """
        Dumps the logs of the container to the directory path specified
        
        :param dirpath: The absolute path to the directory where the logs will be saved
        """
        
        output = self._container.logs(timestamps=True).decode("utf-8") 
        filename = 'mistk_container_%s.log' % (self._container.name)
        with open(os.path.join(dirpath, filename), 'w') as writer:
            writer.write(output)
        return os.path.join(dirpath, filename)
        
    def add_network(self, network):
        """
        Add network to container
        
        :param network: Network to add
        """
        if self._container:
            network.connect(self._container)
            
            
