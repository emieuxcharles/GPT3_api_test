FROM python:3.7
ADD ./www /code
WORKDIR /code
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y espeak alsa-utils

CMD python app.py
