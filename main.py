from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

import models
from database import engine
from routers import users, tasks

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Team Task Manager API",
    description="""
A real-world API for managing team tasks.

## How to use
1. **Register** at `/users/register`
2. **Login** at `/users/login` → copy your `access_token`
3. Click **Authorize** (top right), enter: `Bearer <your_token>`
4. All endpoints are now accessible!
    """,
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response   = await call_next(request)
    response.headers["X-Process-Time"] = f"{time.time() - start_time:.4f}s"
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."}
    )


app.include_router(users.router)
app.include_router(tasks.router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Task Manager API is running!", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
