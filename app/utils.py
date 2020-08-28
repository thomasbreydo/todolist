from contextlib import contextmanager


def empty_input(*fields):
    for field in fields:
        if len(field) == 0:
            return True
    return False


def asbytes(string_or_bytes):
    try:
        return string_or_bytes.encode()
    except AttributeError:
        if isinstance(string_or_bytes, bytes):
            return string_or_bytes
        raise NotImplementedError(
            "asbytes is not implemented for types other than str and bytes")


@contextmanager
def ignore(error):
    try:
        yield
    except error:
        pass
