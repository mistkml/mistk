# this model uses a generic python v3 base image
FROM python:3.6

# these lines pull the MISTK base infrastructure into this model
RUN pip install mistk --no-cache-dir --extra-index-url http://pypiserver.sml.svc.sml.atl.lmco.com:8080 --trusted-host pypi.python.org --trusted-host pypiserver.sml.svc.sml.atl.lmco.com

RUN pip install numpy pandas scikit-learn scipy --trusted-host pypi.python.org

# install the python code for our Logistic Regression model
RUN mkdir -p /usr/src/models/scikit-basicmodels
COPY . /usr/src/models/scikit-basicmodels
RUN cd /usr/src/models/scikit-basicmodels && python setup.py easy_install -Z .

# these lines set up and run this model using the MISTK infrastructure
EXPOSE 8080
ENTRYPOINT ["python3"]
CMD ["-m", "mistk", "scikit_learn.logistic_regression", "ScikitLearnLogisticRegressionModel"]
