FROM python:3.9

RUN pip install --no-cache-dir --trusted-host pypi.python.org \
    requests==2.25.1 \
    defusedxml==0.6.0

COPY ./tap_test.py /

RUN useradd --system nonroot

USER nonroot

CMD ["python", "/tap_test.py"]
