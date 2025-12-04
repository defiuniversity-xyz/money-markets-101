# Money Markets Media Bucket Setup Instructions

**Status:** The bucket `money-markets-media` needs to be created before uploading files.

## Quick Setup Commands

After authenticating with Google Cloud (`gcloud auth login`), run these commands:

### 1. Create Bucket
```bash
gcloud storage buckets create gs://money-markets-media \
  --project=defi-university \
  --location=us-central1 \
  --uniform-bucket-level-access
```

### 2. Configure Public Access
```bash
gsutil iam ch allUsers:objectViewer gs://money-markets-media
```

### 3. Configure CORS
```bash
cd ebooks/money-markets-ebook/money-markets-gitbook/tools
gsutil cors set cors-config.json gs://money-markets-media
```

### 4. Grant Service Account Permissions
```bash
gsutil iam ch serviceAccount:defi-university-automation@defi-university.iam.gserviceaccount.com:roles/storage.objectAdmin gs://money-markets-media
```

### 5. Verify Configuration
```bash
# Check CORS
gsutil cors get gs://money-markets-media

# Check permissions
gsutil iam get gs://money-markets-media | grep -A 5 "allUsers\|bindings"
```

After completing these steps, you can proceed with uploading media files.

