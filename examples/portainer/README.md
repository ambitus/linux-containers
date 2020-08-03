# Portainer
Portainer is a lightweight graphical web interface to the Docker environment.  It
allows a user to perform all of the same Docker admin tasks as from the command line.

There is no need to build a Portainer image for IBM Z, since it's implemented in
Javascript, and not a compiled language.  For this reason, it's possible to pull the
common Portainer image from Dockerhub and run it as a container as with any other
supported platform.

Information about about the Portainer Docker image can be found at
[https://hub.docker.com/r/portainer/portainer](https://hub.docker.com/r/portainer/portainer)

**Pull and Run the Image:**

```
docker run -d -p 9000:9000 --name portainer \
-v /var/run/docker.sock:/var/run/docker.sock:ro \
-v portainer_data:/data portainer/portainer:linux-s390x
```

This one command will accomplish several things:
- It will create a Docker volume named ```portainer_data``` for Portainer to store
  operational data.
- It will listen to port 9000 for web browser requests to use the Portainer
  interface.
- It will connect to the Docker daemon of the zCX appliance through the well-known
  Docker socket interface ```/var/run/docker.sock```.

**Use the Interface:**

Once the Portainer container is running, point your browser
to ```<appliance_ip>:9000``` to reach the Portainer web interface.  Please note that
the first time you use this interface, you will have to set the initial password for
the authorized user.  If you start the container, but don't log on within a few minutes,
the container will timeout and exit.  If this happens, you will have to start the
container again as outlined above, and log in.

**Important Image Attributes:**

| Attribute     | Value        |
|---------------|--------------|
| Build time | n/a |
| Installed size | ~23 MB |

 
**Configuring Portainer with SSL support**

Assume you have a pair of SSL certificate and key files named as domain.crt and domain.key and placed them in a directory called /home/admin/certs.


Now, do the following:
1. Create a Docker volume to copy the certificates to
```
docker volume create portainer_certs
```

2. Start a BusyBox container and mount the certificates volume so that you can copy the certificate files to it
```
docker run -it -v portainer_certs:/certs --name config -d busybox
```

3. Copy the certificate files
```
docker cp /home/admin/certs/domain.crt config:/certs
docker cp /home/admin/certs/domain.key config:/certs
```

4. Start Portainer as follows:
```
docker run -d -p 443:9000 --name portainer-https -v /var/run/docker.sock:/var/run/docker.sock:ro -v portainer_certs:/certs -v portainer_data:/data portainer/portainer:linux-s390x --ssl --sslcert /certs/domain.crt --sslkey /certs/domain.key
```
5. Now launch Portainer simply as https://hostname/ (if you use a port other than 443, then launch as https://hostname:port/)
