# Lockheed Martin Copyright 2022, all rights reserved

""" The base environment which has the expected env methods pre-defined.

    Each game's and/or video game engine's orchestrator should be linked up to
    a game or environment. That game or environment's class should inherit off
    of this BaseEnv class, which defines the core APIs we expect.
"""

from typing import Any, Dict, List, Tuple, Union


class BaseEnv:
    """ This defines the core APIs we expect to create/play a game.
    """
    def __init__(self):
        self.game_env = NotImplemented

    def engine_create(self, players: int, game_kwargs: Dict[str, Any]):
        """  This creates the game/environment engine

        Args:
            players (int): Number of players this game expects [Default=1]
            game_kwargs (Dict[str, Any]): Kwargs that the engine wants
        """
        return NotImplementedError

    def step(self, actions: Dict[str, List[Union[int, float]]])\
        -> Tuple[Dict[str, List[float]], List[float], bool, Dict[str, Any]]:
        """ Steps through the game environment, acting for each agent.

        Args:
            actions: Dict of each agent's requested actions for this turn.
                Your game will dictate the specific format it needs.

        Returns:
            Dict[str, List[float]]: The observations every agent saw
            Dict[str, int]: The rewards every agent got
            bool: A bool if the game is done
            Dict[str, Any]: Metadata of each player's information & the score
        """
        return NotImplementedError

    def reset(self) -> Dict[str, List[float]]:
        """ Resets the game environment as an episode begins AND ends.

        Returns:
            Dict[str, List[float]]: Dict containing each agent's name and a
                list of each agent's observation properties (X/Y/Team)
        """
        try:
            return self.game_env.reset()
        except AttributeError as err:
            if not self.game_env or self.game_env == NotImplemented:
                msg = "The game didn't start, the real error should be above."
                raise RuntimeError(f"💩  {msg}")
            else:
                raise AttributeError(err)

    def close(self) -> bool:
        """ Closes the game environment upon completion.
        """
        try:
            return self.game_env.close()
        except AttributeError as err:
            if not self.game_env or self.game_env == NotImplemented:
                msg = "The game didn't start, the real error should be above."
                raise RuntimeError(f"💩  {msg}")
            else:
                raise AttributeError(err)
