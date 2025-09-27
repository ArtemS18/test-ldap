from fastapi import HTTPException, status


JWT_MISSING_TOKEN = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Missing token",
    headers={"WWW-Authenticate": "Bearer"},
)

JWT_BASE_EXEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

JWT_TOKEN_EXPIRED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has expired",
    headers={"WWW-Authenticate": "Bearer"},
)
JWT_BAD_CREDENSIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Bad token`s credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

JWT_DECODE_ERROR = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Decode error",
    headers={"WWW-Authenticate": "Bearer"},
)

REFRESH_TOKEN_NOT_FOUND = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Refresh token not found",
    headers={"WWW-Authenticate": "Bearer"},
)
ACCESS_TOKEN_NOT_FOUND = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Access token not found",
    headers={"WWW-Authenticate": "Bearer"},
)

BAD_CREDENSIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Bad credentials",
)

USER_NOT_FOUND = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User not found",
    headers={"WWW-Authenticate": "Bearer"},
)

REFRESH_TOKEN_NOT_FOUND = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Refresh token not found",
    headers={"WWW-Authenticate": "Bearer"},
)
ACCESS_TOKEN_NOT_FOUND = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Access token not found",
    headers={"WWW-Authenticate": "Bearer"},
)


FORBIDDEN_ROLE = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Not valid role"
)

NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
