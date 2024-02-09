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

from mistk.orchestrator.abstract_orchestrator import AbstractOrchestrator
from mistk.watch.wait import wait_for_state
import mistk.log
logger = mistk.log.get_logger()

class TestOrchestrator (AbstractOrchestrator):
    def __init__(self):
        AbstractOrchestrator.__init__(self)
        self._props = None
        self._orchestrator_file_name = 'test-orchestrator.mdl'
        self._agents_needed = NotImplemented
        self._default_env = {}

        self.step_num = 0

        logger.info("Orchestrator started")

    def do_initialize(self, env: dict = {}, agents_needed: int = 1):
        """ This initializes Airlift Orchestrator

        Args:
            env (dict, optional): Dictionary which has keyword args that will
                be used for the env's initialization method [Default = None]
            agents_needed (int, optional): Number of agents who'll play in
                this game. [Default = 1]
        """
        env_dict = env if env else self._default_env
        self._agents_needed = int(agents_needed)

        logger.info("do_initialize called")
        logger.info(f"Initializing the Test Orchestrator with:  {env_dict}")

        # TODO: Call Initialize Method to Environment
        # TODO: Call Reset Method to Environment

    def do_register_agent(self, agent_name: str, agent_url: str):
        """
        Instructs the service to register all of the agents this orchestrator
        will work with.

        :param agent_name: The name of the agent
        :param agent_url: The agent URL
        """
        pass

    def do_start_episode(self, episode_cfg: dict):
        """
        Begins starting the episode of playing the game

        :param episode_cfg: Dictionary with the episode's config settings
        """
        logger.info("Starting episode")
        for agent in self._agents:  # Tells each agent to start an episode
            try:
                episode_cfg['obs'] =  {agent: [0]}
                self._agents[agent].episode_started(episode_cfg=episode_cfg)
                wait_for_state(self._agents[agent], 'episode_started', 'in_episode')
            except Exception as ex:  #pylint: disable=broad-except
                logger.exception("Unable to start episode for Agent {agent} in do_start_episode")
                self.fail(str(ex))

        # Loop between each step to play the game
        for step_num in range(self._steps):
            self.step_num = step_num
            logger.info(f"Running step number {self.step_num}")
            self.update_status({"step": self.step_num})

            # Gets each agent's desired actions based on current observations
            # TODO: Convert actions to an array of float types
            for agent in self._agents:
                agent_obs = {agent: self.obs[agent]}
                try:
                    logger.debug(f"[{step_num}] Getting actions for {agent} with obs {agent_obs}")
                    action = self._agents[agent].get_action(obs=agent_obs)
                    logger.info(f"[{step_num}] Got actions for {agent}: {action}")
                except Exception as ex:  #pylint: disable=broad-except
                    logger.exception("Unable to get actions from Agent {agent} in do_start_episode")
                    self.fail(str(ex))
                wait_for_state(self._agents[agent], 'get_action', 'in_episode')
                self.actions[agent] = action[agent]

            # TODO: Need to add step method to the Environment
            # TODO: And with that, deal with obs/rewards

            # Performs each agent's requested action
            # TODO: Convert step_data into four actual keyword args
            for agent in self._agents:
                logger.info(f"[{step_num}] Replaying actions for {agent} with actions {self.actions[agent]}")
                try:
                    step_data = {'prev_obs': self.obs[agent],
                                'rewards': self.rewards[agent],
                                'actions': self.actions[agent],
                                'new_obs': self.obs[agent]}
                except Exception as ex:  #pylint: disable=broad-except
                    logger.exception("Unable to get data to replay action for Agent {agent} in do_start_episode")
                    self.fail(str(ex))
                try:
                    self._agents[agent].replay_action(obs=step_data)
                    wait_for_state(self._agents[agent], 'replay_action', 'in_episode')
                except Exception as ex:  #pylint: disable=broad-except
                    logger.exception("Unable to replay action for Agent {agent} in do_start_episode")
                    self.fail(str(ex))
                wait_for_state(self._agents[agent], 'replay_action', 'in_episode')

    def do_get_status(self):
        """
        Gets the status of the currently running orchestrator
        """
        pass

    def do_stop_episode(self):
        """
        Stops all processing and releases any resources that are in use in
        preparation for being shut down.
        """
        pass

    def do_reset(self):
        # TODO: Call reset method on environment
        pass