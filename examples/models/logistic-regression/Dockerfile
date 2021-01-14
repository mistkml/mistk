# this model uses a generic python v3 base image
FROM python:3.6

RUN mkdir -p /usr/src/models/mnist-logistic-regression
COPY requirements.txt /usr/src/models/mnist-logistic-regression
RUN pip3 install --no-cache-dir -r /usr/src/models/mnist-logistic-regression/requirements.txt --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org

# Add the built MISTK wheel file 
ADD mistk*.whl /tmp/

# Install it via pip
RUN pip install /tmp/mistk*.whl --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org


# install the python code for our Logistic Regression model

COPY . /usr/src/models/mnist-logistic-regression
RUN cd /usr/src/models/mnist-logistic-regression && python setup.py easy_install -Z .

# these lines set up and run this model using the MISTK infrastructure
EXPOSE 8080
ENTRYPOINT ["python3"]
CMD ["-m", "mistk", "logistic_regression_mistk.logistic_regression", "ScikitLearnLogisticRegressionModel"]
