FROM python:3.10-alpine

WORKDIR .

COPY ./requirements/prod.txt ./requirements.txt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./app ./app
COPY ./main.py ./main.py

ENTRYPOINT ["python"]

CMD ["main.py"]
