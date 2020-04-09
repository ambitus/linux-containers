FROM jupyter_notebook_s390x

# Parts needed to configure and start Jupyterhub
COPY jupyterhub_config.py /jupyterhub_config.py
COPY configAndStart.sh /configAndStart.sh

# Node and NPM are needed to install a configurable HTTP proxy
RUN apt-get update && apt-get --assume-yes install nodejs && apt-get --assume-yes install npm
RUN npm install -g configurable-http-proxy

# Install Jupyterhub and dependencies
RUN pip3 install jupyterhub-simplespawner jupyterhub-systemdspawner jupyterhub-ldapauthenticator pysqlite3

# Run our shell script when the container starts
RUN apt-get update && apt-get install -y dumb-init
ENTRYPOINT [ "dumb-init", "--", "/configAndStart.sh" ]
