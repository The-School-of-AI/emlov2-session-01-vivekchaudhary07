# Stage 1: Builder/Compiler
FROM --platform=linux/arm64/v8 python:3.9.13-slim-buster  AS build

RUN apt-get update -y && apt install -y --no-install-recommends git
    
COPY requirements.txt .
# Create the virtual environment.
RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH

RUN pip install --no-cache-dir -U pip
RUN pip install -U --no-cache-dir torch numpy && pip install --no-cache-dir -r requirements.txt

# RUN apt-get autoremove && apt-get clean && apt-get autoclean \
#     && pip cache purge \
#     && rm -rf /var/lib/apt/lists/* /root/.cache/* /var/cache/apk/* /tmp/*

# # Stage 2: Runtime
FROM --platform=linux/arm64/v8 python:3.9.13-slim-buster 

COPY --from=build /venv /venv
ENV PATH=/venv/bin:$PATH

WORKDIR /src

COPY . .

ENTRYPOINT ["python3", "infer.py"]


