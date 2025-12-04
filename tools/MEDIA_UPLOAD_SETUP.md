# Money Markets GitBook Media Upload Setup

This guide explains how to upload audio and video files to Google Cloud Storage and integrate them into the GitBook lessons.

## Prerequisites

- Google Cloud account with project: `defi-university`
- Service account JSON file: `Keys/google-service-account.json`
- Python dependencies installed: `pip install -r tools/requirements.txt`

## Step 1: Create GCS Bucket

**IMPORTANT:** The bucket must be created before uploading files.

### Option A: Using Google Cloud Console (Recommended)

1. Log in to [Google Cloud Console](https://console.cloud.google.com)
2. Select project: **defi-university**
3. Navigate to **Cloud Storage** > **Buckets**
4. Click **Create bucket**
5. Configure:
   - **Name**: `money-markets-media` (must be globally unique)
   - **Location type**: Region (e.g., `us-central1`)
   - **Storage class**: Standard
   - **Access control**: Uniform (recommended)
6. Click **Create**

### Option B: Using gcloud CLI (After Authentication)

After authenticating (`gcloud auth login`), run:

```bash
gcloud storage buckets create gs://money-markets-media \
  --project=defi-university \
  --location=us-central1 \
  --uniform-bucket-level-access
```

## Step 2: Configure Public Access

1. Go to bucket > **Permissions** tab
2. Click **Grant Access**
3. Configure:
   - **New principals**: `allUsers`
   - **Role**: `Storage Object Viewer`
4. Click **Save**
5. Confirm the warning about making bucket publicly accessible

## Step 3: Configure CORS

1. In your bucket, go to **Configuration** tab
2. Scroll to **CORS configuration**
3. Click **Edit CORS configuration**
4. Paste this JSON configuration:

```json
[
  {
    "origin": ["https://docs.gitbook.com", "https://*.gitbook.io", "http://localhost:3000"],
    "method": ["GET", "HEAD"],
    "responseHeader": ["Content-Type", "ETag"],
    "maxAgeSeconds": 3600
  }
]
```

5. Click **Save**

Or use the command line (after authentication):

```bash
cd ebooks/money-markets-ebook/money-markets-gitbook/tools
gsutil cors set cors-config.json gs://money-markets-media
```

## Step 4: Grant Service Account Permissions

Grant the service account write permissions:

```bash
gsutil iam ch serviceAccount:defi-university-automation@defi-university.iam.gserviceaccount.com:roles/storage.objectAdmin gs://money-markets-media
```

## Step 5: Upload Media Files

Once the bucket is created and configured, upload all media files:

```bash
cd ebooks/money-markets-ebook/money-markets-gitbook/tools
python3 upload_all_media.py
```

This will upload:
- 12 audio files from `content/audio/` (`.m4a` files)
- 12 video files from `content/videos/` (`.mp4` files)

Files will be organized in GCS as:
- `money-markets-media/lesson-01/audio/lesson1 DeFi_Money_Markets_Monolithic_Versus_Modular_Risk.m4a`
- `money-markets-media/lesson-01/video/lesson1 DeFi__Banking_Without_a_Bank.mp4`
- (and similarly for lessons 02-12)

## Step 6: Add Embeds to Lesson Files

After uploading, add embed tags to all lesson files:

```bash
cd ebooks/money-markets-ebook/money-markets-gitbook/tools
python3 add_media_embeds.py
```

This will:
- Add audio embed at the top of each lesson
- Add video embed below audio (with blank line between)
- Generate properly URL-encoded GCS URLs
- Match investor mindset format exactly

## Step 7: Verify and Push

1. Verify embeds appear correctly in lesson files
2. Commit and push to GitHub

## Verification

After uploading:

1. **Check GCS Console**: Verify files appear in correct folders
2. **Test URLs**: Open each URL in browser to verify public access
3. **Test Playback**: Verify audio/video files play correctly
4. **Test GitBook**: Verify embeds display correctly in GitBook preview

## Troubleshooting

### Upload Fails with "Bucket does not exist"
- Ensure bucket `money-markets-media` has been created
- Verify bucket name matches in scripts (default: `money-markets-media`)

### Upload Fails with "Permission Denied"
- Check service account has `Storage Object Admin` role on bucket
- Verify service account JSON file path is correct

### Files Don't Show in GitBook
- Check CORS is configured: `gsutil cors get gs://money-markets-media`
- Verify URLs are properly encoded (spaces, special characters)
- Check bucket has public access configured

## Scripts Reference

- `upload_asset.py` - Upload individual files to GCS
- `upload_all_media.py` - Batch upload all audio and video files
- `add_media_embeds.py` - Add embed tags to lesson files
- `fix_url_encoding.py` - Fix URL encoding in existing embeds
- `fix_embed_formatting.py` - Fix embed formatting (add blank lines)
- `create_bucket.py` - Attempt to create bucket programmatically

## File Structure

```
money-markets-gitbook/
├── content/
│   ├── audio/          (12 .m4a audio files - excluded from git)
│   ├── videos/         (12 .mp4 video files - excluded from git)
│   └── lessons/        (12 lesson markdown files - with embeds)
└── tools/
    ├── upload_asset.py
    ├── upload_all_media.py
    ├── add_media_embeds.py
    ├── cors-config.json
    └── requirements.txt
```

## Notes

- Audio files use GitBook's `{% embed %}` syntax which creates a playable audio player (not a download link)
- Audio embed appears first, then video embed, then lesson content
- All URLs are properly URL-encoded for browser compatibility
- CORS configuration is critical for GitBook to access media files

