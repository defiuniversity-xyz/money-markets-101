#!/usr/bin/env python3
"""
Batch upload all audio and video files to Google Cloud Storage.
"""

import os
import sys
import re
from pathlib import Path
from upload_asset import upload_file, extract_lesson_number

# Paths
SCRIPT_DIR = Path(__file__).parent
GITBOOK_DIR = SCRIPT_DIR.parent
AUDIO_DIR = GITBOOK_DIR / "content" / "audio"
VIDEO_DIR = GITBOOK_DIR / "content" / "videos"

def format_lesson_slug(lesson_num):
    """Format lesson number as slug (e.g., 1 -> "lesson-01")"""
    return f"lesson-{lesson_num:02d}"

def upload_all_media():
    """Upload all audio and video files"""
    print("=" * 60)
    print("Uploading All Media Files to Google Cloud Storage")
    print("=" * 60)
    print()
    
    # Track uploads
    uploaded = []
    failed = []
    
    # Upload audio files
    print("📢 Uploading Audio Files...")
    print("-" * 60)
    audio_files = sorted(AUDIO_DIR.glob("*.m4a"))
    for audio_file in audio_files:
        lesson_num = extract_lesson_number(audio_file.name)
        if lesson_num:
            lesson_slug = format_lesson_slug(lesson_num)
            print(f"Uploading: {audio_file.name} → {lesson_slug}")
            result = upload_file(str(audio_file), lesson_slug)
            if result:
                uploaded.append((audio_file.name, lesson_slug, "audio"))
                print(f"  ✅ Success: {result}")
            else:
                failed.append((audio_file.name, lesson_slug, "audio"))
                print(f"  ❌ Failed")
        else:
            print(f"  ⚠️  Could not extract lesson number from: {audio_file.name}")
            failed.append((audio_file.name, None, "audio"))
        print()
    
    # Upload video files
    print("🎬 Uploading Video Files...")
    print("-" * 60)
    video_files = sorted(VIDEO_DIR.glob("*.mp4"))
    for video_file in video_files:
        lesson_num = extract_lesson_number(video_file.name)
        if lesson_num:
            lesson_slug = format_lesson_slug(lesson_num)
            print(f"Uploading: {video_file.name} → {lesson_slug}")
            result = upload_file(str(video_file), lesson_slug)
            if result:
                uploaded.append((video_file.name, lesson_slug, "video"))
                print(f"  ✅ Success: {result}")
            else:
                failed.append((video_file.name, lesson_slug, "video"))
                print(f"  ❌ Failed")
        else:
            print(f"  ⚠️  Could not extract lesson number from: {video_file.name}")
            failed.append((video_file.name, None, "video"))
        print()
    
    # Summary
    print("=" * 60)
    print("Upload Summary")
    print("=" * 60)
    print(f"✅ Successfully uploaded: {len(uploaded)} files")
    print(f"❌ Failed: {len(failed)} files")
    print()
    
    if uploaded:
        print("Uploaded files:")
        for filename, lesson_slug, media_type in uploaded:
            print(f"  ✅ {media_type}: {filename} → {lesson_slug}")
        print()
    
    if failed:
        print("Failed files:")
        for filename, lesson_slug, media_type in failed:
            print(f"  ❌ {media_type}: {filename}")
        print()
    
    return len(uploaded), len(failed)

if __name__ == "__main__":
    # Set service account path
    # From tools/: go up to gitbook dir, then up to ebook dir, then up to ebooks, then up to root, then into Keys
    service_account = os.getenv(
        'GOOGLE_APPLICATION_CREDENTIALS',
        str(GITBOOK_DIR.parent.parent.parent / "Keys" / "google-service-account.json")
    )
    
    if not os.path.exists(service_account):
        print(f"ERROR: Service account file not found: {service_account}")
        print("Please set GOOGLE_APPLICATION_CREDENTIALS environment variable")
        sys.exit(1)
    
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account
    print(f"Using service account: {service_account}")
    print()
    
    success, failed = upload_all_media()
    
    if failed > 0:
        sys.exit(1)
    else:
        print("🎉 All files uploaded successfully!")
        sys.exit(0)

