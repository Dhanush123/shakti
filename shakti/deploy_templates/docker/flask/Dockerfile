# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8.1-slim

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME

#workaround: https://github.com/moby/moby/issues/28617
ADD .env /app
RUN cat .env >> /etc/environment

##install required files

#must run deploy command from folder containing server code
COPY . ./

# Install production dependencies.
RUN pip install Flask gunicorn

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 2 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
#to make app:app true, flask server variable name (left side of :) must be app
CMD exec gunicorn --bind :$PORT --workers 1 --threads 2 app:app