from uuid import uuid4


def build_uuid4_str() -> str:
    return str(uuid4().hex)


def public_dict(object_) -> dict:
    return {k: v for k, v in vars(object_).items() if not k.startswith('_')}
