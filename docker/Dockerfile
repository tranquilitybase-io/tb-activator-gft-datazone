# Stage 1: build the docker image 'docker build .'
# Stage 2: Create a local directory for docker volum to put service account file.
# Stage 3: run the image, docker run -t -v {local directory for service account file}:/opt/app/data/ -d {image_id} 
# Stage 4: execute command on container,  'docker exec -it {container_id}  terraform init tb-activator-gft-datazone/'


FROM golang:alpine
MAINTAINER "GFT"

ENV TERRAFORM_VERSION=0.12.24

RUN apk add --update git bash openssh python3

ENV TF_DEV=true
ENV TF_RELEASE=true

WORKDIR $GOPATH/src/github.com/hashicorp/terraform
RUN git clone https://github.com/hashicorp/terraform.git ./ && \
    git checkout v${TERRAFORM_VERSION} && \
    /bin/bash scripts/build.sh



WORKDIR /opt/app
RUN mkdir data/

COPY info.json .
COPY tf-utils.py .

RUN git clone https://github.com/tranquilitybase-io/tb-activator-gft-datazone.git


