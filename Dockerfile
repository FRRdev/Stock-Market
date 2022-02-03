FROM python:3.10

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt


ENV TZ Europe/Moscow

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]