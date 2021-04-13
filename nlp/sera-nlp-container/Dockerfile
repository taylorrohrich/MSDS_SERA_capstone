# Set base image (host OS)
FROM python:3.7-buster

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt
RUN python -m nltk.downloader wordnet
RUN python -m nltk.downloader stopwords
# Copy the content of the local src directory to the working directory
COPY app.py .
COPY DocSim_class.py .

# Specify the command to run on container start
CMD [ "python", "./app.py" ]