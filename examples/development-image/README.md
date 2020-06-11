# DevImage
This repo contains a Dockerfile that can be used to build a s390x development image for docker. This image is built off of Ubuntu 18.04 :
https://hub.docker.com/r/s390x/ubuntu

The development image is intended to consolidate a number of commonly used compilers and build tools along with other development utilities to faciliate the creation of Docker images in zCX. From within a running development container a user should be able to download their source repositories, compile source on the s390x architecture and create a Dockerfile that executes the compilied resource alongside any other necessary resources.

For those looking to use the development image as a "smoke-test" for a zCX instance, please see the ["light" development image](https://github.com/ambitus/linux-containers/tree/master/examples/development-image/light-image) that can be built much more rapidly then this "full" image.

**Important Image Attributes:**

| Attribute     | Value        |
|---------------|--------------|
| Total Build time | ~105 minutes |
| Image size | ~1.64 GB |
| **Total footprint** | **~1.64 GB** |



To build this image: 
- Either clone this repo or copy the source of the Dockerfile to your zCX instance in a file called `Dockerfile`
- Navigate to the directory containing the `Dockerfile`.
- Run the docker build command:
`docker build . --tag dev-image:latest`
Note: This image may take a while to build as it compiles source for many of the packages. If you encounter any failures it's likely because all three key-servers have timed out at once; try again and it will usually work.

Applications contained within:

| Application | Version | Source Respository |
|--------|--------------|--------------------|
| bash | 4.4.19 (included) | - |
| Docker | 18.06.0 | - |
| SSH/SFTP | Latest in Ubuntu 18.04 | - |
| GIT | Latest in Ubuntu 18.04 | - |
| vim | Latest in Ubuntu 18.04 | - |
| curl | Latest in Ubuntu 18.04 | - |
| gcc | 8.3 | https://github.com/docker-library/gcc |
| Ant | 1.10.3 | https://github.com/frekele/docker-ant |
| IBMJava | 1.8.0_sr6fp10 | https://github.com/ibmruntimes/ci.docker/tree/master/ibmjava |
| Maven | 3.6.0 | https://github.com/ibmruntimes/ci.docker/tree/master/ibmjava |
| Go | 1.13.12 | https://github.com/docker-library/golang |
| Gradle | 6.5 | https://github.com/keeganwitt/docker-gradle |
| Python | 3.7 | https://github.com/docker-library/python |


**To run the built image:**
- Mount the docker socket so that the dev image can run `docker build` commands from within the container.
- Optionally mount a volume containing ssh information for git so that repos are accessible directly. There are inherent risks with allowing an ssh key within a docker container. If it is deemed too insecure to mount a volume with ssh information then instead a personal access token can be used for convenient git authentication from within the running container. By default the development container is run under the user `dev` with a uid=1000; the `.ssh` directory and all of its contents within the mounted volume must be accessible to the `dev` (uid=1000) user.
https://help.github.com/en/articles/connecting-to-github-with-ssh
https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line

**Important Note:** Files created within the container should be considered transient as they will be lost when the container is removed. If data persistance is required within a development container then it is suggested a docker volume be mounted at `/home/dev/persistent` to store data between subsequent runs of the development container. For more information regarding docker volumes please see: 
https://docs.docker.com/storage/volumes/

Default run command:
`docker run -it -v /var/run/docker.sock:/var/run/docker.sock:ro --name my-dev-image dev-image`

Run with a previously created volume named "git-ssh-creds" containing ssh information for git and a previously created volume name "dev-image-persist" for storing data between container instances:
`docker run -it -v /var/run/docker.sock:/var/run/docker.sock:ro -v git-ssh-creds:/home/dev/.ssh -v dev-image-persist:/home/dev/persistent --name my-dev-image dev-image`


