import csv
import logging
import pandas
import numpy as np
from  mistk.model.client import MistkDataRecord

_logger = logging.getLogger(__name__)

def csv_Predictions_to_DataFrame(csv_file):
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

def csv_Groundtruth_to_DataFrame(csv_file):
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
    return truth_df

def csv_Predictions_to_MistkDataRecord(csv_file, set_id):
    """
    Convert csv to data record list
    """
    _logger.debug('Converting csv file ' + str(csv_file) + ' to DataRecords')
    recordList = []   
    with open(csv_file) as fp:
        # Check if the file has a header line, skip if necessary
        has_header = csv.Sniffer().has_header(fp.read(2048)) # Size of buffer for header
        fp.seek(0)  # Rewind.
        reader = csv.reader(fp)
        header = None
        # header
        if has_header:
            header = next(reader)
            indices = {}
            id_index = None
            label_index = None
            bounds_index = None
            # check for defined headers
            for col in header:
                if col == 'id':
                    id_index = header.index('id')
                elif col == 'recordId':
                    id_index = header.index('recordId')
                elif col == 'label':
                    label_index = header.index('label')
                elif col == 'labels':
                    label_index = header.index('labels')
                elif col == 'bounds':
                    bounds_index = header.index('bounds')
                else:
                    indices[col] = [i for i, x in enumerate(header) if x == col]       
            
            # check indices exist
            if id_index is None:
                err = "CSV header does not contain 'id' or 'recordId' column for label id in file: " + str(csv_file)
                _logger.debug(err)
                raise Exception(err)
            if label_index is None:
                err = "CSV header does not contain 'label' or 'labels' column for labels in file: " + str(csv)
                _logger.debug(err)
                raise Exception(err)
            
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
                        label_dict[column] = val.split(' ')[i] 
                    # bounds are special due to 4 values per bounding box
                    if bounds_index:
                        bounds = _split_bounds(data[bounds_index].strip())
                        label_dict['bounds'] = bounds[i]                     
                    record_data.append(label_dict)   
                    i += 1
                record = MistkDataRecord(record_id=recordId, referenced_set_id=set_id, values=record_data)
                recordList.append(record)  
        # no header
        else:
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
                record = MistkDataRecord(record_id=recordId, referenced_set_id=set_id, values=record_data)
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
