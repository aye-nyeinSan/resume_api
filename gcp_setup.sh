#!/bin/sh
# One-time bootstrap before running Terraform.
# Terraform manages everything else (cloudbuild, run, artifactregistry APIs,
# Artifact Registry repo, IAM bindings, Cloud Build trigger).

set -e

PROJECT_ID=$(gcloud config get-value project)
REGION="asia-southeast1"
STATE_BUCKET="${PROJECT_ID}-tf-state"

# 1. Enable the APIs Terraform itself needs
gcloud services enable \
  cloudresourcemanager.googleapis.com \
  iam.googleapis.com \
  storage.googleapis.com

# 2. Create GCS bucket for Terraform state (versioned)
if ! gcloud storage buckets describe "gs://${STATE_BUCKET}" >/dev/null 2>&1; then
  gcloud storage buckets create "gs://${STATE_BUCKET}" \
    --location="${REGION}" \
    --uniform-bucket-level-access
  gcloud storage buckets update "gs://${STATE_BUCKET}" --versioning
fi

echo "Bootstrap complete."
echo "Next steps:"
echo "  1. In GCP Console, connect the GitHub repo: Cloud Build > Triggers > Connect Repository"
echo "  2. cd terraform && terraform init && terraform apply"
