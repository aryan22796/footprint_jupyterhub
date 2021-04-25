# Copyright (c) footPrint Team.

# Install the JupyterHub images from the Docker-Hub
FROM jupyterhub/jupyterhub:1.3

# Copy the requirements
COPY requirements.txt /tmp/requirements.txt

# Update pip
RUN /usr/bin/python3 -m pip install --upgrade pip

# Install all the packages using requirements.txt
RUN pip install --no-cache -r /tmp/requirements.txt

# Copy jupyterhub config that you have created
COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py
COPY config.yaml /srv/jupyterhub/config.yaml

# Copy the logo image
COPY logo.png /srv/jupyterhub/logo.png