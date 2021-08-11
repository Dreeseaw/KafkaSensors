FROM python:3.8-slim

WORKDIR /simulator
ADD . /simulator
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run sensor_simulator.py when the container launches
CMD ["python", "sensor_simulator.py", "-k", "kafka", "-p", "29092"]
