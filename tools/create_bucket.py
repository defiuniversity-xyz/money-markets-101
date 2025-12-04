#!/usr/bin/env python3
"""
Create Google Cloud Storage bucket for money markets media files.
"""

from google.cloud import storage
import os
import sys
from pathlib import Path

# Configuration
SCRIPT_DIR = Path(__file__).parent
GITBOOK_DIR = SCRIPT_DIR.parent
ROOT_DIR = GITBOOK_DIR.parent.parent
SERVICE_ACCOUNT_PATH = os.getenv(
    'GOOGLE_APPLICATION_CREDENTIALS',
    str(ROOT_DIR / "Keys" / "google-service-account.json")
)
BUCKET_NAME = os.getenv('GCS_BUCKET_NAME', 'money-markets-media')
PROJECT_ID = 'defi-university'
LOCATION = 'us-central1'

def create_bucket():
    """Create the GCS bucket if it doesn't exist"""
    # Verify service account file exists
    if not os.path.exists(SERVICE_ACCOUNT_PATH):
        print(f"ERROR: Service account file not found: {SERVICE_ACCOUNT_PATH}")
        print("Please set GOOGLE_APPLICATION_CREDENTIALS environment variable")
        sys.exit(1)
    
    # Set environment variable for Google Cloud authentication
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.abspath(SERVICE_ACCOUNT_PATH)
    
    try:
        storage_client = storage.Client(project=PROJECT_ID)
        
        # Check if bucket already exists
        try:
            bucket = storage_client.bucket(BUCKET_NAME)
            if bucket.exists():
                print(f"✅ Bucket '{BUCKET_NAME}' already exists")
                return True
        except Exception:
            pass
        
        # Create bucket
        print(f"Creating bucket: gs://{BUCKET_NAME}")
        bucket = storage_client.create_bucket(
            BUCKET_NAME,
            location=LOCATION
        )
        
        # Enable uniform bucket-level access
        bucket.iam_configuration.uniform_bucket_level_access_enabled = True
        bucket.patch()
        
        print(f"✅ Bucket created successfully: gs://{BUCKET_NAME}")
        print()
        print("⚠️  IMPORTANT: You still need to:")
        print("1. Configure public access:")
        print("   - Go to Google Cloud Console > Cloud Storage > Buckets")
        print("   - Click on the bucket > Permissions tab")
        print("   - Grant 'Storage Object Viewer' role to 'allUsers'")
        print()
        print("2. Configure CORS:")
        print("   - Go to bucket > Configuration tab")
        print("   - Add CORS configuration for GitBook domains")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create bucket: {e}")
        return False

if __name__ == "__main__":
    create_bucket()

