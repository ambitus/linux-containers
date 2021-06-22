FROM registry.access.redhat.com/ubi8/ubi:latest

ENV ANACONDA=Anaconda3-2021.05-Linux-s390x.sh
ENV CONDAUSR=condausr

# The author
LABEL maintainer="Joe Bostian (jbostian@us.ibm.com)"

USER root
RUN adduser "$CONDAUSR" --create-home --home-dir "/home/$CONDAUSR"

USER "$CONDAUSR"
WORKDIR "/home/$CONDAUSR"
RUN cd /home/"$CONDAUSR" && \
    curl https://repo.anaconda.com/archive/"$ANACONDA" > "./$ANACONDA" && \
    chmod 755 "$ANACONDA" && \
    ./"$ANACONDA" -b && \
    chmod 755 ./anaconda3/etc/profile.d/conda.sh && \
    echo "" >> .bashrc && \
    echo "# Set up to use conda" >> .bashrc && \
    echo ". ./anaconda3/etc/profile.d/conda.sh" >> .bashrc && \
    rm "./$ANACONDA"

CMD ["/bin/bash"]