import csv
import json
import logging
import pandas
import numpy as np
from typing import List
from  mistk.data import MistkDataRecord, MistkDataRecordList
from mistk.data.utils import deserialize_model

_logger = logging.getLogger(__name__)

def csv_predictions_to_dataframe(csv_file):
    logging.info("Reading predictions from " + csv_file)
    results_csv = []
    possible_cols = ['rowid', 'labels', 'confidence', 'bounds']
    with open(csv_file) as fp:
        # Check if the file has a header line, skip if necessary
        has_header = csv.Sniffer().has_header(fp.read(2048))
        fp.seek(0)  # Rewind.
        reader = csv.reader(fp)
        # ignore header for now
        if has_header:
            next(reader)
        for data in reader:
            results_csv.append(data)        
    results_df = pandas.DataFrame(results_csv)
    # rename columns
    for i, _ in enumerate(results_df.columns.values):
        if i < len(possible_cols):
            results_df.rename(columns = {i : possible_cols[i]}, inplace = True)
    # create columns if they do not exist
    for nancol in possible_cols[len(results_df.columns):len(possible_cols)]:
        results_df[nancol] = np.nan
    results_df = results_df.replace(r'^\s*$', np.nan, regex=True)
    return results_df

def csv_groundtruth_to_dataframe(csv_file):
    logging.info("Reading ground truth from " + csv_file)
    truth_csv = []
    possible_cols = ['rowid', 'labels', 'bounds']
    with open(csv_file) as fp:
        # Check if the file has a header line, skip if necessary
        has_header = csv.Sniffer().has_header(fp.read(2048))
        fp.seek(0)  # Rewind.
        reader = csv.reader(fp)
        # ignore header for now
        if has_header:
            next(reader)
        for data in reader:
            truth_csv.append(data) 
    truth_df = pandas.DataFrame(truth_csv)
    # rename columns
    for i, _ in enumerate(truth_df.columns.values):
        if i < len(possible_cols):
            truth_df.rename(columns = {i : possible_cols[i]}, inplace = True)
    # create columns if they do not exist
    for nancol in possible_cols[len(truth_df.columns):len(possible_cols)]:
        truth_df[nancol] = np.nan
    truth_df = truth_df.replace(r'^\s*$', np.nan, regex=True)
    return truth_df

def csv_has_header(csv_file):
    """
        Check if CSV file has a header
        
        :param csv_file: The csv file to check header for
    """
    has_header = False
    with open(csv_file) as fp:
        # Check if the file has a header line, skip if necessary
        has_header = csv.Sniffer().has_header(fp.read(2048))
    return has_header
    

def json_predictions_to_dataframe(json_file: str)  -> pandas.DataFrame:
    """
        Parse a json file that represents a data record list into a predictions data frame equivalent
        
        :param json_file: The json file to parse the data record list into a data frame
    """
    logging.info("Reading predictions from " + json_file)
    results_json = []
    possible_cols = ['rowid', 'labels', 'confidence', 'bounds']
    cols = ['rowid']
    with open(json_file, 'r') as f:
        data = json.load(f)
        m = deserialize_model(data, MistkDataRecordList)
        for record in m.items:
            row = []
            row.append(record.record_id)
            for value in record.values:
                i = 1
                for key, val in value.items():
                    if key == 'label':
                        key = 'labels'
                    if key not in cols:
                        cols.append(key)
                    if i >= len(row):
                        row.append(val)
                    else:
                        row[i] = f'{row[i]} {val}'
                    i += 1
            results_json.append(row)
                   
    results_df = pandas.DataFrame(results_json, columns=cols)
    
    # create columns if they do not exist
    for possible_col in possible_cols:
        if possible_col not in results_df.columns:
            results_df[possible_col] = np.nan
    results_df = results_df.replace(r'^\s*$', np.nan, regex=True)
    return results_df

def json_groundtruth_to_dataframe(json_file: str) -> pandas.DataFrame:
    """
        Parse a json file that represents a data record list into a ground truth data frame equivalent
        
        :param json_file: The json file to parse the data record list into a data frame
        
        :return Dataframe equivalent
    """
    logging.info("Reading predictions from " + json_file)
    results_json = []
    possible_cols = ['rowid', 'labels', 'bounds']
    cols = ['rowid']
    with open(json_file, 'r') as f:
        data = json.load(f)
        m = deserialize_model(data, MistkDataRecordList)
        for item in m.items:
            row = []
            row.append(item.record_id)
            for value in item.values:
                i = 1
                for key, val in value.items():
                    if key == 'label':
                        key = 'labels'
                    if key not in cols:
                        cols.append(key)
                    if i >= len(row):
                        row.append(val)
                    else:
                        row[i] = f'{row[i]} {val}'
                    i += 1
            results_json.append(row)
                   
    results_df = pandas.DataFrame(results_json, columns=cols)
    
    # create columns if they do not exist
    for possible_col in possible_cols:
        if possible_col not in results_df.columns:
            results_df[possible_col] = np.nan
    results_df = results_df.replace(r'^\s*$', np.nan, regex=True)
    return results_df
    

def csv_predictions_to_mistk_data_records(csv_file: str) -> List[MistkDataRecord]:
    """
    Convert predictions csv to MISTK data record list
    """
    _logger.debug('Converting predictions csv file ' + str(csv_file) + ' to DataRecords')
    recordList = []   
    with open(csv_file) as fp:
        # Check if the file has a header line, skip if necessary
        has_header = csv.Sniffer().has_header(fp.read(10240)) # Size of buffer for header
        fp.seek(0)  # Rewind.
        reader = csv.reader(fp)
        header = None
        
        # check header
        if has_header:
            header = next(reader)
            _logger.debug("Checking header: %s" % str(header))
            indices = {}
            id_index = None
            label_index = None
            bounds_index = None
            # check for defined headers
            for col in header:
                col_strip = col.strip()
                if col_strip == 'id':
                    id_index = header.index(col)
                elif col_strip == 'recordId':
                    id_index = header.index(col)
                elif col_strip == 'label':
                    label_index = header.index(col)
                elif col_strip == 'labels':
                    label_index = header.index(col)
                elif col_strip == 'bounds':
                    bounds_index = header.index(col)
                elif col_strip == 'bounding_box':
                    bounds_index = header.index(col)
                else:
                    indices[col_strip] = [i for i, x in enumerate(header) if x == col]       
            
            # check indices exist
            if id_index is None:
                err = "CSV header does not contain 'id' or 'recordId' column for label id in file: " + str(csv_file)
                _logger.debug(err)
                fp.seek(0)  # Rewind since no header
                has_header = False
            if label_index is None:
                err = "CSV header does not contain 'label' or 'labels' column for labels in file: " + str(csv_file)
                _logger.debug(err)
                fp.seek(0)  # Rewind since no header
                has_header = False         
        
        # header
        if has_header:
            _logger.debug("Processing csv: %s" % str(header)) 
            # pull data
            for data in reader:
                if not len(data) > 0:
                    continue
                recordId = data[id_index].strip()
                record_data = []
                labels = data[label_index].strip()
                i = 0 
                # labeled data may have more than one label per recordId
                for label in labels.split(' '):
                    label_dict={}
                    label_dict['label'] = label
                    # append data related to each label
                    for column, inds in indices.items(): 
                        val = data[inds[0]].strip()
                        if val:
                            label_dict[column] = val.split(' ')[i] 
                    # bounds are special due to 4 values per bounding box
                    if bounds_index:
                        bounds = _split_bounds(data[bounds_index].strip())
                        label_dict['bounds'] = bounds[i]                     
                    record_data.append(label_dict)   
                    i += 1
                record = MistkDataRecord(record_id=recordId, values=record_data)
                recordList.append(record)  
        # no header
        else:
            _logger.debug("No header found")
            for data in reader:
                recordId = data[0].strip()
                record_data = []
                labels = data[1].strip()
                confs = None
                bounds = None
                if len(data) > 2:
                    confs = data[2].strip()
                if len(data) > 3:
                    bounds = data[3].strip()
                i = 0
                for label in labels.split(' '):
                    label_dict={}
                    label_dict['label'] = label
                    if confs:
                        label_dict['confidence'] = confs.split(' ')[i]   
                    if bounds:
                        label_dict['bounds'] = _split_bounds(bounds)[i]
                    record_data.append(label_dict)    
                    i += 1  
                record = MistkDataRecord(record_id=recordId, values=record_data)
                recordList.append(record)
    return recordList


def csv_groundtruth_to_mistk_data_records(csv_file: str) -> List[MistkDataRecord]:
    """
    Convert ground truth csv to MISTK data record list
    """
    _logger.debug('Converting ground truth csv file ' + str(csv_file) + ' to DataRecords')
    recordList = []   
    with open(csv_file) as fp:
        # Check if the file has a header line, skip if necessary
        has_header = csv.Sniffer().has_header(fp.read(10240)) # Size of buffer for header
        fp.seek(0)  # Rewind.
        reader = csv.reader(fp)
        header = None
        
        # check header
        if has_header:
            header = next(reader)
            _logger.debug("Checking header: %s" % str(header))
            indices = {}
            id_index = None
            label_index = None
            bounds_index = None
            # check for defined headers
            for col in header:
                col_strip = col.strip()
                if col_strip == 'id':
                    id_index = header.index(col)
                elif col_strip == 'recordId':
                    id_index = header.index(col)
                elif col_strip == 'label':
                    label_index = header.index(col)
                elif col_strip == 'labels':
                    label_index = header.index(col)
                elif col_strip == 'bounds':
                    bounds_index = header.index(col)
                elif col_strip == 'bounding_box':
                    bounds_index = header.index(col)
                else:
                    indices[col_strip] = [i for i, x in enumerate(header) if x == col]       
            
            # check indices exist
            if id_index is None:
                err = "CSV header does not contain 'id' or 'recordId' column for label id in file: " + str(csv_file)
                _logger.debug(err)
                fp.seek(0)  # Rewind since no header
                has_header = False
            if label_index is None:
                err = "CSV header does not contain 'label' or 'labels' column for labels in file: " + str(csv_file)
                _logger.debug(err)
                fp.seek(0)  # Rewind since no header
                has_header = False   
        
        # header
        if has_header:
            
            # pull data
            for data in reader:
                if not len(data) > 0:
                    continue
                recordId = data[id_index].strip()
                record_data = []
                labels = data[label_index].strip()
                i = 0 
                # labeled data may have more than one label per recordId
                for label in labels.split(' '):
                    label_dict={}
                    label_dict['label'] = label
                    # append data related to each label
                    for column, inds in indices.items(): 
                        val = data[inds[0]].strip()
                        if val:
                            label_dict[column] = val.split(' ')[i] 
                    # bounds are special due to 4 values per bounding box
                    if bounds_index:
                        bounds = _split_bounds(data[bounds_index].strip())
                        label_dict['bounds'] = bounds[i]                     
                    record_data.append(label_dict)   
                    i += 1
                record = MistkDataRecord(record_id=recordId, values=record_data)
                recordList.append(record)  
        # no header
        else:
            _logger.debug("No header found")
            for data in reader:
                recordId = data[0].strip()
                record_data = []
                labels = data[1].strip()
                bounds = None
                if len(data) > 2:
                    bounds = data[2].strip()
                i = 0
                for label in labels.split(' '):
                    label_dict={}
                    label_dict['label'] = label  
                    if bounds:
                        label_dict['bounds'] = _split_bounds(bounds)[i]
                    record_data.append(label_dict)    
                    i += 1  
                record = MistkDataRecord(record_id=recordId, values=record_data)
                recordList.append(record)
    return recordList

def _split_bounds(bounds):
    bounding_boxes = []
    bounds_split = bounds.split(' ')
    for index in range(0, len(bounds_split), 4):
            bounding_box = [bounds_split[index], bounds_split[index+1], bounds_split[index+2], bounds_split[index+3]]
            bounding_boxes.append(bounding_box)
    return bounding_boxes

def _split(val):
    svals = val.split(' ')
    # use split values
    if (len(svals) > 1):
        return svals
    # not delimited by a space
    else:
        return val   
    

