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
import sys
import logging

from mistk_test_harness.container import Container
from mistk_test_harness import evaluator
from mistk_test_harness.test_harness import TestHarness

evaluation_types = ['BinaryClassification', 'MultilabelClassification', 'MulticlassClassification', 'Regression']

parser = argparse.ArgumentParser(description='Test harness for validating model implementations',
                                prog='python -m mistk_test_harness',
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                epilog='Examples: \n' + 
                                'python -m mistk_test_harness --train /my/dataset/folder --model-path /my/model/folder mymodel.MyImplementedModel\n' +
                                'python -m mistk_test_harness --train /my/dataset/folder --model-path /my/model/folder http://localhost:8080\n' +
                                'python -m mistk_test_harness --train /my/dataset/folder --model-path /my/model/folder repo/mymodelimpl\n' +
                                'python -m mistk_test_harness --predict /my/dataset/folder --model-path /my/model/folder --predictions-path /my/predictions/folder\n' +
                                '\t--ground-truth-path /ground/truth/folder --evaluate BinaryClassification mymodel.MyImplementedModel\n')
parser.add_argument('model', metavar='MODEL',
                    help='model module/package, service endpoint URL, or Docker image')
parser.add_argument('--train', metavar='PATH',
                    help='Train over the dataset at the local path (requires --model-path)')
parser.add_argument('--predict', metavar='PATH',
                    help='Run predictions over the dataset at the local path')
parser.add_argument('--evaluate', metavar='TYPE',
                    help='Evaluate model predictions as one of: ' + 
                    ', '.join(evaluation_types) + 
                    ' (requires --predictions-path, --ground-truth-path)')
parser.add_argument('--predictions-path', metavar='PATH',
                    help='Local folder path to save/load model predictions')
parser.add_argument('--ground-truth-path', metavar='PATH',
                    help='Local folder path containing dataset ground truth')
parser.add_argument('--model-path', metavar='PATH',
                    help='Local folder path to save/load model checkpoints')
parser.add_argument('--model-props', metavar='FILE',
                    help='Local file containing json dictionary of model properties')
parser.add_argument('--hyperparams', metavar='FILE',
                    help='Local file containing json dictionary of model hyperparameters')
parser.add_argument('--stream-predict', metavar='FILE',
                    help='Local file containing json dictionary of ids to base64 encoded input data')
parser.add_argument('--logs', action='store_true', help='Show all MISTK log output (debug)')
args = parser.parse_args()

if not args.logs:
    logging.getLogger().setLevel(logging.FATAL)

if args.train and not args.model_path:
    print('--train flag requires --model-path')
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

model = args.model
model_train_path = args.train
model_test_path = args.predict
model_predictions_path = args.predictions_path
model_save_path = args.model_path
container = None

if not args.model.startswith('http:') and re.match('[\w:-]*/[\w:-]*', args.model) is not None:
    volumes = {}
    if args.train and args.predict and args.train == args.predict:
        volumes[args.train] = {'bind': '/tmp/data', 'mode': 'rw'}
        model_train_path = '/tmp/data'
        model_test_path = '/tmp/data'
    elif args.train:
        volumes[args.train] = {'bind': '/tmp/train', 'mode': 'rw'}
        model_train_path = '/tmp/train'
    elif args.predict:
        volumes[args.predict] = {'bind': '/tmp/test', 'mode': 'rw'}
        model_test_path = '/tmp/test'

    if args.predictions_path:
        volumes[args.predictions_path] = {'bind': '/tmp/predictions', 'mode': 'rw'}
        model_predictions_path = '/tmp/predictions'
    if args.model_path:
        volumes[args.model_path] = {'bind': '/tmp/model', 'mode': 'rw'}
        model_save_path = '/tmp/model'

    print('Starting container ' + args.model)
    container = Container(args.model)
    name = container.run(volumes)
    model = 'http://localhost:8080'

harness = TestHarness()

dataset_map = {}
objectives = []
if args.train:
    dataset_map['train'] = model_train_path
    objectives.append('training')
if args.predict:
    dataset_map['test'] = model_test_path
    objectives.append('prediction')
if args.stream_predict:
    objectives.append('streaming_prediction')

if args.train or args.predict or args.stream_predict:
    harness.model_init(model, objectives, dataset_map, model_save_path, model_props, hyperparams)

    if args.train:
        harness.model_train(model_save_path)

    if args.predict:
        harness.model_predict(model_predictions_path)
        
    if args.stream_predict:
        harness.model_stream_predict(stream_input)

if args.evaluate:
    print('Evaluating predictions')
    evaluator.perform_assessment(args.evaluate, args.predictions_path, args.ground_truth_path)
    print('Evaluation completed, verify assessment output in ' + args.predictions_path)

if container:
    print('Stopping container')
    container.stop()
    
print("Validation completed")
