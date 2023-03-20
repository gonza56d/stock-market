FROM python:3.10.10

RUN pip install --upgrade pip
RUN mkdir -p app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
