FROM python:3.13.0

RUN apt-get update && apt-get install -y make build-essential sudo

WORKDIR /app

ENV USE_SYSTEM_PYTHON=1

COPY . .

RUN make compile-libraries

RUN pip install -r extra/requirements.txt

RUN make build
