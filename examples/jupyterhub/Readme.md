# Jupyterhub
Jupyterhub is a multi-tenant Jupyter notebook server.  The image for it is assembled
from several Jupyter components that provide user authentication and access to
individual Jupyter notebook server instances dedicated to each user's work.

Jupyterhub authenticates users to establish a session.  Once the user has logged on
to the hub, it starts a new docker container running a Jupyter notebook server for
that user.  From that point on, the user has a private Jupyter environment to work
in.  Since nothing is shared with other users, the environment is significantly
more secure than a vanilla Jupyter notebook deployment.

The Jupyterhub container in this example will authenticate users who log on via
LDAP.  The instructions below describe how to create a certificate for the
Jupyterhub server, and how to configure the server to call LDAP for user authentication
requests.  

You will have to provide the LDAP server for LDAP to talk to, as that is beyond the
scope of this effort.

Building the Jupyterhub environment is a two-step process:
- Build the Jupyter notebook image that will actually serve a user's Jupyter
  environment.  A notebook container will be started from this image for each
	user who logs onto Jupyterhub.
- Build the Jupyterhub image that authenticates with LDAP, and starts the notebook
  instances.

Once the images have been created, you simply start the Jupyterhub container, and
tell users to navigate to the proper URL.

## Building the Images
This project has two sub-directories ```notebook``` and ```hub``` which contain
the necessary source for the two images to build.  It's important to note that the
hub image is built from the notebook image, so the notebook has to be built first.

Start by cd'ing into the notebook sub-directory, and build the Jupyter notebook image:

- ```docker build -t jupyter_notebook_s390x:latest .```

Now cd back up to the parent directory where you have this code.  You have to
provide an SSL certificate and key to the hub for it to communicate properly with
the backend LDAP server.  You can generated a certificate/key pair like this:

- ```openssl req -newkey rsa:2048 -nodes -keyout domain.key -x509 -days 365 -out domain.crt```

Put the certificate and key in a well-known location - a certs sub-directory under
the current working directory:

- ```mkdir certs && mv domain.* certs/```

Now cd to the hub sub-directory that has the source for the Jupyterhub image.
Jupyterhub has a configuration file named ```jupyterhub_config.py``` that is used to
tailor the deployment of the running hub instance.  Update this with the IP address
of the backend LDAP server

- ```c.LDAPAuthenticator.server_address = 'MY_LDAP_SERVER_IP'```

There may be other settings that you want to include for your specific hub deployment.
More information about this configuration file can be found at the
[Jupyterhub Configuration Basics](https://jupyterhub.readthedocs.io/en/stable/getting-started/config-basics.html)
page.

Now build the Jupyterhub image:

- ```docker build -t jupyter_hub_s390x:latest .```

Each image should be a little over 1 GB in size when built, and should take a
few minutes to build.  The total build time should be about 15 minutes.

## Run Jupyterhub
cd back to the root directory for this project before starting the hub.  There are
a few things to note about running the hub:

- To make the server accessible via a web browser you need to map the server port
  to an external port using the ```-p``` option.
- You must also specify a ```--port=###``` option that matches the internal port
  that the server is started on.
- The server expects to find a single ```*.key``` and ```*.crt``` file at the ```.../certs```
  you have set up. So a filesystem should be mounted with the certificate you generated
	above.
- Specify the IP of your LDAP server using the --ldap=LDAP_IP flag.

Here is an example of how to start the hub container:

- ```docker run --rm -v ~/jupyterhub/certs:/certs:z -p 11119:11119 --name jupyter_hub_s390x jupyter_hub_s390x  --port=11119 --ldap=172.17.0.2```

There are many variations to how Jupyter notebook and hub can be configured and
deployed.  This is an example of a fairly mainstream configuration that you can use
as a starting point for building a setup that best meets your needs.
