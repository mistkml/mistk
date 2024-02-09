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
import importlib, inflection, functools
from urllib3.util.retry import Retry

from mistk import logger
import mistk.model.client as mistk_model_client
import mistk.transform.client as mistk_transform_client
import mistk.evaluation.client as mistk_evaluation_client
import mistk.agent.client as mistk_agent_client
import mistk.orchestrator.client as mistk_orchestrator_client


clients = ['model', 'transform', 'evaluation', 'agent', 'orchestrator']

# These are here just so that we have some auto-completion for IDEs; built below using functools.partial
#pylint: disable=unused-argument
def get_mistk_model_client(host=None, endpoint=None): return mistk_model_client.ApiClient() 
def get_mistk_transform_client(host=None, endpoint=None): return mistk_transform_client.ApiClient()
def get_mistk_evaluation_client(host=None, endpoint=None): return mistk_evaluation_client.ApiClient()
def get_mistk_agent_client(host=None, endpoint=None): return mistk_agent_client.ApiClient()
def get_mistk_orchestrator_client(host=None, endpoint=None): return mistk_orchestrator_client.ApiClient()


def get_client(apiCls, cfgCls, name, url=None):
    """
    Retrieves a client for the specified component name
    
    :param apiCls: The API class for the component 
    :param cfgCls: The Cfg class for the component
    :param name: The name of the component
    :param url: Optional URL for the host and port where the component is running. 
        This is retrieved from the configuration file if it is not provided.
    """
    config = cfgCls()
    url = url
    if url:
        config.host = url
        
    logger.debug(f' name: {name} , url: {url}')
    
    # If this service uses SSL, load the appropriate certificates. 
    if 'https://' in config.host:
        
        ssl_dir = os.environ.get('SML_SSL_DIR', '/etc/sml/ssl/')
        
        cert_file = os.path.join(ssl_dir, 'tls.crt')
        logger.debug('Loading SSL server certificate from %s' % cert_file)
        
        key_file = os.path.join(ssl_dir, 'tls.key')
        logger.debug('Loading SSL server key from %s' % key_file)
        
        ca_cert_file = os.path.join(ssl_dir, 'ca-cert.pem')
        logger.debug('Loading SSL CA Cert from %s' % ca_cert_file)
        
        config.cert_file=cert_file
        config.ssl_ca_cert=ca_cert_file
        config.key_file =key_file        
        config.assert_hostname = False
    
    client = apiCls(config)
    client.rest_client.pool_manager.connection_pool_kw['retries'] = Retry(connect=25, backoff_factor=.1)
    return client


for client in clients:
    m = importlib.import_module("mistk." + client + ".client")
    api = getattr(m, "ApiClient")
    cfg = getattr(m, "Configuration") 
    globals()["get_mistk_" + client + "_client"] = \
        functools.partial(get_client, api, cfg, client) 
