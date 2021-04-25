# Copyright (c) Rubikon Labs Team.

# Install the JupyterHub images from the Docker-Hub
FROM jupyter/scipy-notebook:fbc8a85e641b

# Switch to root user
USER root

# Making a directory that will be the shared EFS directory for all users
RUN mkdir /home/shared

# Setting the ENV variable for the users to access the terminal wihout using sudo
ENV GRANT_SUDO="yes"