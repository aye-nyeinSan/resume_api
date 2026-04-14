from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.visitors import router as visitors_router
from api.loveVotes import router as lovevotes_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", #for dev
                   "https://rubiayenyeinsan.vercel.app/"], #for production
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(visitors_router)
app.include_router(lovevotes_router)
