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

import docker

class Network(object):
    """
    A wrapper class to create docker networks
    """

    def __init__(self, name):
        """
        Initializes the network
        """
        self._client = docker.from_env()
        self.name = name
        self.network = None
        self.created = False
    
    def create_network(self):
        """
        Gets the docker network and creates the network if it does not exist. The network reference
        is stored in the classes network parameter
        
        :param name: Name of network to create 
        
        :return: Boolean for if the network was created
        """
        # created network
        network = None
        network_created = False
        try:
            network = self._client.networks.get(self.name)
        except docker.errors.NotFound as nf:
            network = self._client.networks.create(self.name)
            network_created = True
        except docker.errors.APIError as api:
            network = None
        self.network = network
        self.created = network_created
        return network_created
    
    def delete_network(self):
        """
        Deletes the docker network 
        
        :return: Boolean for if the network was deleted
        """
        network_deleted = False
        try:
            network = self._client.networks.get(self.name)
            network.remove()
            network_deleted = True
        except docker.errors.NotFound as nf:
            return network_deleted
        except docker.errors.APIError as api:
            return network_deleted
        self.created = False
        return network_deleted
        
            
            
