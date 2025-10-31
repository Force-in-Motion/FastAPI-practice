from fastapi import FastAPI
from auth.base_auth import router as auth_router

app = FastAPI()
app.include_router(auth_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8000, reload=True)





































