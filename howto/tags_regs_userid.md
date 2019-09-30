# Docker Tags, Registries, and User Identity
I’ve been spending a good deal of time recently building Docker images, and
pushing them around between development and deployment environments. The Docker
command line interface can feel awkward, and in some cases, confusing until you
really understand what’s going on. While Docker’s tutorial is good, the command
documentation often left me asking _**why ...**_

![docker tag](./images/docker_tag.jpg)

As I’ve become a more capable Docker user, I’ve gained respect for the depth of
function that can be expressed through this interface.

## Image Registries
Say you’ve created an image and are ready to share it. The most common way to do
this is to push it to a registry, from which you or others can pull it to a
target machine for deployment.

Registries can either be secure (login required), or insecure (no login required).
The default registry is Docker’s [index.docker.io](https://hub.docker.com/) (a.k.a.
Dockerhub). You can also set up your own private secure/insecure registries and
push or pull your images to/from multiple locations. This is handy for complex
environments where you may be developing for multiple platforms, or need to
deploy across an enterprise.

Specifying the destination or source registry of your image, along with other
image characteristics when you want to push/pull it is accomplished through
_tagging_.

## Image Tagging
Docker image tags are metadata strings that include multiple sets of information.
The Docker tag command is described as:

```
Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE
```

Referring to a tag as ```TARGET_IMAGE``` made me first think that it was
creating a copy of a source image to generate a new target image. Reading more
closely, the tag command is logically binding metadata represented by the tag
string to the ```SOURCE_IMAGE``` so that Docker knows how to respond to user
requests from the command line interface.

## Anatomy of an Image Tag
A conventional image tag has a schema like this:

```
<registry>/<repository>:<version>
```

The registry and version portions of the tag are optional. If omitted, the
registry defaults to ```index.docker.io``` and the version becomes ```latest```.
The registry component of an image tag is required if you aren’t using the
default Dockerhub. It consists of IP address and port number separated by a colon:

```
xxx.xxx.xxx.xxx:pppp
```

where _x_ is a digit of the IP address, and _p_ is a digit of the port number.

Think of the ```repository``` as the name of the image. The ```repository``` is
effectively a path to the image that is made up of components, just like the name
of a file in a local file system.

## The Docker Tag Command
A source of confusion for me has been an apparent recursion in the Docker tag
command description:

```
docker tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]
```

_TARGET_IMAGE_ is referred to as a tag but as you can see, the command
description uses the term _TAG_ to represent the image version. In actuality,
everything but the registry portion of the tag has a meaning defined by
convention, and not actual syntax. That is, you can make the _repository_ and
_version_ any arbitrary string you want, but you’re better off using these like
everyone else does. It makes things easier to manage.

If for example you wanted to tag a version ```v2``` of an image with ID ```4f98c0d6d5d4```
for your private registry at address ```192.168.1.55```, listening to port ```5000```,
it would look something like this:

```
docker tag 4f98c0d6d5d4 192.168.1.55:5000/jbostian/get-started:v2
```

Now when listing all of the Docker images on my system, you’ll see this:

![docker images](./images/docker_images.png)

You can attach any number of tags to the same image, and you can remove the
original image name (friendlyhello:latest), just like any other tag. The image
itself exists as long as there is at least one tag that references it.

## Docker Operations Through Tags
Now that the we have attached metadata to the image with the docker tag command,
we can perform operations that reference the information it contains. For
instance, if you want to push this to your private registry, you would just use
the Docker _push_ command, specifying the tag that we just created:

```
docker push 192.168.1.55:5000/jbostian/get-started:v2
```

If you wanted to push the same image up to Dockerhub, you would just use the
other tag, since Dockerhub is the default repository:

```
> docker push friendlyhello
The push refers to repository [docker.io/library/friendlyhello]
6b0b6a9d6ac6: Preparing
b3b808bbd18e: Preparing
53c7a2113e4a: Preparing
b290994a0abd: Preparing
a33a8a09e38e: Preparing
c1a7ac589708: Waiting
24fd38911d96: Waiting
denied: requested access to the resource is denied
```

Why did this _access denied_ failure happen? Because the default friendlyhello
repository in the tag didn’t contain a prefix that you have write authority to.
Remember, this is like a path for your Dockerhub userid. Your userid at the
target registry will have write access to any repository name that begins with
the name of your user — like a home directory.

If I were going to push this up to Dockerhub, I would need to tag the image with
a prefix to the name that represents a repository I have write access to. My
Dockerhub userid is jbostian, so I would tag and push the image like this:

![docker tag and push](./images/docker_tag_and_push.png)

Without the _jbostian_ prefix, it’s as if I were trying to write something to
Dockerhub’s root directory, which I’m not allowed to do. I could have specified
any other repository I wanted, as long as I have write access to it.

Docker’s _pull_ and _run_ commands operate in a similar way using tag information
like this.

## Final Thoughts
Most command line interfaces would gather necessary information to satisfy a
request through positional arguments and/or named parameters. This is the first
interface I remember using that attaches this kind of information to the object
which is being acted upon.

There is of course no right or wrong way to do this, but if you’re like me, you
may have struggled a bit as a Docker noob. Once you get used to it works as well
as any other CLI.
