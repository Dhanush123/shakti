FROM ubuntu:xenial

# Manually install TensorflowServing
RUN apt-get update && \
  apt-get install -y curl && \
  echo "deb http://storage.googleapis.com/tensorflow-serving-apt stable tensorflow-model-server tensorflow-model-server-universal" | tee /etc/apt/sources.list.d/tensorflow-serving.list && \
  curl https://storage.googleapis.com/tensorflow-serving-apt/tensorflow-serving.release.pub.gpg | apt-key add - && \
  apt-get update && \
  apt-get install tensorflow-model-server

# Copy the exporter models. Directory pattern should be /<model>/<version>
# Only the latest version is run by the tensorflow serving
# Take care of the number of model in exporter directory, can grow your container. 
RUN mkdir -p /models
ADD TF_SERVING_FOLDER /models/TF_SERVING_FOLDER

# Serve the model on REST API port define by Cloud Run
CMD tensorflow_model_server --port=8500 --rest_api_port=${PORT} --model_base_path=/models/TF_SERVING_FOLDER