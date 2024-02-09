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
import sys
import numpy as np
from typing import Dict, List, Union

# To import any learners in this directory
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from mistk.agent.abstract_agent import AbstractAgent
import mistk.log
logger = mistk.log.get_logger()

class TestAgent (AbstractAgent):
    """ Agent that produces random integers
    """
    def __init__(self):
        AbstractAgent.__init__(self)
        self._props = None
        self._model_file_name = 'test-agent.mdl'
        self._training_data = None
        self._testing_data = None
        self._predictions = None
        self._generations = []
        self._stream_props = None

        logger.info("Agent started")

    def do_initialize(self, props : dict, hparams : dict):
        """ Initializes the Random Learner

        Learner Args (put these in hparams):
            'low': Set this to the lowest int that can be returned
            'high': Set this to the highest int that will not be returned.
                In other words if this is 2, we may return 1, but never 2.
            'size': How many ints should be returned.

        Args:
            props (dict): Not used.
            hparams (dict): Parameters for the learner. Args defined above.
        """
        self._props = props or {}
        self._hparams = hparams or {}
        logger.info(f"do_initialize called for the Test Agent with: {self._props}")

    def do_build_model(self, path: str = ''):
        logger.info("do_build_model called")

    def do_save_model(self, path):
        if path:
            logger.info("we cannot save a Random Learner")

    def do_agent_registered(self, agent_cfg: dict):
        logger.info("do_agent_registered called")
        logger.info(f"agent config: {agent_cfg}")

    def do_episode_started(self, episode_cfg: dict):
        logger.info("do_episode_started called")
        # If the learner must be reset with the current obs, it needs to happen
        # here. The current obs will be in `episode_cfg['obs']`
        logger.info(f"episode config: {episode_cfg}")
        pass

    def do_get_action(self, obs: Dict[str, List[Union[int, float]]]) -> Dict[str, List[int]]:
        logger.info(f"do_get_action for a Random Learner called with obs={obs}")
        rng = np.random.default_rng()
        rng_ints = rng.integers(low=self._hparams['low'],
                                high=self._hparams['high'],
                                size=self._hparams['size'])
        action = {self.agent_name: [int(x) for x in rng_ints]}
        logger.info(f"The random learner will return: {action}")
        return action

    def do_replay_action(self, obs: Dict[str, Union[List[Union[int, float]], bool]]):
        logger.info("do_replay_action called")
        logger.info(f"observations: {obs}")

    def do_episode_stopped(self):
        logger.info("do_episode_stopped called")

    def do_pause(self):
        logger.info("do_pause called")

    def do_terminate(self):
        pass

    def do_reset(self, unload_model):
        logger.info("do_reset called")
        logger.info(f"unload_model: {unload_model}")
        pass
