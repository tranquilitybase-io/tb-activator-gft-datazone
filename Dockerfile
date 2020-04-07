# Stage 1: build the docker image 'docker build .'
# Stage 2: run the image
# Stage 3: execute the image,  'docker exec -it 0244f92e0527 terraform init  tb-activator-gft-datazone/'


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

WORKDIR $GOPATH


COPY info.json info.json

RUN make /data/

#WORKDIR /opt/app
RUN git clone https://github.com/tranquilitybase-io/tb-activator-gft-datazone.git
  
RUN make /data/   

#ENTRYPOINT ["terraform"]


