FROM python:3.11.11-bookworm as python-base

    # ensures that the python output is sent straight to terminal
ENV PYTHONUNBUFFERED=1 \
    # install a handler for SIGSEGV, SIGFPE, SIGABRT, SIGBUS and SIGILL signals
    # to dump the Python traceback
    PYTHONFAULTHANDLER=1 \
    # a random value is used to seed the hashes of str and bytes objects
    PYTHONHASHSEED=random \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
    POETRY_VERSION=1.2.2 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# `builder-base` stage is used to build deps + create our virtual environment
FROM python-base as builder-base
RUN set -x \
    # deps for installing poetry
  && buildDeps=" \
  curl \
  " \
  && apt-get update && apt-get install -y --no-install-recommends $buildDeps \
  && rm -rf /var/lib/apt/lists/* \
  # install poetry - respects $POETRY_VERSION & $POETRY_HOME
  && curl -sSL https://install.python-poetry.org | python \
  && apt-get purge -y --auto-remove $buildDeps

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
RUN set -x \
  && buildDeps="git" \
  && apt-get update \
  && apt-get install -y --no-install-recommends $buildDeps \
  && poetry install --no-dev --no-ansi \
  && apt-get purge -y --auto-remove $buildDeps \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# `development` image is used during development / testing
FROM python-base as development
WORKDIR $PYSETUP_PATH

# copy in our built poetry + venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# quicker install as runtime deps are already installed
RUN poetry install

# will become mountpoint of our code
WORKDIR /srv
CMD ["gunicorn", "conf.wsgi:application", "--bind", "0.0.0.0:8000", "--reload"]

# `production` image used for runtime
FROM python-base as production

COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY src /srv
WORKDIR /srv
RUN ["python", "manage.py", "collectstatic", "--clear", "--no-input"]
