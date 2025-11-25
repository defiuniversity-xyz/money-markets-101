#!/usr/bin/env python3
"""
Upload all money markets GitBook images to Google Cloud Storage.
Mirrors the folder structure: lessons/lesson_XX/ and exercises/exercise_XX/
"""

from google.cloud import storage
import os
import mimetypes
from pathlib import Path

# Configuration
SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent.parent.parent.parent  # Go up from tools/ to "Testimonials Insert"
DEFAULT_SERVICE_ACCOUNT = BASE_DIR / 'Keys' / 'google-service-account.json'

SERVICE_ACCOUNT_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', str(DEFAULT_SERVICE_ACCOUNT))
BUCKET_NAME = os.getenv('GCS_BUCKET_NAME', 'money-markets-gitbook-images')
PROJECT_ID = 'defi-university'

def upload_images():
    """Upload all images from assets/infographics/output/money-markets/ to GCS"""
    
    # Verify service account file exists
    service_account_abs = os.path.abspath(SERVICE_ACCOUNT_PATH)
    if not os.path.exists(service_account_abs):
        # Try alternative paths
        alt_paths = [
            str(DEFAULT_SERVICE_ACCOUNT),
            str(BASE_DIR / 'Keys' / 'google-service-account.json'),
            os.path.expanduser('~/Keys/google-service-account.json'),
        ]
        found = False
        for alt_path in alt_paths:
            if os.path.exists(alt_path):
                service_account_abs = os.path.abspath(alt_path)
                found = True
                break
        
        if not found:
            print(f"ERROR: Service account file not found: {SERVICE_ACCOUNT_PATH}")
            print("Tried alternative paths:", alt_paths)
            print("Please set GOOGLE_APPLICATION_CREDENTIALS environment variable")
            return False
    
    # Set environment variable for Google Cloud authentication
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account_abs
    
    # Setup Google Cloud Storage client
    try:
        storage_client = storage.Client(project=PROJECT_ID)
        # Check if bucket exists
        bucket = storage_client.bucket(BUCKET_NAME)
        if not bucket.exists():
            print(f"Bucket '{BUCKET_NAME}' does not exist.")
            print(f"Please create it manually using:")
            print(f"  gcloud storage buckets create gs://{BUCKET_NAME} --project={PROJECT_ID} --location=US")
            print(f"Or ensure the service account has storage.buckets.create permission.")
            return False
        print(f"✓ Using existing bucket: {BUCKET_NAME}")
    except Exception as e:
        print(f"ERROR: Failed to connect to Google Cloud Storage: {e}")
        return False
    
    # Find all images
    script_dir = Path(__file__).parent
    gitbook_dir = script_dir.parent
    # Navigate to assets/infographics/output/money-markets
    images_dir = gitbook_dir.parent.parent.parent / "assets" / "infographics" / "output" / "money-markets"
    
    if not images_dir.exists():
        print(f"ERROR: Images directory not found: {images_dir}")
        return False
    
    # Find all PNG files
    image_files = list(images_dir.rglob("*.png"))
    
    if not image_files:
        print(f"No PNG files found in {images_dir}")
        return False
    
    print(f"Found {len(image_files)} images to upload")
    print(f"Uploading to: gs://{BUCKET_NAME}/")
    print("=" * 60)
    
    uploaded = []
    failed = []
    
    for image_file in sorted(image_files):
        # Get relative path from money-markets directory
        relative_path = image_file.relative_to(images_dir)
        
        # Create GCS object key (mirror folder structure)
        # Structure: lessons/lesson_XX/asset.png or exercises/exercise_XX/asset.png
        object_key = relative_path.as_posix()
        
        # Determine MIME type
        mime_type, _ = mimetypes.guess_type(str(image_file))
        if mime_type is None:
            mime_type = 'image/png'
        
        try:
            print(f"Uploading: {relative_path} → {object_key}")
            
            blob = bucket.blob(object_key)
            blob.content_type = mime_type
            blob.upload_from_filename(str(image_file))
            
            # Note: With uniform bucket-level access, objects are automatically public
            # if the bucket IAM policy grants allUsers access (already configured)
            # No need to call make_public() - it would fail with uniform access
            
            url = f"https://storage.googleapis.com/{BUCKET_NAME}/{object_key}"
            uploaded.append((str(relative_path), url))
            print(f"  ✓ Success: {url}")
            
        except Exception as e:
            print(f"  ✗ Failed: {e}")
            failed.append(str(relative_path))
    
    print("=" * 60)
    print(f"\nUpload Summary:")
    print(f"  ✅ Successfully uploaded: {len(uploaded)} images")
    print(f"  ❌ Failed: {len(failed)} images")
    
    if failed:
        print(f"\nFailed files:")
        for file in failed:
            print(f"  - {file}")
    else:
        print(f"\nAll images uploaded successfully! GCS Base URL: https://storage.googleapis.com/{BUCKET_NAME}/")
    
    return len(failed) == 0

if __name__ == "__main__":
    success = upload_images()
    exit(0 if success else 1)

