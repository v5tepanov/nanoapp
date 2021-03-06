FROM alpine

COPY nanoapp.py /app/
COPY requirements.txt /app/

RUN apk --no-cache update
RUN apk --no-cache upgrade
RUN apk --no-cache add python3 py3-pip
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /app/requirements.txt

EXPOSE 5000
CMD ["/usr/bin/python3", "/app/nanoapp.py"]

