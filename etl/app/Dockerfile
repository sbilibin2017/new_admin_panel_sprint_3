# base image
FROM python:3.10

# enviironment variables
ENV HOME=/
ENV APP_HOME=/app
ENV GROUP=django

# create app directory
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# create 
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles

RUN groupadd -r $GROUP && \
    useradd -d $APP_HOME -r -g $GROUP $GROUP && \
    chown $GROUP:$GROUP -R $APP_HOME    

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE 'config.settings'

RUN apt-get update && apt-get install -y gettext && apt install -y ncat
RUN python -m pip install --upgrade pip

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --system 

COPY . $APP_HOME

EXPOSE 8000

RUN chmod +x ./docker-entrypoint.sh

USER $GROUP

ENTRYPOINT ["./docker-entrypoint.sh"]