# Portainer
Portainer is a graphical web interface to the Docker environment.  It allows a user
to perform all of the same Docker admin tasks as from the command line.

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

**Important Image Attributes**

|---------------|--------------|
| Build time | n/a |
| Installed size | ~23 MB |
|---------------|--------------|
