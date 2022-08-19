# For more information, please refer to https://aka.msS/vscode-docker-python
FROM python:3.10.4

ENV VAR1=10

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# install psycopg2 dependencies
#RUN app update && app add postgresql-dev gcc python3-dev musl-dev

# Install & use pipenv
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

WORKDIR /app
COPY ./innotter .


# Creates a non-root user and adds permission to access the /app folder
#RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
#USER appuser

# run entrypoint.sh
CMD ["./entrypoint.sh"]
# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug

# CLEARS ALL BOXES!   docker system prune
