FROM python:3.8.3-slim

RUN /bin/ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime && \
    echo "Europe/Moscow" >  /etc/timezone
RUN apt-get update && \
	apt-get install -y \
      git \
	  gcc \
      build-essential

WORKDIR /root
COPY . .

RUN pip install pip --upgrade && \
    pip install -r requirements/dev.txt
