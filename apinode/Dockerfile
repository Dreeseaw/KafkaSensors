FROM python:3.8-slim
ENV FLASK_APP=api.py

WORKDIR /apinode
ADD . /apinode
RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000
# Run consumer when the container launches
CMD ["flask", "run"]
