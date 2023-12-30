import logging
import os
import sys
import time

import psycopg

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def wait_for_postgres():
    dbname = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    suggest_unrecoverable_after = 30
    start = time.time()

    while True:
        try:
            psycopg.connect(
                dbname=dbname, user=user, password=password, host=host, port=port
            )
            logging.info("PostgreSQL is available")
            break
        except psycopg.OperationalError as error:
            logging.info("Waiting for PostgreSQL to become available...")
            if time.time() - start > suggest_unrecoverable_after:
                logging.error(f"This is taking longer than expected: {error}")
                sys.exit(1)
            time.sleep(1)


if __name__ == "__main__":
    wait_for_postgres()
