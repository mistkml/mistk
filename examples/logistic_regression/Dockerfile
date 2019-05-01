# this model uses a generic python v3 base image
FROM python:3.6

# Install the MISTK Python library from github
RUN pip install git+https://github.com/mistkml/mistk#egg=mistk --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org

# Install necessary third part libraries for logistic regression model
RUN pip install numpy pandas scikit-learn scipy --trusted-host pypi.python.org

# install the python code for our Logistic Regression model
RUN mkdir -p /usr/src/models/scikit-basicmodels
COPY . /usr/src/models/scikit-basicmodels
RUN cd /usr/src/models/scikit-basicmodels && python setup.py easy_install -Z .

# these lines set up and run this model using the MISTK infrastructure
EXPOSE 8080
ENTRYPOINT ["python3"]
CMD ["-m", "mistk", "scikit_learn.logistic_regression", "ScikitLearnLogisticRegressionModel"]
