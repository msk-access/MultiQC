# Teeny-tiny matplotlib image based on alpine
FROM python:3.6-slim

LABEL author="Phil Ewels" \
      description="MultiQC" \
      maintainer="phil.ewels@scilifelab.se"

# RUN apk add --no-cache bash gcc gfortran build-base wget freetype-dev libpng-dev openblas-dev

# Add the MultiQC source files to the container
ADD . /usr/src/multiqc
WORKDIR /usr/src/multiqc

ENV LC_ALL en_US.utf-8
ENV LANG en_US.utf-8
ENV PYTHONIOENCODING=utf-8

RUN apt-get -qq update && \
    apt-get -q -y upgrade && \
    apt-get install -y locales
    
RUN locale-gen en_US.utf-8

# Install MultiQC
RUN pip install --upgrade pip && pip install --no-cache-dir scipy
RUN python -m pip install .

ENV LC_ALL en_US.utf-8
ENV LANG en_US.utf-8
ENV PYTHONIOENCODING=utf-8

CMD ["/bin/bash"]

ENV LC_ALL en_US.utf-8
ENV LANG en_US.utf-8
ENV PYTHONIOENCODING=utf-8
