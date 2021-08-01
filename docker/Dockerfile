FROM python:3.9.6
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY ./docker/requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /code/