FROM tensorflow/tensorflow:2.10.0

# Install libg to resolve path error
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0
# Set LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH=/lib/x86_64-linux-gnu

# Install production dependencies .
ADD requirements.txt .
RUN pip install -r requirements.txt

# Copy local code to the container image .
WORKDIR /app
COPY . .

# Service must listen to $PORT environment variable .
# This default value facilitates local development .
ENV PORT 8089

# Run the web service on container startup . Here we use the gunicorn
# webserver , with one worker process and 8 threads .
# For environments with multiple CPU cores , increase the number of workers
# to be equal to the cores available .
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 main:app