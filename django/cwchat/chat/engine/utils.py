import uuid


def new_uuid():
    """
    生成UUID
    """
    uuid_str = str(uuid.uuid4())
    uuid_str = uuid_str.replace("-", "")
    return uuid_str
