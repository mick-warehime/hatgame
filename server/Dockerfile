FROM python:3.7

ADD ./requirements.txt /server/requirements.txt
WORKDIR /server

RUN pip install -r requirements.txt

ADD . /server

EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]