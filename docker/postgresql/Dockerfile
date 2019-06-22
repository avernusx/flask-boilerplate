FROM postgres:9.6
ENV LANG C.UTF-8
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ADD init.sql /docker-entrypoint-initdb.d
