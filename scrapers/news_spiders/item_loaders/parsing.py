def lowercase_and_strip(value):
    if not value:
        return value

    return value.strip().lower()


def split(value):
    if not value:
        return value

    return value.split(",")


def to_int(value):
    return int(float(value))
