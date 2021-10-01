import os, gzip, glob
import logging
import numpy as np
from mistk.transform.abstract_transform_plugin import AbstractTransformPlugin

class ground_truth_transform(AbstractTransformPlugin):
    
    def __init__(self):
        super().__init__()
    
    def do_terminate(self):
        AbstractTransformPlugin.do_terminate(self)
    
    def do_transform(self, inputDirs, outputDir, properties):
        input_path=inputDirs[0].data_path
        self.ground_truth_transform(input_path, outputDir.data_path)

    def ground_truth_transform(self, inputPath, outputPath): 
        try:
            #mnist = input_data.read_data_sets(inputPath, one_hot=True)
            
            _, mnist_train_labels = load_data(inputPath, is_training=True)
            _, mnist_test_labels = load_data(inputPath, is_training=False)
            
            output_file = os.path.join(outputPath, 'ground_truth.csv')
            
            with open(output_file, 'w') as writer:
                
                # Write the header
                header = 'id, label\n'
                writer.write(header)
                
                # Process the training data
                padding_size = len(str(abs(len(mnist_train_labels))))                        
                
                for idx in range(len(mnist_train_labels)):
                    label = mnist_train_labels[idx]
                    row_id = 'mnist-train-%s' % (str(idx+1).zfill(padding_size))
                    line = '%s, %s\n' % (row_id, label)                
                    writer.write(line)
                    #idx+=1
                 
                # Process the test data
                padding_size = len(str(abs(len(mnist_test_labels))))                        
                for idx in range(len(mnist_test_labels)):
                    label = mnist_test_labels[idx]
                    row_id = 'mnist-test-%s' % (str(idx+1).zfill(padding_size))
                    line = '%s, %s\n' % (row_id, label)                
                    writer.write(line)                    
                    
        except Exception as ex:
            msg = "Unexpected error caught during transform"
            logging.exception(msg)
            raise ex


def load_data(basedir: str, is_training: bool):
    """Loads the Fashion-MNIST dataset.

    # Returns
    Tuple of Numpy arrays: `(x_train, y_train).
    """
    if is_training:
        files = ['train-labels-idx1-ubyte.gz', 'train-images-idx3-ubyte.gz']
    else:
        files = ['t*k-labels-idx1-ubyte.gz', 't*k-images-idx3-ubyte.gz']
    
    logging.debug("Loading files from %s" % basedir)
    paths = []
    for fname in files:
        flist = glob.glob(os.path.join(basedir, fname))
        for f in flist:
            paths.append(f)
            logging.debug("Added file %s to load path" % f)
    
    with gzip.open(paths[0], 'rb') as lbpath:
        y = np.frombuffer(lbpath.read(), np.uint8, offset=8)
    
    with gzip.open(paths[1], 'rb') as imgpath:
        x = np.frombuffer(imgpath.read(), np.uint8, offset=16).reshape(len(y), 28, 28)
        
    return (x, y)