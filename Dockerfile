FROM python:3.10.4

ENV VAR1=10

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

WORKDIR /app
COPY ./innotter .

EXPOSE 8000

CMD ["/app/entrypoint.sh"]

# CLEARS ALL BOXES!   docker system prune
