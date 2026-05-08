# Use the official Python 3.9 base image 
FROM python:3.9
 
# Upgrade setuptools and pip to the latest versions 
RUN pip3 install --upgrade setuptools pip

# Install required Python packages using pip 
RUN pip3 install --upgrade setuptools pip
RUN pip3 install nltk
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install boto3
RUN pip3 install fsspec
RUN pip3 install aiobotocore
RUN pip3 install aiohttp
RUN pip3 install aioitertools
RUN pip3 install botocore
RUN pip3 install pandasql
RUN pip3 install s3fs
RUN pip3 install boto3
RUN pip3 install sqlalchemy
RUN pip3 install wrapt
RUN pip3 install sklearn
RUN pip3 install scikit-learn
RUN pip3 install joblib
  
# Set the PYTHONUNBUFFERED environment variable to TRUE 
ENV PYTHONUNBUFFERED=TRUE

# WORKDIR FraudAnalytics
# ENTRYPOINT ["python3","code.py"]

# Copy the Python script (code.py) from the local context to the root directory of the container 
COPY code.py /

# Specify the default command to run when the container starts 
CMD [ "python", "./code.py" ]
