FROM python:3.11-slim

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir '.[dev]'

COPY ./compose/local/flask/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

EXPOSE 5000

CMD ["/entrypoint"]
