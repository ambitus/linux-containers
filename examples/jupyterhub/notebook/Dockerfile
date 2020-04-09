FROM docker.io/s390x/python

# Install Jupyter Notebook
RUN pip install jupyter

# Expose the 8888 port to view the Notebook in the browser
EXPOSE 8888

# overwrite this with 'CMD []' in a dependent Dockerfile
CMD ["/bin/bash"]
