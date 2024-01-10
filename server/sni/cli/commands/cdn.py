import fnmatch
import os
from pathlib import Path

import boto3
import typer
from typing_extensions import Annotated

from sni.config import settings

EXCLUSION_PATTERNS = [
    "code/*",
    "cryptomises/*.mp3",
    "docs/*.pdf",
    "docs/*.epub",
    "docs/*.mobi",
    "sni-docs.zip",
]

client = boto3.client(
    "s3",
    endpoint_url=settings.CDN_ENDPOINT_URL,
    aws_access_key_id=settings.CDN_ACCESS_KEY,
    aws_secret_access_key=settings.CDN_SECRET_KEY,
)

app = typer.Typer(help="Manage static files")


def get_r2_files(bucket_name):
    """List all files in the R2 bucket."""
    response = client.list_objects_v2(Bucket=bucket_name)
    return [item["Key"] for item in response.get("Contents", [])]


def upload_file(file_path, bucket_name, file_key):
    """Upload a file to R2."""
    client.upload_file(Filename=str(file_path), Bucket=bucket_name, Key=file_key)
    print(f"Uploaded {file_key}")


def delete_file(bucket_name, file_key):
    """Delete a file from R2."""
    client.delete_object(Bucket=bucket_name, Key=file_key)
    print(f"Deleted {file_key}")


def list_files_recursive(directory):
    """Recursively list all files in the directory."""
    for path in Path(directory).rglob("*"):
        if path.is_file():
            yield path


def sync_directory(local_directory, bucket_name, exclusion_patterns=[]):
    local_files = {
        str(f.relative_to(local_directory)): f
        for f in list_files_recursive(local_directory)
    }
    r2_files = set(get_r2_files(bucket_name))

    # Upload or update files
    for file_key, file_path in local_files.items():
        if file_key not in r2_files or os.path.getmtime(file_path) > os.path.getctime(
            file_path
        ):
            upload_file(file_path, bucket_name, file_key)

    # Delete files that are not in local directory or excluded
    for file_key in r2_files:
        if file_key not in local_files:
            if not any(
                fnmatch.fnmatch(file_key, pattern) for pattern in exclusion_patterns
            ):
                delete_file(bucket_name, file_key)
            else:
                print(f"Skipped deletion for excluded file {file_key}")


@app.command()
def sync(
    force: Annotated[
        bool, typer.Option(help="Force cdn sync even if in development")
    ] = False,
):
    if settings.ENVIRONMENT == "development" and not force:
        print("Skipping sync in development environment without force flag.")
        return

    necessary_values = {
        "CDN_ENDPOINT_URL": settings.CDN_ENDPOINT_URL,
        "CDN_ACCESS_KEY": settings.CDN_ACCESS_KEY,
        "CDN_SECRET_KEY": settings.CDN_SECRET_KEY,
        "CDN_BUCKET_NAME": settings.CDN_BUCKET_NAME,
    }

    missing_values = [key for key, value in necessary_values.items() if value is None]
    if missing_values:
        missing_values_str = ", ".join(missing_values)
        raise ValueError(
            f"Missing necessary configuration values: {missing_values_str}"
        )

    sync_directory(
        "static", settings.CDN_BUCKET_NAME, exclusion_patterns=EXCLUSION_PATTERNS
    )


if __name__ == "__main__":
    app()
