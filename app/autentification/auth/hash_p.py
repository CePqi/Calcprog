import bcrypt

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pswd: bytes = password.encode()
    hash_p: bytes = bcrypt.hashpw(pswd, salt)
    return hash_p


def check_password(password: str, hash_psrd: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hash_psrd)