import shortuuid


def generate_uuid(alphabet, length):
    s = shortuuid.ShortUUID(alphabet=alphabet)
    return s.random(length)
