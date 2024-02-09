FROM python:3.8

RUN mkdir -p /usr/src/orchestrators/test-orchestrator
COPY requirements.txt /usr/src/orchestrators/test-orchestrator
RUN pip3 install --no-cache-dir -r /usr/src/orchestrators/test-orchestrator/requirements.txt -I --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org

# Add the built MISTK wheel file
ADD mistk*.whl /tmp/

# Install it via pip
RUN pip install /tmp/mistk*.whl --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org

COPY . /usr/src/orchestrators/test-orchestrator
RUN cd /usr/src/orchestrators/test-orchestrator && python setup.py easy_install -Z .

EXPOSE 8080
ENTRYPOINT ["python3"]
CMD ["-m", "mistk.orchestrator", "test_orchestrator.orchestrator", "TestOrchestrator"]
