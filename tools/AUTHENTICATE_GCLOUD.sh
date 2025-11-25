#!/bin/bash
# Google Cloud Authentication Commands
# Copy and paste these commands into your terminal

# Step 1: Authenticate with Google Cloud
gcloud auth login

# Step 2: Set the project
gcloud config set project defi-university

# Step 3: Verify authentication
gcloud auth list

# Step 4: Create the bucket
gcloud storage buckets create gs://money-markets-gitbook-images \
  --project=defi-university \
  --location=US \
  --uniform-bucket-level-access

# Step 5: Make bucket publicly readable
gcloud storage buckets add-iam-policy-binding gs://money-markets-gitbook-images \
  --member=allUsers \
  --role=roles/storage.objectViewer

# Step 6: Verify bucket was created
gcloud storage buckets describe gs://money-markets-gitbook-images

