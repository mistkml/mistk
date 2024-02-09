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


import numpy as np
from typing import List

class RandomInt():
    def __init__(self, low: int = 0, high: int = 2, size: int = 1):
        self.low = low
        self.high = high
        self.size = size

    def get_action(self, obs: list) -> List[int]:
        rng = np.random.default_rng()
        rng_ints = rng.integers(low=self.low, high=self.high, size=self.size)
        return [int(x) for x in rng_ints]
