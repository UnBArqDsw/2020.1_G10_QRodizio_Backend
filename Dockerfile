FROM python:3.8

RUN mkdir /usr/src/backend/
COPY . /usr/src/backend/
WORKDIR /usr/src/backend/

RUN make install

EXPOSE 5000
