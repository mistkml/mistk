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

import argparse
import json
import re
import sys, os
import logging

from mistk_test_harness.container import Container
from mistk_test_harness import evaluator
from mistk_test_harness.test_harness import TestHarness

evaluation_types = ['BinaryClassification', 'MultilabelClassification', 'MulticlassClassification', 'Regression']

parser = argparse.ArgumentParser(description='Test harness for validating model implementations',
                                prog='python -m mistk_test_harness',
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                epilog='Examples: \n' + 
                                'python -m mistk_test_harness --train /my/dataset/folder --model-path /my/model/folder --model-save-path /my/trained/model/folder --model mymodel.MyImplementedModel\n' +
                                'python -m mistk_test_harness --train /my/dataset/folder --model-path /my/model/folder --model-save-path /my/trained/model/folder --model http://localhost:8080\n' +
                                'python -m mistk_test_harness --train /my/dataset/folder --model-path /my/model/folder --model-save-path /my/trained/model/folder --model repo/mymodelimpl\n' +
                                'python -m mistk_test_harness --predict /my/dataset/folder --model-path /my/model/folder --predictions-path /my/predictions/folder\n' +
                                '\t--ground-truth-path /ground/truth/folder --evaluate BinaryClassification --model mymodel.MyImplementedModel\n' +
                                'python -m mistk_test_harness --predictions-path /my/predictions/folder --ground-truth-path /ground/truth/folder --evaluate BinaryClassification\n\n' +
                                'python -m mistk_test_harness --transform-output-path /tmp/ --transform-input-paths /my/input/folder/1 /my/input/folder/2 ... /my/input/folder/n\n' +
                                '\t--transform-properties /my/properties/file --transform mytransform.MyTransformImplementation\n' +
                                'python -m mistk_test_harness --transform-output-path /tmp/ --transform-input-paths /my/input/folder --transform http://localhost:8080\n'+
                                'python -m mistk_test_harness --transform-output-path /tmp/ --transform-input-paths /my/input/folder --transform repo/mytransformimpl'
                                )
parser.add_argument('--model', metavar='MODEL',
                    help='Model module/package, service endpoint URL, or Docker image')
parser.add_argument('--train', metavar='PATH',
                    help='Train over the dataset at the local path')
parser.add_argument('--transfer-learning', action='store_true',
                    help='Flag indicating that the training operation will be performing transfer learning')
parser.add_argument('--predict', metavar='PATH',
                    help='Run predictions over the dataset at the local path')
parser.add_argument('--evaluate', metavar='TYPE',
                    help='Evaluate model predictions as one of: ' + 
                    ', '.join(evaluation_types) + 
                    ' (requires --predictions-path, --ground-truth-path)')
parser.add_argument('--predictions-path', metavar='PATH',
                    help='Local folder path to save/load model predictions, used with the --predict and --evaluate options')
parser.add_argument('--ground-truth-path', metavar='PATH',
                    help='Local folder path containing dataset ground truth, used with the --evaluate option')
parser.add_argument('--model-path', metavar='PATH',
                    help='Local folder path to load model checkpoints, used with the --train or --predict options')
parser.add_argument('--model-save-path', metavar='PATH',
                    help='Local folder path to save model checkpoints, used with the --train option')
parser.add_argument('--model-props', metavar='FILE',
                    help='Local file containing json dictionary of model properties')
parser.add_argument('--hyperparams', metavar='FILE',
                    help='Local file containing json dictionary of model hyperparameters')
parser.add_argument('--stream-predict', metavar='FILE',
                    help='Local file containing json dictionary of ids to base64 encoded input data')
parser.add_argument('--transform', metavar='TRANSFORM',
                    help='Transform module/package, service endpoint URL, or Docker image')
parser.add_argument('--transform-output-path', metavar='PATH',
                    help='Local folder path to save results of transformation')
parser.add_argument('--transform-input-paths', metavar='PATH', nargs='+',
                    help='One or more local folder paths to be used as input directories when performing a transformation')
parser.add_argument('--transform-properties', metavar='FILE',
                    help='Local file containing json dictionary of transform properties')
parser.add_argument('--disable-container-shutdown', action='store_true', help='Disables automatic shutdown of the model or transform docker container')
parser.add_argument('--logs', action='store_true', help='Show all MISTK log output (debug)')

args = parser.parse_args()

if not args.logs:
    logging.getLogger().setLevel(logging.FATAL)

if args.model and args.transform:
    print('Cannot perform model and transform operations at the same time')

if args.train and not args.model:
    print('--train flag requires --model')
    sys.exit()

if args.predict and not args.model:
    print('--predict flag requires --model')
    sys.exit()    

if args.evaluate:
    if args.evaluate not in evaluation_types:
        print('--evaluate TYPE must be one of: ' + ', '.join(evaluation_types))
        sys.exit()
    if not args.predictions_path or not args.ground_truth_path:
        print('--evaluate flag requires --predictions-path and --ground-truth-path')
        sys.exit()

if args.model_props:
    with open(args.model_props) as file:
        model_props = json.load(file)
else:
    model_props = None
    
if args.hyperparams:
    with open(args.hyperparams) as file:
        hyperparams = json.load(file)
else:
    hyperparams = None
    
if args.stream_predict:
    with open(args.stream_predict) as file:
        stream_input = json.load(file)

if args.transform_properties:
    with open(args.transform_properties) as file:
        transform_properties = json.load(file)
else:
    transform_properties = None
        
dataset_map = {}
objectives = []

# Set up the test harness for models
model_container = None        
if args.model:
    model = args.model
    model_train_path = os.path.abspath(args.train) if args.train else None
    model_test_path = os.path.abspath(args.predict) if args.predict else None
    model_predictions_path = os.path.abspath(args.predictions_path) if args.predictions_path else None
    model_path = os.path.abspath(args.model_path) if args.model_path else None
    model_save_path = os.path.abspath(args.model_save_path) if args.model_save_path else None
    
    # Build the docker model_container for the model
    if not args.model.startswith('http:') and re.match('[\w:-]*/[\w:-]*', args.model) is not None:
        volumes = {}
        if model_train_path and model_test_path and model_train_path == model_test_path:
            volumes[model_train_path] = {'bind': '/tmp/data', 'mode': 'ro'}
            model_train_path = '/tmp/data'
            model_test_path = '/tmp/data'
        elif model_train_path:
            volumes[model_train_path] = {'bind': '/tmp/train', 'mode': 'ro'}
            model_train_path = '/tmp/train'
        elif model_test_path:
            volumes[model_test_path] = {'bind': '/tmp/test', 'mode': 'ro'}
            model_test_path = '/tmp/test'
    
        if model_predictions_path:
            volumes[model_predictions_path] = {'bind': '/tmp/predictions', 'mode': 'rw'}
            model_predictions_path = '/tmp/predictions'
        if model_save_path:
            volumes[model_save_path] = {'bind': '/tmp/model', 'mode': 'rw'}
            model_save_path = '/tmp/model'
        if model_path:
            volumes[model_path] = {'bind': '/tmp/checkpoint', 'mode': 'ro'}
            model_path = '/tmp/checkpoint'
                
        print('Starting model_container ' + args.model)
        model_container = Container(args.model)
        name = model_container.run(volumes)
        model = 'http://localhost:8080'

    if model_train_path:
        dataset_map['train'] = model_train_path
        objectives.append('training')
        if args.transfer_learning:
            objectives.append('transfer_learning')
    if args.predict:
        dataset_map['test'] = model_test_path
        objectives.append('prediction')
    if args.stream_predict:
        objectives.append('streaming_prediction')
        
        
# Set up the test harness for transforms        
transform_container = None
if args.transform:
    transform = args.transform
    transform_output_path = os.path.abspath(args.transform_output_path)
    transform_input_paths = []
    for input_dir in args.transform_input_paths:
        if not os.path.exists(os.path.abspath(input_dir)):
            print('Invalid input directory %s, exiting' % os.path.abspath(input_dir))
            sys.exit()
        transform_input_paths.append(os.path.abspath(input_dir))
        
    if not transform_input_paths or transform_input_paths == []:
        print('No input directory paths were provided for transform, exiting')        
        sys.exit()
        
    if not transform_output_path:
        print('No output directory path was provided for transform, exiting')
        sys.exit()
        
        
    if not os.path.exists(transform_output_path):
        os.makedirs(transform_output_path)
    
    # Build the docker transform_container for the model
    if not args.transform.startswith('http:') and re.match('[\w:-]*/[\w:-]*', args.transform) is not None:
        volumes = {}
        # Configure the input directories  
        input_dirs = []
        for dir_path in transform_input_paths:
            base_name = os.path.basename(os.path.normpath(dir_path))
            volumes[dir_path] = {'bind': '/tmp/input/%s' % base_name, 'mode': 'r'}
            input_dirs.append('/tmp/input/%s' % base_name)
        transform_input_paths = input_dirs
        # Configure the output directories
        volumes[transform_output_path] = {'bind': '/tmp/output', 'mode': 'rw'}
        transform_output_path = '/tmp/output'
        
        print('Starting transform_container ' + args.transform)
        transform_container = Container(args.transform)
        name = transform_container.run(volumes)
        transform = 'http://localhost:8080'

harness = TestHarness()
    

try:
    if args.train or args.predict or args.stream_predict:
        harness.model_init(model, objectives, dataset_map, model_path, model_props, hyperparams)
    
        if args.train:
            harness.model_train(model_save_path)
    
        if args.predict:
            harness.model_predict(model_predictions_path)
            
        if args.stream_predict:
            harness.model_stream_predict(stream_input)
    
    if args.evaluate:
        print('Evaluating predictions')
        evaluator.perform_assessment(args.evaluate, os.path.abspath(args.predictions_path), os.path.abspath(args.ground_truth_path))
        print('Evaluation completed, verify assessment output in ' + os.path.abspath(args.predictions_path))

    if args.transform:
        print('Performing data transformation')
        harness.transform(transform, transform_input_paths, transform_output_path, transform_properties)
        print('Data transformation is complete, output data can be found at %s' % args.transform_output_path)

    print("Validation completed")
except Exception as ex:
    print('Received the following exception: %s' % ex)

    # Save the container logs to a file
    if model_container:
        output_file = model_container.save_logs(os.getenv('MISTK_LOG_DIR', '/tmp'))
        print('Model container logs are available at %s' % output_file)
    if transform_container:
        output_file = transform_container.save_logs(os.getenv('MISTK_LOG_DIR', '/tmp'))
        print('Transform  container logs are available at %s' % output_file)
finally:
    if not args.disable_container_shutdown and model_container:
        print('Stopping model_container')
        model_container.stop()
        print('Container stopped')
        
    if not args.disable_container_shutdown and transform_container:
        print('Stopping transform_container')   
        transform_container.stop()
        print('Container stopped')
