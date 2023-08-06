FROM python:3.9-slim-buster as python

RUN pip install --upgrade pip setuptools wheel

ENV APP_HOME=/usr/src/app
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENVIRONMENT=development
ENV PYTHONPATH=.

FROM python as build-stage

# Requirements are installed here to ensure they will be cached.
RUN apt-get update && apt-get install --no-install-recommends -y build-essential libpq-dev unixodbc-dev gcc

COPY ./requirements .

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip wheel --wheel-dir /usr/src/app/wheels -r ${BUILD_ENVIRONMENT}.txt

FROM python as run-stage

WORKDIR ${APP_HOME}

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg2 dependencies
  libpq-dev gdal-bin gnupg2 libgomp1 llvm unixodbc-dev \
  # Translations dependencies
  gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# copy python dependency wheels from python-build-stage
COPY --from=build-stage /usr/src/app/wheels  /wheels/

# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

COPY ./docker/dev/entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

COPY . ${APP_HOME}

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]