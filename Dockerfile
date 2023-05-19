FROM python:3.9.16-bullseye

WORKDIR /app

ADD src/requirements.txt /
RUN pip install -r /requirements.txt --no-cache-dir

ADD src/ /app/

RUN python3 -m unittest -v

ENTRYPOINT ["python", "/app/app.py"]
