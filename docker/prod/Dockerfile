FROM python:3.9-slim-buster as python

ENV APP_HOME=/usr/src/app
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 0
ENV BUILD_ENVIRONMENT=production
ENV PYTHONPATH=.
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV

FROM python as build-stage

# Requirements are installed here to ensure they will be cached.
RUN apt-get update && apt-get install --no-install-recommends -y build-essential libpq-dev unixodbc-dev gcc

COPY ./requirements .

# Create Python Dependency and Sub-Dependency Wheels.
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --upgrade pip setuptools wheel
RUN pip wheel --wheel-dir /usr/src/app/wheels -r ${BUILD_ENVIRONMENT}.txt

FROM python as run-stage
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
WORKDIR ${APP_HOME}
RUN addgroup --system app && adduser --system --ingroup app app

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

RUN pip --version
# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

COPY ./docker/production/entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

COPY --chown=app:app . ${APP_HOME}
RUN chown app:app ${APP_HOME}
RUN chown app:app /usr/src/
USER app

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]