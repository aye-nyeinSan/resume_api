from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Request
from google.cloud import firestore

from config.firestoreDb import db as firestoreDB

router = APIRouter(prefix="/resume", tags=['resume'])
visitors_ref = firestoreDB.collection('visitors')
stats_ref = firestoreDB.collection('stats').document('resume')


@router.get("/visits")
def track_visit():
    docs = visitors_ref.stream()
    visitors = [doc.to_dict() for doc in docs]
    return {"total": len(visitors), "visitors": visitors}


@router.post("/visits")
def add_visitor(request: Request) -> dict:
    print("Request:", request)
    ip = request.headers.get("X-Forwarded-For", request.client.host if
                             request.client else "unknown")
    doc = visitors_ref.document(ip).get()
    is_new = not doc.exists

    if is_new:
        stats_ref.set({"total_visitors": firestore.Increment(1)}, merge=True)
       # Add data to firstore collection
        visitors_ref.document(ip).set({
            "ip": ip,
            "visited_at": firestore.SERVER_TIMESTAMP,
            "visit_count": firestore.Increment(1),
            "expired_at": datetime.now(timezone.utc) + timedelta(hours=24)

        }, merge=True)
    return {"message": "successfully added visitor to DB", "is_new": is_new}


@router.get("/visitor-status")
def get_stats():
    doc = stats_ref.get()
    return doc.to_dict() if doc.exists else {"total_visitors": 0, "total_love_count": 0}
