import hashlib


def get_file_hash(filename, hash_function="sha256"):
    """Return the hash of a file."""
    h = hashlib.new(hash_function)

    with open(filename, "rb") as file:
        # Reading in chunks to manage memory for large files
        for chunk in iter(lambda: file.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()
