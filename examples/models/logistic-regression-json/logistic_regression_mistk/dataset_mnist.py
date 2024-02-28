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



from __future__ import division

import os, gzip
import numpy as np 

def load_training_data(basedir: str):
    """Loads MNIST training dataset.

    # Returns
    Tuple of Numpy arrays: `(x_train, y_train, IDs).
    """

    files = ['train-labels-idx1-ubyte.gz', 'train-images-idx3-ubyte.gz']
    paths = []
    for fname in files:
        paths.append(os.path.join(basedir, fname))
    
    # labels
    with gzip.open(paths[0], 'rb') as lbpath:
        labels = np.frombuffer(lbpath.read(), np.uint8, offset=8)    
    # image array 784
    with gzip.open(paths[1], 'rb') as imgpath:
        images = np.frombuffer(imgpath.read(), np.uint8, offset=16).reshape(len(labels), 784)
        # Convert from [0, 255] -> [0.0, 1.0].
        images = images.astype(np.float32)
        images = np.multiply(images, 1.0 / 255.0)
    # make ids for mnist
    idx=1
    row_ids = []
    for _ in labels:
        padding_size = len(str(abs(len(labels))))
        row_id = 'mnist-train-%s' % (str(idx).zfill(padding_size))
        row_ids.append(row_id)
        idx+=1
    row_ids = np.asarray(row_ids)
    
    return (images, labels, row_ids)


def load_test_data(basedir: str):
    """Loads the MNIST test dataset.

    # Returns
    Tuple of Numpy arrays: `(x_train, y_train, IDs).
    """
    
    files = ['t10k-labels-idx1-ubyte.gz', 't10k-images-idx3-ubyte.gz']
    paths = []
    for fname in files:
        paths.append(os.path.join(basedir, fname))
    
    # labels
    with gzip.open(paths[0], 'rb') as lbpath:
        labels = np.frombuffer(lbpath.read(), np.uint8, offset=8)    
    # image array 784
    with gzip.open(paths[1], 'rb') as imgpath:
        images = np.frombuffer(imgpath.read(), np.uint8, offset=16).reshape(len(labels), 784)
        # Convert from [0, 255] -> [0.0, 1.0].
        images = images.astype(np.float32)
        images = np.multiply(images, 1.0 / 255.0)
    # make ids for mnist
    idx=1
    row_ids = []
    for _ in labels:
        padding_size = len(str(abs(len(labels))))
        row_id = 'mnist-test-%s' % (str(idx).zfill(padding_size))
        row_ids.append(row_id)
        idx+=1
    row_ids = np.asarray(row_ids)
    
    return (images, labels, row_ids)