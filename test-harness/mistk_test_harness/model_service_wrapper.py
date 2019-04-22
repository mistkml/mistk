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

from mistk_test_harness.client import ApiClient, Configuration
from mistk_test_harness.client import ModelInstanceEndpointApi

class ModelServiceWrapper(object):

    def __init__(self, model_url):
        mi_api_cfg = Configuration()
        mi_api_cfg.host = model_url
        mie_api = ApiClient(configuration=mi_api_cfg)
        self._mi_api = ModelInstanceEndpointApi(mie_api)

    def initialize_model(self, initialization_parameters):
        self._mi_api.initialize_model(initialization_parameters=initialization_parameters)

    def load_data(self, datasets=None):
        self._mi_api.load_data(datasets=datasets)

    def build_model(self, model_path=None):
        self._mi_api.build_model(model_path=model_path)

    def train(self):
        self._mi_api.train()

    def save_model(self, model_path):
        self._mi_api.save_model(model_path=model_path)

    def pause(self):
        self._mi_api.pause()

    def resume_training(self):
        self._mi_api.resume_training()

    def resume_predict(self):
        self._mi_api.resume_predict()

    def predict(self):
        self._mi_api.predict()
        
    def stream_predict(self, data_map):
        return self._mi_api.stream_predict(data_map=data_map)

    def save_predictions(self, dataset):
        self._mi_api.save_predictions(dataset=dataset)
    
    def get_status(self):
        return self._mi_api.get_status()
    
    def terminate(self):
        self._mi_api.terminate()
