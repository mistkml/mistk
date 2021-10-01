FROM python:3.6

# Install Dependencies
RUN mkdir -p /usr/src/evaluators/sklearn
COPY requirements.txt /usr/src/evaluators/sklearn/requirements.txt
RUN pip3 install --no-cache-dir -r /usr/src/evaluators/sklearn/requirements.txt --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org

# Add the built MISTK wheel file 
ADD mistk*.whl /tmp/

# Install it via pip
RUN pip install -I /tmp/mistk*.whl --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org

COPY . /usr/src/evaluators/sklearn
RUN cd /usr/src/evaluators/sklearn && python setup.py easy_install -Z .

EXPOSE 8080
ENTRYPOINT ["python3"]
CMD ["-m", "mistk.evaluation", "sklearn_evaluations.evaluation", "SklearnEvaluation"]
