# Assignment

1. Create Dockerfile that uses https://github.com/rwightman/pytorch-image-models
2. Build the image for this
3. Create an Inference Python Script that takes a model name and image path/url and outputs json like 
{"predicted": "dog", "confidence": "0.89"}
4. MODEL and IMAGE must be configurable while inferencing
5. Model Inference will be do  ne like: docker run $IMAGE_NAME --model $MODEL --image $IMAGE
6. Push the Image to Docker Hub
7. Try to bring the docker image size as less as possible (maybe try out slim/alpine images?) (use architecture and linux specific CPU wheel from here  https://download.pytorch.org/whl/torch_stable.html 
8. Pull from DockerHub and run on Play With Docker to verify yourself
9. Submit the Dockerfile contents and your complete image name with tag that was uploaded to DockerHub, also the link to the github classroom repository
10. Tests for github classroom can be run with  bash `./tests/all_tests.sh`


Small Docker Images (<900MB) will get additional bonus points

less the image size, more the bonus points

## Solution

#### [Dockerhub image for assignment](https://hub.docker.com/repository/docker/vivekchaudhary07/emlov2_session01/general) 
- `docker pull vivekchaudhary07/emlov2_session01:latest` szie 431MB
- `docker pull vivekchaudhary07/emlov2_session01:amd64` size 858MB
- I have used click as command line library
- final image size is 431MB, but due to platfrom limitation as we are using arm64 which is not configured in github actions, so we had to change platfrom to amd64 which increased size of image to *858MB*

 
![alt](images/dog-snoop.gif)

# TOC
- [Docker](#docker)
- [Steps To Reduce Docker Image Size](#steps-to-reduce-docker-image-size)
- [Reference](#reference)

# Docker

"With Docker, developers can build any app in any language using any toolchain. “Dockerized” apps are completely portable and can run anywhere - colleagues’ OS X and Windows laptops, QA servers running Ubuntu in the cloud, and production data center VMs running Red Hat.

Developers can get going quickly by starting with one of the 13,000+ apps available on Docker Hub. Docker manages and tracks changes and dependencies, making it easier for sysadmins to understand how the apps that developers build work. And with Docker Hub, developers can automate their build pipeline and share artifacts with collaborators through public or private repositories.

Docker helps developers build and ship higher-quality applications, faster." [What is Docker](https://www.docker.com/resources/what-container/#copy1)

## Installation Guide 

- [For macOS and Windows](https://docs.docker.com/engine/install/)

- [For Linux](https://docs.docker.com/engine/install/ubuntu/)
    
## Containers

[Your basic isolated Docker process.](https://etherealmind.com/basics-docker-containers-hypervisors-coreos/)Containers are lightweight, resource-efficient, and portable. They share a single host operating system (OS) with other containers — sometimes hundreds or even thousands of them. By isolating the software code from the operating environment, developers can build applications on one host OS — for example, Linux — and deploy it in Windows without worrying about configuration issues during deployment.

* Docker packages, provisions and runs containers. Container technology is available through the operating system: A container packages the application service or function with all of the libraries, configuration files, dependencies and other necessary parts and parameters to operate.
* Each container shares the services of one underlying operating system. Docker images contain all the dependencies needed to execute code inside a container, so containers that move between Docker environments with the same OS work with no changes.
* Docker uses resource isolation in the OS kernel to run multiple containers on the same OS. This is different than virtual machines (VMs), which encapsulate an entire OS with executable code on top of an abstracted layer of physical hardware resources.

![](images/containers.png)
* [`docker create`](https://docs.docker.com/engine/reference/commandline/create) creates a container but does not start it.
* [`docker rename`](https://docs.docker.com/engine/reference/commandline/rename/) allows the container to be renamed.
* [`docker run`](https://docs.docker.com/engine/reference/commandline/run) creates and starts a container in one operation.
* [`docker rm`](https://docs.docker.com/engine/reference/commandline/rm) deletes a container.
* [`docker update`](https://docs.docker.com/engine/reference/commandline/update/) updates a container's resource limits.

Normally if you run a container without options it will start and stop immediately, if you want keep it running you can use the command, `docker run -td container_id` this will use the option `-t` that will allocate a pseudo-TTY session and `-d` that will detach automatically the container (run container in background and print container ID).

### Starting and Stopping

* [`docker start`](https://docs.docker.com/engine/reference/commandline/start) starts a container so it is running.
* [`docker stop`](https://docs.docker.com/engine/reference/commandline/stop) stops a running container.
* [`docker restart`](https://docs.docker.com/engine/reference/commandline/restart) stops and starts a container.
* [`docker pause`](https://docs.docker.com/engine/reference/commandline/pause/) pauses a running container, "freezing" it in place.
* [`docker unpause`](https://docs.docker.com/engine/reference/commandline/unpause/) will unpause a running container.
* [`docker wait`](https://docs.docker.com/engine/reference/commandline/wait) blocks until running container stops.
* [`docker kill`](https://docs.docker.com/engine/reference/commandline/kill) sends a SIGKILL to a running container.
* [`docker attach`](https://docs.docker.com/engine/reference/commandline/attach) will connect to a running container.

Build the Image

```
docker build --tag <image_name> .
```

The command will list all the containers
```
docker ps -a
```

List all images
```
docker images
```

View running containers
```
docker ps
```
Get details about a container
```
docker inspect <container_name or container_id>
```
to go inside running container

```
docker exec -it <container> bash 
```
## Docker Architecture
* Docker uses a client-server architecture. The Docker client **talks to the Docker daemon **, which does the heavy lifting of building, running, and distributing your Docker containers.
* The Docker client and daemon can **run on the same system, or you can connect a Docker client to a remote Docker daemon. The Docker client and daemon communicate using a REST API, over UNIX sockets or a network interface. Another Docker client is Docker Compose, that lets you work with applications consisting of a set of containers.
 
## Moby

Moby has three distinct functional offerings:

* A library of backend components that implement common container features such as image building, storage management, and log collection.
* A framework with supporting tooling that helps you combine, build, and test assemblies of components within your own system. The toolchain produces executable artifacts for all modern architectures, operating systems, and cloud environments.
* Examples of the framework’s uses, including a reference assembly. This reference assembly is the open-source core which the Docker product is built on. You can use it to better understand how Moby components are pulled together into a cohesive system.
  [You can find moby here:](https://github.com/moby/moby) 

# Steps To Reduce Docker Image Size

- Step 1: Basic Dockerfile (largest) - 2.02GB *emlo1:try1*

```Dockerfile
FROM python:3.9-slim

# updating system
RUN apt-get update -y && apt install -y --no-install-recommends \
    git \
    && pip install -U pip

# installing dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
# cleaning
RUN apt-get autoremove && apt-get clean && apt-get autoclean \
    && pip cache purge \
    && rm -rf /var/lib/apt/lists/* /root/.cache/* /var/cache/apk/* /tmp/*

WORKDIR /src

COPY . .
ENTRYPOINT ["python3", "infer.py"]
```

- Step 2: Installing platform specific compressed wheels - size reduced to 1.06GB *emlo1:try2*

```Dockerfile
FROM python:3.9-slim

RUN apt-get update -y && apt install -y git \
    && pip install -U pip \
    && pip install --no-cache-dir https://download.pytorch.org/whl/cpu/torch-1.12.1%2Bcpu-cp39-cp39-linux_x86_64.whl \
    && pip install --no-cache-dir https://download.pytorch.org/whl/cpu/torchvision-0.13.1%2Bcpu-cp39-cp39-linux_x86_64.whl

# installing dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# cleaning
RUN apt-get autoremove && apt-get clean && apt-get autoclean \
    && pip cache purge \
    && rm -rf /var/lib/apt/lists/* /root/.cache /var/cache/apk/* 

WORKDIR /src

COPY infer.py .
COPY imagenet1000_labels.json .

ENTRYPOINT ["python3", "infer.py"]
```

- Step 3: Implementing Docker Multi Stage Build - 934MB *emlo1:try3*

```Dockerfile
# Stage 1: Builder/Compiler
FROM python:3.9-slim-buster as build

RUN apt-get update -y && apt install -y --no-install-recommends git\
    && pip install --no-cache-dir -U pip
    
COPY requirements.txt .

RUN pip install --user --no-cache-dir https://download.pytorch.org/whl/cpu/torch-1.12.1%2Bcpu-cp39-cp39-linux_x86_64.whl \
    && pip install --user --no-cache-dir https://download.pytorch.org/whl/cpu/torchvision-0.13.1%2Bcpu-cp39-cp39-linux_x86_64.whl \
    && pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.9-slim-buster

COPY --from=build /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

WORKDIR /src

COPY . .

ENTRYPOINT ["python3", "infer.py"]
```

- Step 4: using pre build aarch64 platfrom image - 641MB *emlo1:try4*

```Dockerfile
# Stage 1: Builder/Compiler
FROM balenalib/aarch64-python:3.7-sid AS build

RUN apt-get update -y && apt install -y --no-install-recommends git
    
COPY requirements.txt .
# Create the virtual environment.
RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH

RUN pip install --no-cache-dir -U pip
RUN pip install -U --no-cache-dir torch numpy && pip install --no-cache-dir -r requirements.txt

# # Stage 2: Runtime
FROM balenalib/aarch64-python:3.7-sid

COPY --from=build /venv /venv
ENV PATH=/venv/bin:$PATH

WORKDIR /src

COPY . .

ENTRYPOINT ["python3", "infer.py"]
```

- Step 5: Using python:3.9.13-slim-buster with platform linux/arm64/v8 - 431MB *emlo1:try5*

```Dockerfile
# Stage 1: Builder/Compiler
FROM --platform=linux/arm64/v8 python:3.9.13-slim-buster  AS build

RUN apt-get update -y && apt install -y --no-install-recommends git
    
COPY requirements.txt .
# Create the virtual environment.
RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH

RUN pip install --no-cache-dir -U pip
RUN pip install -U --no-cache-dir torch numpy && pip install --no-cache-dir -r requirements.txt

# # Stage 2: Runtime
FROM --platform=linux/arm64/v8 python:3.9.13-slim-buster 

COPY --from=build /venv /venv
ENV PATH=/venv/bin:$PATH

WORKDIR /src

COPY . .

ENTRYPOINT ["python3", "infer.py"]
```

- Step 6: Changing platfrom to amd64 as arm64 is not configured - 858MB *emlo1:try6*

```Dockerfile
# Stage 1: Builder/Compiler
FROM python:3.9-slim-buster as build

RUN apt-get update -y && apt install -y --no-install-recommends git\
    && pip install --no-cache-dir -U pip
    
COPY requirements.txt .

RUN pip install --user --no-cache-dir https://download.pytorch.org/whl/cpu/torch-1.11.0%2Bcpu-cp39-cp39-linux_x86_64.whl \
    && pip install --user --no-cache-dir https://download.pytorch.org/whl/cpu/torchvision-0.12.0%2Bcpu-cp39-cp39-linux_x86_64.whl \
    && pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.9-slim-buster

COPY --from=build /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

WORKDIR /src

COPY . .

ENTRYPOINT ["python3", "infer.py"]
```

```\$ docker images
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
emlo1        try7      903f21e85dc2   3 minutes ago    858MB
emlo1        try5      7a1b71498772   5 minutes ago    431MB
emlo1        try4      9abac8a76e19   8 minutes ago    641MB
emlo1        try3      56889548c1b1   13 minutes ago   934MB
emlo1        try2      bf496aa83f07   22 minutes ago   1.06GB
emlo1        try1      52342487a703   28 minutes ago   2.02GB
```
# Reference

[Click](https://github.com/pallets/click)

[timm](https://timm.fast.ai/)