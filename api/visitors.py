from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Request, Depends, HTTPException, Header, status
from google.cloud import firestore
from pyrate_limiter import Duration, Limiter, Rate
from fastapi_limiter.depends import RateLimiter
from config.firestoreDb import db as firestoreDB
import os

router = APIRouter(prefix="/resume", tags=['resume'])
visitors_ref = firestoreDB.collection('visitors')
stats_ref = firestoreDB.collection('stats').document('resume')


@router.post("/visits", dependencies=[Depends(RateLimiter(limiter=Limiter(Rate(2, Duration.SECOND * 5))))])
def add_visitor(request: Request) -> dict:
    
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


@router.get("/visitor-status", dependencies=[Depends(RateLimiter(limiter=Limiter(Rate(2, Duration.SECOND * 5))))])
def get_stats():
    try:
        doc = stats_ref.get()
        if not doc.exists:
            return {"total_visitors": 0, "total_love_count": 0}

        return doc.to_dict()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not retrieve statistics from the database."
        ) from e


CRON_SECRET = os.getenv("CRON_SECRET")

@router.delete("/visitors/cleanup")
async def cleanup_visitors(x_cron_secret: str = Header(None)):
    
    if x_cron_secret != CRON_SECRET:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )

    try:
       
        now = datetime.now(timezone.utc)
        docs = firestoreDB.collection('visitors').where(
            'expired_at', '<=', now).stream()

       
        batch = firestoreDB.batch()
        deleted_count = 0

        for doc in docs:
            batch.delete(doc.reference)
            deleted_count += 1
            if deleted_count % 500 == 0:
                batch.commit()
                batch = firestoreDB.batch()

        batch.commit()
        return {"status": "success", "deleted_records": deleted_count}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
