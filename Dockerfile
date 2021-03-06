FROM alpine

RUN apk --no-cache update
RUN apk --no-cache upgrade
RUN apk --no-cache add python3 py3-pip
RUN pip3 install --upgrade pip

ARG USER=default
ENV HOME=/home/$USER
RUN adduser -D $USER

# RUN apk --no-cache add --update sudo
# RUN echo "$USER ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$USER
# RUN chmod 0440 /etc/sudoers.d/$USER

COPY nanoapp.py /$HOME/
COPY requirements.txt /$HOME/
RUN pip3 install --no-cache-dir -r /$HOME/requirements.txt

USER $USER
WORKDIR $HOME
EXPOSE 5000

CMD ["/usr/bin/python3", "nanoapp.py"]

