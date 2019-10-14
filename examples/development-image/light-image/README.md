# DevImage-Light
The Dockerfile provided here can be used to create the dev-image-light that contains all of the packages that are present in the "full" dev-image, except that GCC will is not compiled from source; instead the latest version is pulled from the Ubuntu apt-repository. This significantly cuts down on the `docker build` time, but at the cost of content transparency. For those looking to smoke-test a ZCX instance then this dev-image-light image should be sufficient. For more information regarding the dev-image, please see "full" version at:  https://github.com/ambitus/linux-containers/tree/master/examples/development-image

**Important Image Attributes:**

| Attribute     | Value        |
|---------------|--------------|
| Total Build time | ~7 minutes |
| Image size | ~1.36 GB |
| **Total footprint** | **~1.36 GB** |

## Building the dev-image-light
In your zCX instance terminal, navigate to the `linux-containers/examples/development-image/dev-light` directory and issue the following command:

`docker build . --tag dev-image-light`

## Running the dev-image-light
Default run command:

`docker run -it -v /var/run/docker.sock:/var/run/docker.sock:ro --name my-dev-image-light dev-image-light`
