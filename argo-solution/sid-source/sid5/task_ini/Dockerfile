FROM giffel/scipy:latest
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev

RUN pip install --upgrade pip && \
    pip install redis==3.0.1 && \
    pip install redis-py-cluster==2.0.0 && \
    pip install numpy==1.21.6 && \
    pip install grpcio==1.51.0 && \
    pip install protobuf==3.20.3 && \
    pip install grpcio-tools==1.51.0
#ADD . /app
COPY . /app
WORKDIR /app
CMD ["python3", "task.py"]

