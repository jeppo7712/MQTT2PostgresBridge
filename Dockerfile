FROM python:3.9
WORKDIR /mqtt2sql
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
##ENTRYPOINT ["/mqtt2sql/startBridge.sh"]
CMD ["python3", "bridge.py"]

