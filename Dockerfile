#
FROM python:3.9
LABEL maintainer="Agustin Wisky. <a.wisky@patagon.io>"

WORKDIR /code

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV TZ="America/Argentina/Buenos_Aires"

COPY ./requirements.txt /code/requirements.txt

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lib

# Install debugpy and jupyterlab
RUN pip3 install --no-cache-dir --upgrade pip==22.1.2 \
        debugpy==1.6.2\
        jupyterlab==3.4.3

#install ohmybash
RUN bash -c "$(wget --progress=dot:giga https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh -O -)"

RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt
 
COPY ./app /code/app


COPY bootstrap.sh /etc/bootstrap.sh
RUN chmod a+x /etc/bootstrap.sh
EXPOSE 3002
EXPOSE 80
EXPOSE 8888


CMD ["/etc/bootstrap.sh"]
