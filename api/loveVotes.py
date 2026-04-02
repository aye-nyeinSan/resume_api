from fastapi import APIRouter, Request
from config.firestoreDb import db as firestoreDB
from google.cloud import firestore

router = APIRouter(prefix="/resume", tags=['love-votes'])
stats_ref = firestoreDB.collection('stats').document('resume')


@router.post("/love-votes")
def add_love(request: Request):
    stats_ref.set({"total_love_count": firestore.Increment(1)},merge=True)
    return {"message": "loved"}

