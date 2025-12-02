from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app import problems
from app import evaluator
from app.auth.router import router as auth_router
from app.dashboard import router as dashboard_router
# import debugpy

# debugpy.listen(("0.0.0.0", 5678))
# print(" Debugger is waiting... Attach VS Code NOW")

# Base.metadata.create_all(bind=engine)
import os

if os.getenv("RUN_MIGRATIONS", "false").lower() == "true":
    Base.metadata.create_all(bind=engine)


app = FastAPI(title="Drill & Practice API", version="1.0.0")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://drill-practice-system.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(problems.router)
app.include_router(evaluator.router)
app.include_router(auth_router)
app.include_router(dashboard_router)


@app.get("/")
def root():
    return {"message": "Backend is running"}
