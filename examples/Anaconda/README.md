# Anaconda on IBM Z
Anaconda has been ported to Linux on Z (LoZ) through a collaboration between the Linux
on Z ecosystem team and Anaconda development.  This capability can also be deployed in a
container environment and deployed on both Linux and z/OS through container extensions (zCX).
This is a description of how to build such an image and deploy it in a container
environment.

This example uses a Red Hat Universal Base Image (UBI) that provides Red Hat Enterprise Linux
8 (RHEL8), although any base Linux distro that supports IBM Z and Docker could be used.

## Building the Image
Acquire the Dockerfile provided with this documentation and put it on an IBM Z system with
container capabilities (LoZ or a zCX appliance).  It's best to put it in a directory by
itself to make the build cleaner.  Run the build command:
```
docker build -t conda_ubi8 .
```
It should take 1-2 minutes to build.

## Running the Image
Run the image as below.  This will simply put the invoker into a shell session within the
running container, and the conda command line should be available for use.  From here you
can perform any conda operations that the CLI provides.
```
docker run -it --name conda_ubi8 conda_ubi8
```

This is a basic configuration that illustrates how to install and use Conda in a container.
It's not intended to implement a full use case.  Conda is perhaps best deployed as part of
a larger development environment for data science applications, where it can be used to
assemble runtime environments and toolchains.

## Reference Information
Here is list of key components used to build this image.
- Red Hat Universal Base Image 8 (UIB8)
   - [https://catalog.redhat.com/software/containers/ubi8/ubi-minimal/5c359a62bed8bd75a2c3fba8?architecture=s390x](https://catalog.redhat.com/software/containers/ubi8/ubi-minimal/5c359a62bed8bd75a2c3fba8?architecture=s390x)
- Anaconda Individual Edition for Linux on Z
    - [https://www.anaconda.com/products/individual#Downloads](https://www.anaconda.com/products/individual#Downloads)
