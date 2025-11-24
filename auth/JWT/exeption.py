from fastapi import HTTPException, status


class DBExeption(Exception):

    inactive = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User inactive",
    )

    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid login or password",
    )

    not_found = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not found",
    )

    token_invalid = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token type",
    )
