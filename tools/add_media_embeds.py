#!/usr/bin/env python3
"""
Add audio and video embed tags to the top of each lesson file.
"""

import re
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import quote

# Configuration
SCRIPT_DIR = Path(__file__).parent
GITBOOK_DIR = SCRIPT_DIR.parent
LESSONS_DIR = GITBOOK_DIR / "content" / "lessons"
AUDIO_DIR = GITBOOK_DIR / "content" / "audio"
VIDEO_DIR = GITBOOK_DIR / "content" / "videos"
BUCKET_NAME = "money-markets-media"

def extract_lesson_number(filename: str) -> Optional[int]:
    """Extract lesson number from filename (e.g., 'lesson-01-...' -> 1)"""
    match = re.search(r'lesson-(\d+)', filename, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None

def find_media_file(lesson_num: int, media_dir: Path, extension: str) -> Optional[str]:
    """Find media file for a lesson number"""
    # Try both "lesson1" and "lesson01" patterns
    patterns = [
        f"lesson{lesson_num} ",
        f"lesson{lesson_num:02d} ",
        f"lesson{lesson_num}_",
        f"lesson{lesson_num:02d}_",
    ]
    
    files = list(media_dir.glob(f"*{extension}"))
    for file in files:
        filename = file.name
        for pattern in patterns:
            if filename.startswith(pattern):
                return filename
    
    return None

def generate_gcs_url(lesson_num: int, filename: str, media_type: str) -> str:
    """Generate GCS URL for a media file with proper URL encoding"""
    lesson_slug = f"lesson-{lesson_num:02d}"
    folder = "audio" if media_type == "audio" else "video"
    # URL-encode the filename to handle special characters (spaces, $, =, etc.)
    encoded_filename = quote(filename, safe='')
    return f"https://storage.googleapis.com/{BUCKET_NAME}/{lesson_slug}/{folder}/{encoded_filename}"

def has_existing_embeds(content: str) -> bool:
    """Check if file already has embed tags at the top"""
    # Check for embed syntax at the beginning
    lines = content.split('\n')
    if len(lines) > 0 and '{% embed' in lines[0]:
        return True
    if len(lines) > 1 and '{% embed' in lines[1]:
        return True
    return False

def add_embeds_to_lesson(lesson_file: Path) -> Tuple[bool, str]:
    """
    Add audio and video embed tags to the top of a lesson file.
    Returns (success, message)
    """
    lesson_num = extract_lesson_number(lesson_file.name)
    if lesson_num is None:
        return False, f"Could not extract lesson number from {lesson_file.name}"
    
    # Read current content
    with open(lesson_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if embeds already exist
    if has_existing_embeds(content):
        return True, f"Embeds already exist in {lesson_file.name}"
    
    # Find audio and video files
    audio_filename = find_media_file(lesson_num, AUDIO_DIR, ".m4a")
    video_filename = find_media_file(lesson_num, VIDEO_DIR, ".mp4")
    
    if not audio_filename and not video_filename:
        return False, f"No media files found for lesson {lesson_num}"
    
    # Generate embed tags
    embeds = []
    if audio_filename:
        audio_url = generate_gcs_url(lesson_num, audio_filename, "audio")
        embeds.append(f'{{% embed url="{audio_url}" %}}')
    
    if video_filename:
        video_url = generate_gcs_url(lesson_num, video_filename, "video")
        embeds.append(f'{{% embed url="{video_url}" %}}')
    
    if not embeds:
        return False, f"No embed tags generated for lesson {lesson_num}"
    
    # Add embeds at the top with blank lines between (matching investor mindset format)
    # Format: audio embed, blank line, video embed, blank line, content
    if len(embeds) == 2:
        embed_block = embeds[0] + '\n\n' + embeds[1] + '\n\n'
    else:
        embed_block = '\n\n'.join(embeds) + '\n\n'
    new_content = embed_block + content
    
    # Write back to file
    with open(lesson_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    media_list = []
    if audio_filename:
        media_list.append(f"audio: {audio_filename}")
    if video_filename:
        media_list.append(f"video: {video_filename}")
    
    return True, f"Added embeds to {lesson_file.name} ({', '.join(media_list)})"

def main():
    """Process all lesson files"""
    print("=" * 60)
    print("Adding Media Embeds to Lesson Files")
    print("=" * 60)
    print()
    
    lesson_files = sorted(LESSONS_DIR.glob("lesson-*.md"))
    if not lesson_files:
        print("No lesson files found!")
        return
    
    success_count = 0
    skip_count = 0
    fail_count = 0
    
    for lesson_file in lesson_files:
        print(f"Processing: {lesson_file.name}")
        success, message = add_embeds_to_lesson(lesson_file)
        
        if success:
            if "already exist" in message:
                print(f"  ⏭️  {message}")
                skip_count += 1
            else:
                print(f"  ✅ {message}")
                success_count += 1
        else:
            print(f"  ❌ {message}")
            fail_count += 1
        print()
    
    # Summary
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"✅ Successfully added embeds: {success_count}")
    print(f"⏭️  Skipped (already exist): {skip_count}")
    print(f"❌ Failed: {fail_count}")
    print()

if __name__ == "__main__":
    main()

