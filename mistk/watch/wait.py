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

import time
from mistk import logger

def wait_for_state(service, stage, state):
        """
        Waits for a model or transform service wrapper to change their 
        state to the desired state
        
        :param service: The model, transform, evaluation, agent, or orchestrator service to get status for
        :param stage: The current stage of the container
        :param state: The desired state of the container        
        """
        logger.info(f'Called \'{stage}\' on container, waiting for state change to \'{state}\'')
        status_version = 0
        initial_delay = 1
        delay = .5
        time.sleep(initial_delay)
        st = service.get_status()
        while status_version == st.object_info.resource_version:
            time.sleep(delay)
            st = service.get_status()
        
        if isinstance(state, str):
            state = [state]
        
        while not st.state in state and not st.state == 'failed':
            if status_version != st.object_info.resource_version:
                logger.debug('Endpoint state: %s (%s)' % (st.state, str(st.payload)))
                status_version = st.object_info.resource_version
            time.sleep(delay)
            st = service.get_status()
            
        logger.debug('Endpoint state: %s' % st.state)
        status_version = st.object_info.resource_version
        
        if st.state == 'failed':
            msg = 'Endpoint in failed state, exiting'
            print(msg)
            raise Exception(msg)
        