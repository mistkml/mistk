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

from mistk.model.client import ApiClient, Configuration, ModelInstanceEndpointApi
from mistk.data import ModelInstanceInitParams

class ModelServiceWrapper(object):
    """
    A wrapper class for interacting with the ModelInstanceEndpointApi
    """
    
    def __init__(self, model_url):
        """
        Initializes this class and creates the client connection to the 
        AbstractModel implementation via the ModelInstanceEndpointApi
        
        :param model_url: The URL at which the AbstractModel instance is running
        """
        mi_api_cfg = Configuration()
        mi_api_cfg.host = model_url
        mie_api = ApiClient(configuration=mi_api_cfg)
        self._mi_api = ModelInstanceEndpointApi(mie_api)

    def initialize_model(self, initialization_parameters: ModelInstanceInitParams):
        """
        Executes the model instance's initialize_model method with the parameters provided
        
        :param initialization_parameters: An instance of the ModelInstanceInitParams
            which includes the objectives, model hyperparameters, and
            model properties
        """
        self._mi_api.initialize_model(initialization_parameters=initialization_parameters)

    def load_data(self, datasets=None):
        """
        Executes the model instance's load_data method with the input provided
        
        :param datasets: A dictionary mapping objectives (train, test) to MistkDataset objects
        """
        self._mi_api.load_data(datasets=datasets)

    def build_model(self, model_path=None):
        """
        Executes the model instance's build_model method with the input provided
        
        :param model_path: The directory path to where the model's snapshot file can
            be loaded
        """
        self._mi_api.build_model(model_path=model_path)

    def train(self):
        """
        Executes the model instance's train method
        """
        self._mi_api.train()

    def save_model(self, model_path):
        """
        Executes the model instance's save_model method
        
        :param model_path: The path to which the model checkpoint should be saved.
        """
        self._mi_api.save_model(model_path=model_path)

    def pause(self):
        """
        Executes the model instance's pause method
        """
        self._mi_api.pause()

    def resume_training(self):
        """
        Executes the model instance's resume_training method
        """
        self._mi_api.resume_training()

    def resume_predict(self):
        """
        Executes the model instance's resume_predict method
        """
        self._mi_api.resume_predict()

    def predict(self):
        """
        Executes the model instance's predict method
        """
        self._mi_api.predict()
        
    def stream_predict(self, data_map):
        """
        Executes the model instance's stream_predict method
        
        :param data_map: A dictionary mapping file names/ids to their
            base64 encoded data
        """
        return self._mi_api.stream_predict(data_map=data_map)
    
    def update_stream_properties(self, props):
        """
        Executes the model instance's update_stream_properties method

        :param props: A dictionary of metadata properties to be used by the model
        """
        self._mi_api.update_stream_properties(props=props)

    def save_predictions(self, data_path):
        """
        Executes the model instance's save_predictions method
        
        :param data_path: The directory path in which to save the predictions file
        """
        self._mi_api.save_predictions(data_path=data_path)
        
    def generate(self):
        """
        Executes the model instance's generate method
        """
        self._mi_api.generate()
        
    def save_generations(self, data_path):
        """
        Executes the model instance's save_generations method
        
        :param data_path: The directory path in which to save the generations created by the model
        """
        self._mi_api.save_generations(data_path=data_path)
    
    def get_status(self):
        """
        Executes the model instance's get_status method
        """
        return self._mi_api.get_status()
    
    def terminate(self):
        """
        Initiates shutdown procedures for the model instance 
        """
        self._mi_api.terminate()
