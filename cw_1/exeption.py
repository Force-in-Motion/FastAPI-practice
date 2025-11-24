from fastapi import HTTPException, status


class DBExeption(Exception):


    not_found = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Book not found",
    )

    db_error = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Error Data Base",
    )