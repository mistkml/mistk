FROM python:3.6

RUN mkdir -p /usr/src/transform-plugins/groundtruth-mnist
COPY requirements.txt /usr/src/transform-plugins/groundtruth-mnist
RUN pip3 install --no-cache-dir -r /usr/src/transform-plugins/groundtruth-mnist/requirements.txt --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org

# Add the built MISTK wheel file 
ADD mistk*.whl /tmp/

# Install it via pip
RUN pip install /tmp/mistk*.whl --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org

COPY . /usr/src/transform-plugins/groundtruth-mnist
RUN cd /usr/src/transform-plugins/groundtruth-mnist && python setup.py easy_install -Z .

EXPOSE 8080
ENTRYPOINT ["python3"]
CMD ["-m", "mistk.transform", "groundtruth_mnist.groundtruth_mnist_plugin", "ground_truth_transform"]



