FROM python:3.6

COPY dist/**/*.whl /pip-packages/
COPY requirements.txt /
