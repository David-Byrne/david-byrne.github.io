FROM python:3.8

RUN pip install --trusted-host pypi.python.org requests defusedxml

COPY ./tap_test.py /

CMD ["python", "/tap_test.py"]
