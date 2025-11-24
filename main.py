
from fastapi import FastAPI
from auth.Base.base_auth import router as auth_router
from auth.JWT.jwt_auth import router as jwt_router
from cw_1.api import router as cw_1

app = FastAPI(prefix="/auth")

app.include_router(auth_router)
app.include_router(jwt_router)
app.include_router(cw_1)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8000, reload=True)






































