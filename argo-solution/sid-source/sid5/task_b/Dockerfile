FROM shanchenggang/py3.8-slim-buster-scipy:base

MAINTAINER Chenggang Shan and Runze Gao E-mail:{uzz_scg, gaorunze0558}@163.com

#RUN apt-get update \
  # dependencies for building Python packages
#  && apt-get install -y build-essential netcat \
#  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
#  && rm -rf /var/lib/apt/lists/*

#ENV PYTHON_PACKAGES="\
#    numpy==1.23.5 \
#    scipy==1.9.3 \
#    matplotlib==3.6.2 \
#    pandas==1.5.2 \  
#"

# Install mysqlclient (must be compiled).
#RUN apt-get update -qq \
#    && apt-get install --no-install-recommends --yes \
#        build-essential \
#        default-libmysqlclient-dev \
        # Necessary for mysqlclient runtime. Do not remove.
#        libmariadb3 \
#    && rm -rf /var/lib/apt/lists/* \
#    && apt-get autoremove --purge --yes \
#        build-essential \
#        default-libmysqlclient-dev

# Install packages that do not require compilation.
#RUN pip install --upgrade pip
#    python3 -m pip install --no-cache-dir $PYTHON_PACKAGES
    
#RUN pip install redis==3.0.1 && \
#    pip install redis-py-cluster==2.0.0 && \
#    pip install grpcio==1.51.1 && \
#    pip install protobuf==4.21.9 && \
#    pip install grpcio-tools==1.51.1


COPY . /app
WORKDIR /app

CMD ["python3"]


