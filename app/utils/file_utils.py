import os

def save_upload_tmp(data: bytes, suffix: str = "") -> str:
    import tempfile
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(data)
    tmp.flush()
    tmp.close()
    return tmp.name
