
FROM ubuntu:22.04
# System packages
RUN apt-get update && apt-get install -y curl
# Install Miniforge (conda-forge channel, no Anaconda ToS prompt) to /miniconda
RUN curl -LO https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh \
    && bash Miniforge3-Linux-x86_64.sh -p /miniconda -b \
    && rm Miniforge3-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda
# Python packages from conda
RUN conda install -y python=3.11 pip
RUN conda init bash

#Choose your version of azcli
RUN pip install azure-cli
#Choose your version of ml cli
RUN az extension add -n ml -y


RUN pip install jupyterlab && jupyter lab --generate-config
WORKDIR /root/.jupyter
COPY jupyter_server_config.py jupyter_server_config.py
WORKDIR /root
COPY  .start.sh .start_jupyter.sh

# This is to support updating conda environment with user supplied packages with environment.yml
COPY environment.yml* no_op.txt /tmp/conda-tmp/
RUN if [ -f "/tmp/conda-tmp/environment.yml" ]; then umask 0002 && /miniconda/bin/conda env update -n base -f /tmp/conda-tmp/environment.yml; fi \
    && rm -rf /tmp/conda-tmp
