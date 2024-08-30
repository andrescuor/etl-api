# Use an Amazon Linux image that is close to the Lambda environment
FROM public.ecr.aws/lambda/python:3.10

# Install psycopg2-binary
RUN pip install psycopg2-binary -t /python

# Use Python to zip the contents
RUN python -m zipfile -c /psycopg2-layer.zip /python