# Model Integration Software ToolKit (MISTK) SDK
 
MISTK is an ecosystem for integrating, validating, and evaluating machine learning models and algorithms. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

It is expected to that the following software is installed on the system when building the MISTK toolkit:

```
Python 3.6
Pip
Docker
```

### Installing

To build a python wheel file from source, run the following command:

```
make clean dist
```

To install that wheel file for your local user, run the following command:

```
make install
```

## Example models

Logistic Regression 

### Building the logistic regression model

To build the logistic regression model, run the following command from within the 'examples/logistic_regression' directory:

```
make dist
```

To build the docker image for the logistic regression model, run the following command from within the 'examples/logistic_regression' directory:

```
make docker-image
```