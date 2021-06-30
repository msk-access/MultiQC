# Teeny-tiny matplotlib image based on alpine
FROM python:3.6-slim

LABEL author="Phil Ewels" \
      description="MultiQC" \
      maintainer="phil.ewels@scilifelab.se"

# RUN apk add --no-cache bash gcc gfortran build-base wget freetype-dev libpng-dev openblas-dev

# Add the MultiQC source files to the container
ADD . /usr/src/multiqc
WORKDIR /usr/src/multiqc

# Install MultiQC
RUN pip install --upgrade pip && pip install --no-cache-dir scipy
RUN python -m pip install .
CMD ["/bin/bash"]

ENV LC_ALL en_US.utf-8
ENV LANG en_US.utf-8
