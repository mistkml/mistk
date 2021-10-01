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
import mistk.evaluation
from mistk.evaluation.abstract_evaluation_plugin import AbstractEvaluationPlugin

_endpoint_service = mistk.evaluation.service.EvaluationPluginEndpoint()

if len(sys.argv) <= 2:
    raise RuntimeError("Requires a module and class name as an argument")

_module = importlib.import_module(sys.argv[1])
_evaluation_plugin = getattr(_module, sys.argv[2])()
assert isinstance(_evaluation_plugin, AbstractEvaluationPlugin)
_endpoint_service.load_metrics_spec(_module)
_endpoint_service.evaluation_plugin = _evaluation_plugin
_evaluation_plugin.endpoint_service = _endpoint_service

try:
    service_port = sys.argv[3]
    _endpoint_service.start_server(port=int(service_port))
except IndexError:
    _endpoint_service.start_server() # defaults to 8080
