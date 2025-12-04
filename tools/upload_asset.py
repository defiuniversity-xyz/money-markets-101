#!/usr/bin/env python3
"""
Upload media assets to Google Cloud Storage for GitBook embedding.
Based on the decoupled architecture strategy from publishing context.
Uses existing Google Cloud service account for authentication.
"""

from google.cloud import storage
import sys
import mimetypes
import os
import re
from pathlib import Path

# Configuration
# Service account JSON file path (relative to project root)
# From tools/upload_asset.py: go up to gitbook dir, then up to ebooks, then up to root, then into Keys
SCRIPT_DIR = Path(__file__).parent
GITBOOK_DIR = SCRIPT_DIR.parent
# From tools/: go up to gitbook dir, then up to ebook dir, then up to ebooks, then up to root, then into Keys
ROOT_DIR = GITBOOK_DIR.parent.parent.parent
SERVICE_ACCOUNT_PATH = os.getenv(
    'GOOGLE_APPLICATION_CREDENTIALS',
    str(ROOT_DIR / "Keys" / "google-service-account.json")
)
BUCKET_NAME = os.getenv('GCS_BUCKET_NAME', 'money-markets-media')
PROJECT_ID = 'defi-university'

def extract_lesson_number(filename):
    """Extract lesson number from filename"""
    match = re.search(r'lesson(\d+)', filename, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None

def upload_file(file_path, lesson_slug=None):
    """
    Upload a file to Google Cloud Storage and return the GitBook embed syntax.
    
    Args:
        file_path: Path to the file to upload
        lesson_slug: Optional lesson number (e.g., "lesson-01") for organization
    """
    # Verify service account file exists
    if not os.path.exists(SERVICE_ACCOUNT_PATH):
        print(f"ERROR: Service account file not found: {SERVICE_ACCOUNT_PATH}")
        print("Please set GOOGLE_APPLICATION_CREDENTIALS environment variable or ensure")
        print("Keys/google-service-account.json exists relative to project root")
        return None
    
    # Set environment variable for Google Cloud authentication
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.abspath(SERVICE_ACCOUNT_PATH)
    
    # 1. Setup Google Cloud Storage client
    try:
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
    except Exception as e:
        print(f"ERROR: Failed to connect to Google Cloud Storage: {e}")
        print(f"Project: {PROJECT_ID}")
        print(f"Bucket: {BUCKET_NAME}")
        print(f"Service Account: {SERVICE_ACCOUNT_PATH}")
        return None
    
    # 2. Prepare file metadata
    file_path_obj = Path(file_path)
    filename = file_path_obj.name
    mime_type, _ = mimetypes.guess_type(file_path)
    
    if mime_type is None:
        mime_type = 'application/octet-stream'
    
    # 3. Determine file type and folder organization
    if "video" in mime_type:
        folder = "video"
    elif "audio" in mime_type:
        folder = "audio"
    elif "image" in mime_type:
        folder = "images"
    else:
        folder = "files"
    
    # 4. Auto-detect lesson number from filename if not provided
    if lesson_slug is None:
        lesson_num = extract_lesson_number(filename)
        if lesson_num:
            lesson_slug = f"lesson-{lesson_num:02d}"
        else:
            lesson_slug = "general"
    
    # 5. Generate object key (path in GCS)
    object_key = f"{lesson_slug}/{folder}/{filename}"
    
    # 6. Upload with critical headers
    print(f"Uploading {filename} to {object_key}...")
    try:
        blob = bucket.blob(object_key)
        blob.content_type = mime_type  # CRITICAL for playback
        blob.upload_from_filename(file_path)
        
        # Note: Public access is configured at bucket level (uniform bucket-level access)
        # No need to call make_public() - files are automatically public due to bucket IAM policy
        
        print(f"✓ Upload successful!")
    except Exception as e:
        print(f"✗ Upload failed: {e}")
        return None
    
    # 7. Generate GitBook syntax based on type
    # GCS public URL format: https://storage.googleapis.com/BUCKET_NAME/path/to/file
    full_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{object_key}"
    
    print("\n" + "="*60)
    print("COPY TO MARKDOWN:")
    print("="*60)
    
    if "video" in mime_type or "audio" in mime_type:
        embed_syntax = f'{{% embed url="{full_url}" %}}'
        print(embed_syntax)
    elif "image" in mime_type:
        alt_text = filename.replace('_', ' ').replace('-', ' ').replace('.png', '').replace('.jpg', '').replace('.jpeg', '')
        markdown_syntax = f'![{alt_text}]({full_url})'
        print(markdown_syntax)
    else:
        link_syntax = f'[{filename}]({full_url})'
        print(link_syntax)
    
    print("="*60 + "\n")
    
    return full_url

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python upload_asset.py <file_path> [lesson_slug]")
        print("\nExample:")
        print("  python upload_asset.py ../content/audio/lesson1-audio.m4a")
        print("  python upload_asset.py ../content/videos/lesson1-video.mp4 lesson-01")
        print("\nEnvironment Variables:")
        print("  GOOGLE_APPLICATION_CREDENTIALS: Path to service account JSON (optional)")
        print("  GCS_BUCKET_NAME: Bucket name (default: money-markets-media)")
        sys.exit(1)
    
    file_path = sys.argv[1]
    lesson_slug = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}")
        sys.exit(1)
    
    upload_file(file_path, lesson_slug)

