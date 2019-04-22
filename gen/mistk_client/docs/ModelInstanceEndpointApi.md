# mistk_test_harness.client.ModelInstanceEndpointApi

All URIs are relative to *http://localhost/v1/mistk*

Method | HTTP request | Description
------------- | ------------- | -------------
[**build_model**](ModelInstanceEndpointApi.md#build_model) | **POST** /buildModel | Build the model
[**get_status**](ModelInstanceEndpointApi.md#get_status) | **GET** /status | Get the status of the model
[**initialize_model**](ModelInstanceEndpointApi.md#initialize_model) | **POST** /initialize | Initialize the model
[**load_data**](ModelInstanceEndpointApi.md#load_data) | **POST** /loadData | Loads data for the model
[**pause**](ModelInstanceEndpointApi.md#pause) | **POST** /pause | Pause the model
[**predict**](ModelInstanceEndpointApi.md#predict) | **POST** /predict | Perform predictions with the model
[**reset**](ModelInstanceEndpointApi.md#reset) | **POST** /reset | Resets the model
[**resume_predict**](ModelInstanceEndpointApi.md#resume_predict) | **POST** /resumePredict | Resume predicitons on a paused model
[**resume_training**](ModelInstanceEndpointApi.md#resume_training) | **POST** /resumeTraining | Resume training on a paused model
[**save_model**](ModelInstanceEndpointApi.md#save_model) | **POST** /saveModel | Save the model snapshot
[**save_predictions**](ModelInstanceEndpointApi.md#save_predictions) | **POST** /savePredictions | Save the model&#39;s predictions
[**stream_predict**](ModelInstanceEndpointApi.md#stream_predict) | **POST** /streamPredict | Perform streaming predictions with the model
[**terminate**](ModelInstanceEndpointApi.md#terminate) | **POST** /shutdown | Shut down the model
[**train**](ModelInstanceEndpointApi.md#train) | **POST** /train | Train the model


# **build_model**
> build_model(model_path=model_path)

Build the model

Instructs the container to construct the model

### Example
```python
from __future__ import print_function
import time
import mistk_test_harness.client
from mistk_test_harness.client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = mistk_test_harness.client.ModelInstanceEndpointApi()
model_path = 'model_path_example' # str | The absolute path to the directory where the model's checkpoint/snapshot file can be found.   (optional)

try:
    # Build the model
    api_instance.build_model(model_path=model_path)
except ApiException as e:
    print("Exception when calling ModelInstanceEndpointApi->build_model: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **model_path** | **str**| The absolute path to the directory where the model&#39;s checkpoint/snapshot file can be found.   | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_status**
> ModelInstanceStatus get_status(watch=watch, resource_version=resource_version)

Get the status of the model

Retrieves the current status of the model

### Example
```python
from __future__ import print_function
import time
import mistk_test_harness.client
from mistk_test_harness.client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = mistk_test_harness.client.ModelInstanceEndpointApi()
watch = False # bool | Watch for changes to the described resources and return them as a stream of add, update, and remove notifications. Specify resourceVersion.  (optional) (default to False)
resource_version = 56 # int | When specified with a watch call, shows changes that occur after that particular version of a resource. Defaults to changes from the beginning of history.  (optional)

try:
    # Get the status of the model
    api_response = api_instance.get_status(watch=watch, resource_version=resource_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelInstanceEndpointApi->get_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **watch** | **bool**| Watch for changes to the described resources and return them as a stream of add, update, and remove notifications. Specify resourceVersion.  | [optional] [default to False]
 **resource_version** | **int**| When specified with a watch call, shows changes that occur after that particular version of a resource. Defaults to changes from the beginning of history.  | [optional] 

### Return type

[**ModelInstanceStatus**](ModelInstanceStatus.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **initialize_model**
> initialize_model(initialization_parameters)

Initialize the model

Instructs the model instance to initialize.

### Example
```python
from __future__ import print_function
import time
import mistk_test_harness.client
from mistk_test_harness.client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = mistk_test_harness.client.ModelInstanceEndpointApi()
initialization_parameters = mistk_test_harness.client.ModelInstanceInitParams() # ModelInstanceInitParams | Initialization parameters for the model including the objectives, properties, and hparams. Objectives are a list of objectives for this model instance from the following options { train, predict}. Properties are a dictionary of properties for this model instance.  Hparams are a dictionary of hyperparameters for this model instance. 

try:
    # Initialize the model
    api_instance.initialize_model(initialization_parameters)
except ApiException as e:
    print("Exception when calling ModelInstanceEndpointApi->initialize_model: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **initialization_parameters** | [**ModelInstanceInitParams**](ModelInstanceInitParams.md)| Initialization parameters for the model including the objectives, properties, and hparams. Objectives are a list of objectives for this model instance from the following options { train, predict}. Properties are a dictionary of properties for this model instance.  Hparams are a dictionary of hyperparameters for this model instance.  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **load_data**
> load_data(datasets)

Loads data for the model

Loads data onto a staging area for use by the model

### Example
```python
from __future__ import print_function
import time
import mistk_test_harness.client
from mistk_test_harness.client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = mistk_test_harness.client.ModelInstanceEndpointApi()
datasets = NULL # object | A dictionary mapping objectives to Object References of Dataset objects.  Dictionary keys must be one of the following {train, test} 

try:
    # Loads data for the model
    api_instance.load_data(datasets)
except ApiException as e:
    print("Exception when calling ModelInstanceEndpointApi->load_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **datasets** | **object**| A dictionary mapping objectives to Object References of Dataset objects.  Dictionary keys must be one of the following {train, test}  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pause**
> pause()

Pause the model

Instructs the container to pause the current training or  prediction activity 

### Example
```python
from __future__ import print_function
import time
import mistk_test_harness.client
from mistk_test_harness.client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = mistk_test_harness.client.ModelInstanceEndpointApi()

try:
    # Pause the model
    api_instance.pause()
except ApiException as e:
    print("Exception when calling ModelInstanceEndpointApi->pause: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **predict**
> predict()

Perform predictions with the model

Perform predictions with the test dataset previously loaded

### Example
```python
from __future__ import print_function
import time
import mistk_test_harness.client
from mistk_test_harness.client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = mistk_test_harness.client.ModelInstanceEndpointApi()

try:
    # Perform predictions with the model
    api_instance.predict()
except ApiException as e:
    print("Exception when calling ModelInstanceEndpointApi->predict: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **reset**
> reset()

Resets the model

Resets the model

### Example
```python
from __future__ import print_function
import time
import mistk_test_harness.client
from mistk_test_harness.client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = mistk_test_harness.client.ModelInstanceEndpointApi()

try:
    # Resets the model
    api_instance.reset()
except ApiException as e:
    print("Exception when calling ModelInstanceEndpointApi->reset: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resume_predict**
> resume_predict()

Resume predicitons on a paused model

Resumes the training activity 

### Example
```python
from __future__ import print_function
import time
import mistk_test_harness.client
from mistk_test_harness.client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = mistk_test_harness.client.ModelInstanceEndpointApi()

try:
    # Resume predicitons on a paused model
    api_instance.resume_predict()
except ApiException as e:
    print("Exception when calling ModelInstanceEndpointApi->resume_predict: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resume_training**
> resume_training()

Resume training on a paused model

Resumes the training activity 

### Example
```python
from __future__ import print_function
import time
import mistk_test_harness.client
from mistk_test_harness.client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = mistk_test_harness.client.ModelInstanceEndpointApi()

try:
    # Resume training on a paused model
    api_instance.resume_training()
except ApiException as e:
    print("Exception when calling ModelInstanceEndpointApi->resume_training: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save_model**
> save_model(model_path)

Save the model snapshot

Instructs the container to serialize the model to the specified path 

### Example
```python
from __future__ import print_function
import time
import mistk_test_harness.client
from mistk_test_harness.client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = mistk_test_harness.client.ModelInstanceEndpointApi()
model_path = 'model_path_example' # str | A path pointing to the directory where the model is to be saved. 

try:
    # Save the model snapshot
    api_instance.save_model(model_path)
except ApiException as e:
    print("Exception when calling ModelInstanceEndpointApi->save_model: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **model_path** | **str**| A path pointing to the directory where the model is to be saved.  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save_predictions**
> save_predictions(dataset)

Save the model's predictions

Instructs the container to save the predictions to the specified path 

### Example
```python
from __future__ import print_function
import time
import mistk_test_harness.client
from mistk_test_harness.client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = mistk_test_harness.client.ModelInstanceEndpointApi()
dataset = mistk_test_harness.client.MistkDataset() # MistkDataset | A dataset that contains a path pointing to the directory where the predictions are to be saved. 

try:
    # Save the model's predictions
    api_instance.save_predictions(dataset)
except ApiException as e:
    print("Exception when calling ModelInstanceEndpointApi->save_predictions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset** | [**MistkDataset**](MistkDataset.md)| A dataset that contains a path pointing to the directory where the predictions are to be saved.  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stream_predict**
> object stream_predict(data_map)

Perform streaming predictions with the model

Perform predictions with the test dataset previously loaded

### Example
```python
from __future__ import print_function
import time
import mistk_test_harness.client
from mistk_test_harness.client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = mistk_test_harness.client.ModelInstanceEndpointApi()
data_map = NULL # object | Dictionary of IDs to b64 encoded data

try:
    # Perform streaming predictions with the model
    api_response = api_instance.stream_predict(data_map)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelInstanceEndpointApi->stream_predict: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_map** | **object**| Dictionary of IDs to b64 encoded data | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **terminate**
> terminate()

Shut down the model

Shuts down the model

### Example
```python
from __future__ import print_function
import time
import mistk_test_harness.client
from mistk_test_harness.client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = mistk_test_harness.client.ModelInstanceEndpointApi()

try:
    # Shut down the model
    api_instance.terminate()
except ApiException as e:
    print("Exception when calling ModelInstanceEndpointApi->terminate: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **train**
> train()

Train the model

Trains the model with the training dataset previously loaded

### Example
```python
from __future__ import print_function
import time
import mistk_test_harness.client
from mistk_test_harness.client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = mistk_test_harness.client.ModelInstanceEndpointApi()

try:
    # Train the model
    api_instance.train()
except ApiException as e:
    print("Exception when calling ModelInstanceEndpointApi->train: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

