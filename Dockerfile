FROM python:3

ADD . /
RUN pip3 install pyserial paho-mqtt

CMD "python3" "/main.py"
