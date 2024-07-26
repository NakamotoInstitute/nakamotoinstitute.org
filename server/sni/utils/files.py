import hashlib
import os


def get_file_hash(filename, hash_function="sha256"):
    """Return the hash of a file."""
    h = hashlib.new(hash_function)

    with open(filename, "rb") as file:
        # Reading in chunks to manage memory for large files
        for chunk in iter(lambda: file.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()


def get_directory_hash(directory):
    sha256_hash = hashlib.sha256()
    for root, dirs, files in os.walk(directory):
        for file in sorted(files):
            filepath = os.path.join(root, file)
            file_hash = get_file_hash(filepath)
            sha256_hash.update(file_hash.encode("utf-8"))
            sha256_hash.update(
                filepath.encode("utf-8")
            )  # to ensure file paths are part of the hash
    return sha256_hash.hexdigest()


def split_filename(filename):
    return filename.split(".")
