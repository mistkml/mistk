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

In order to develop algorithms to be integrated into MISTK, the
MISTK Core Library (and its dependencies) must be available on
PYTHONPATH.

You can download them down from the MISTK Github Repository [Releases Page](https://github.com/mistkml/mistk/releases)
and install the wheel files `pip` with::

    pip install mistk-*-py3-none-any.whl

Verify that mistk is now installed on PYTHON PATH by running::

    >>> import mistk

See full [MISTK Documentation](https://mistkml.github.io/) for detailed installation instructions and to get started with the toolkit.
