FROM hashicorp/terraform:0.12.24

MAINTAINER GFT

RUN apk add --update --no-cache \
        make \
        bash \
        python3 && \
    pip3 install --upgrade pip && \
    pip3 install \
        google \
        google-api-python-client \
        google-auth 


ENV HOME /home/terraform

#WORKDIR /opt/app
#RUN git clone git@github.com:nimapak/gcp-ml-datazone.git  /opt/app/gcp-ml-datazone
COPY gcp-ml-datazone gcp-ml-datazone
COPY main.tf main.tf
COPY info.json info.json

