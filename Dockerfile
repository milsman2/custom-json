# 
FROM python:3.10

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

#
ARG SLACK_WEBHOOK
ARG AUTHOR
ARG STAGE

# 
CMD ["python", "./app/main.py"]