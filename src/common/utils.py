from uuid import uuid4


def build_uui4_str():
    return str(uuid4().hex)


def public_dict(object_):
    return {k: v for k, v in vars(object_).items() if not k.startswith('_')}
