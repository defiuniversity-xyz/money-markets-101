# Google Cloud Storage Setup for Money Markets GitBook

## Step 1: Create GCS Bucket

The bucket `money-markets-gitbook-images` needs to be created manually before uploading images.

### Option A: Using Google Cloud Console (Recommended)

1. Go to: https://console.cloud.google.com/storage
2. Select project: `defi-university`
3. Click "Create Bucket"
4. Bucket name: `money-markets-gitbook-images`
5. Location type: `Region` → `us-central1` (or any US region)
6. Access control: `Uniform` (for uniform bucket-level access)
7. Click "Create"

### Option B: Using gcloud CLI

```bash
gcloud storage buckets create gs://money-markets-gitbook-images \
  --project=defi-university \
  --location=US \
  --uniform-bucket-level-access
```

### Step 2: Make Bucket Public (for image URLs)

```bash
gcloud storage buckets add-iam-policy-binding gs://money-markets-gitbook-images \
  --member=allUsers \
  --role=roles/storage.objectViewer
```

Or via Console:
1. Click on the bucket
2. Go to "Permissions" tab
3. Click "Grant Access"
4. Add principal: `allUsers`
5. Role: `Storage Object Viewer`
6. Save

## Step 3: Upload Images

Once the bucket is created and configured for public access:

```bash
cd tools
python3 upload_images_to_gcs.py
```

This will upload all 70 images from `assets/infographics/output/money-markets/` to the bucket.

## Step 4: Integrate Images into Markdown

After images are uploaded:

```bash
python3 integrate_gitbook_images.py --all
```

This will add GCS URLs to all lesson and exercise markdown files.

