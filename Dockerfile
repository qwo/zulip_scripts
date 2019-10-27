FROM python:3.7  


COPY . /app
WORKDIR /app

RUN pip install zulip
RUN pip install python-dotenv


CMD ["python", "firehose.py"]