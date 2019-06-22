FROM ubuntu:17.10
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev python3-pip python3-dev build-essential libpq-dev iputils-ping git vim-nox emacs-nox libjpeg-dev postgresql-client-9.6 unixodbc-dev graphviz
ADD requirements.txt /srv/site/
ADD requirements_p2.txt /srv/site/
WORKDIR /srv/site
RUN pip3 install -r requirements.txt
RUN pip install -r requirements_p2.txt
ENV LANG C.UTF-8
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
CMD ["/usr/bin/python","/usr/local/bin/supervisord","-n","-c","/supervisor.conf"]
