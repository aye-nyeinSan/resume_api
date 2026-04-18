# Resume API

FastAPI backend for my personal resume site ([rubiayenyeinsan.vercel.app](https://rubiayenyeinsan.vercel.app/)). Tracks unique visitors and "love" votes, backed by Firestore and deployed to Cloud Run via Cloud Build.

Part of the [Cloud Resume Challenge](https://cloudresumechallenge.dev/) on GCP.

## Architecture

```
Client ──► FastAPI (Cloud Run) ──► Firestore

GitHub ──(push to main)──► Cloud Build ──► Artifact Registry ──► Cloud Run
```

- **Runtime:** FastAPI app on Cloud Run, reading/writing to Firestore.
- **CI/CD:** Push to `main` triggers Cloud Build, which builds a Docker image, pushes it to Artifact Registry, deploys to Cloud Run, and cleans up old images.
- **Infra:** Terraform provisions APIs, Artifact Registry, IAM bindings, and Cloud Build triggers.

## Endpoints

All routes are prefixed with `/resume` and rate-limited to 2 requests per 5 seconds.

| Method | Path               | Description                                   |
| ------ | ------------------ | --------------------------------------------- |
| GET    | `/resume/visits`         | List all tracked visitors and total count    |
| POST   | `/resume/visits`         | Record the caller's IP as a visitor          |
| GET    | `/resume/visitor-status` | Aggregate stats (total visitors, love count) |
| POST   | `/resume/love-votes`     | Increment the love counter                   |

## Project structure

```
.
├── main.py                   # FastAPI app + CORS
├── api/
│   ├── visitors.py           # /resume/visits, /resume/visitor-status
│   └── loveVotes.py          # /resume/love-votes
├── config/firestoreDb.py     # Firestore client
├── Dockerfile
├── docker-compose.yml        # local dev (builds from source)
├── docker-compose-prod.yml   # pulls the deployed image from AR
├── cloudBuild.yaml           # Cloud Build pipeline
├── gcp_setup.sh              # one-time GCP bootstrap
└── terraform/                # infra as code
```

## Local development

Prerequisites: Python 3.12, Docker, a GCP service account with Firestore access saved as `serviceAccountKey.json`.

```bash
# 1. Install deps
pip install -r requirements.txt

# 2. Run with Docker (recommended — matches prod)
docker compose up --build

# Or run directly
fastapi dev main.py
```

The API is available at `http://localhost:8000`. Interactive docs at `/docs`.

## Deployment

Pushing to `main` automatically builds and deploys via Cloud Build. Manual setup:

```bash
# One-time: enable APIs, create TF state bucket
./gcp_setup.sh

# Connect the GitHub repo in Cloud Build → Triggers → Manage repositories

# Provision infra
cd terraform && terraform init && terraform apply
```

Changes under `terraform/**` on `main` trigger a separate `terraform apply` build.

## Tech stack

- **API:** FastAPI, Pydantic
- **Database:** Firestore
- **Rate limiting:** pyrate_limiter + fastapi-limiter
- **Container:** Docker (python:3.12-slim)
- **CI/CD:** Cloud Build, Artifact Registry, Cloud Run
- **IaC:** Terraform (state in GCS)
- **Region:** `asia-southeast1`


<img width="2444" height="1086" alt="image" src="https://github.com/user-attachments/assets/c6b74b4f-9568-4708-b6cc-f77f7ec4ce1b" />
