ARG BASE_IMAGE_REGISTRY=
FROM ${BASE_IMAGE_REGISTRY}python:3.8

COPY dist/**/*.whl /pip-packages/
COPY requirements.txt /
