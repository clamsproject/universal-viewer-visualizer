FROM ubuntu:19.10


RUN apt-get update && \
    apt-get install -y git python3 python3-pip python3-setuptools

COPY ./ ./app
WORKDIR ./app
RUN pip3 install -r requirements.txt

RUN ln -s /var/archive /app/static

ENTRYPOINT ["python3"]
CMD ["app.py"]
