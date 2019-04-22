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

import sys
import importlib
import mistk.service
from mistk.abstract_model import AbstractModel

_endpoint_service = mistk.service.ModelInstanceEndpoint()

if len(sys.argv) <= 2:
    raise RuntimeError("Requires a module and class name as an argument")

_module = importlib.import_module(sys.argv[1])
_model = getattr(_module, sys.argv[2])()
assert isinstance(_model, AbstractModel)

_endpoint_service.model = _model
_model.endpoint_service = _endpoint_service

_endpoint_service.start_server()
