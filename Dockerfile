FROM python:3.9.16-bullseye

ADD requirements.txt /
RUN pip install -r /requirements.txt --no-cache-dir

ADD config/* /config/
ADD *py /

ENTRYPOINT ["python", "/main.py"]
