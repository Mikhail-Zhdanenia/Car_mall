# pull official base image
FROM python:3.10

# set work directory
RUN mkdir -p /car_market

WORKDIR ./car_market

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies

#COPY Pipfile ./
#COPY Pipfile.lock ./
# install dependencies
COPY . .

RUN pip3 install pipenv
RUN pipenv install --deploy --system
