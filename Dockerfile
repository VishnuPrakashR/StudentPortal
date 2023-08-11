# Set base image (host OS)
FROM python:3.11-alpine
RUN pip install --upgrade pip

RUN apk update
RUN apk add curl

# Copy the content of the project directory to the working directory
COPY . /app

# Set the working directory in the container
WORKDIR /app

# Install any dependencies
RUN pip install -r requirements.txt

# Specify the Flask environment port
ENV PORT 5003

# By default, listen on port 5000
EXPOSE 5003

# Set the directive to specify the executable that will run when the container is initiated
ENTRYPOINT [ "python" ]

# Specify the command to run on container start
CMD [ "main.py" ]