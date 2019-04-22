# Dataset

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**object_info** | [**ObjectInfo**](ObjectInfo.md) |  | 
**datastash_id** | **str** | The id of the datastash associated with this dataset where all of its files will be stored.  | [optional] 
**datastash_sub_dir** | **str** | This field denotes the sub path within the datastash where this dataset&#39;s data resides.  | [optional] 
**modality** | **str** | The type of the data, one of image, audio, video, text.  This does not specify the format of the data.  | [optional] 
**format** | **str** | A string representing the name of the format of the dataset. This should be sufficient to ensure that models and transforms  are able to read and parse the data.  | [optional] 
**statistics** | [**DatasetStatistics**](DatasetStatistics.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


