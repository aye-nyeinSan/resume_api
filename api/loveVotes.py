from fastapi import APIRouter,Depends 
from google.cloud import firestore
from pyrate_limiter import Duration, Limiter, Rate
from fastapi_limiter.depends import RateLimiter

from config.firestoreDb import db as firestoreDB

router = APIRouter(prefix="/resume", tags=['love-votes'])
stats_ref = firestoreDB.collection('stats').document('resume')


@router.post("/love-votes", dependencies=[Depends(RateLimiter(limiter=Limiter(Rate(2, Duration.SECOND * 5))))])
def add_love():
    stats_ref.set({"total_love_count": firestore.Increment(1)},merge=True)
    return {"message": "loved"}

