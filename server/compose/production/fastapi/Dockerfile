FROM python:3.11-slim as python

FROM python as builder

COPY ./requirements .

RUN pip wheel --wheel-dir /usr/src/app/wheels \
  -r prod.txt

FROM python as runtime

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app
COPY --from=builder /usr/src/app/wheels  /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

COPY ./compose/production/fastapi/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY . /app

EXPOSE 8000

CMD ["/entrypoint"]