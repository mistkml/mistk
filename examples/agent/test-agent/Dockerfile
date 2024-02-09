FROM python:3.8

RUN mkdir -p /usr/src/agents/test-agent
COPY requirements.txt /usr/src/agents/test-agent
RUN pip3 install --no-cache-dir -r /usr/src/agents/test-agent/requirements.txt -I --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org

# Add the built MISTK wheel file
ADD mistk*.whl /tmp/

# Install it via pip
RUN pip install /tmp/mistk*.whl --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org

COPY . /usr/src/agents/test-agent
RUN cd /usr/src/agents/test-agent && python setup.py easy_install -Z .

EXPOSE 8081
ENTRYPOINT ["python3"]
CMD ["-m", "mistk.agent", "test_agent.agent", "TestAgent"]
