#!/usr/bin/env python3
"""
Fix URL encoding in embed tags for audio/video files.
Encodes special characters in filenames to make URLs work properly in GitBook.
"""

from pathlib import Path
import re
from urllib.parse import quote

# Configuration
SCRIPT_DIR = Path(__file__).parent
GITBOOK_DIR = SCRIPT_DIR.parent
LESSONS_DIR = GITBOOK_DIR / "content" / "lessons"
BUCKET_NAME = "money-markets-media"

def encode_url_in_embed(match):
    """Encode the URL in an embed tag"""
    full_url = match.group(1)
    
    # Split URL into parts
    parts = full_url.split('/')
    
    # Find the filename (last part after the last '/')
    if len(parts) > 0:
        filename = parts[-1]
        # Encode the filename (but keep / characters)
        encoded_filename = quote(filename, safe='')
        # Reconstruct URL with encoded filename
        encoded_url = '/'.join(parts[:-1]) + '/' + encoded_filename
        return f'{{% embed url="{encoded_url}" %}}'
    
    return match.group(0)

def fix_url_encoding(lesson_file: Path) -> tuple[bool, str]:
    """
    Fix URL encoding in embed tags.
    """
    # Read current content
    with open(lesson_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match embed tags with money-markets-media URLs
    pattern = r'\{% embed url="(https://storage\.googleapis\.com/money-markets-media/[^"]+)" %\}'
    
    # Check if pattern exists
    matches = re.findall(pattern, content)
    if matches:
        # Replace all embed URLs with encoded versions
        new_content = re.sub(pattern, encode_url_in_embed, content)
        
        # Only write if something changed
        if new_content != content:
            with open(lesson_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, f"Fixed URL encoding in {lesson_file.name}"
        else:
            return True, f"URLs already encoded in {lesson_file.name}"
    else:
        return False, f"No money-markets-media embeds found in {lesson_file.name}"

def main():
    """Process all lesson files"""
    print("=" * 60)
    print("Fixing URL Encoding in Embed Tags")
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
        success, message = fix_url_encoding(lesson_file)
        
        if success:
            if "already encoded" in message:
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
    print(f"✅ Successfully fixed: {success_count}")
    print(f"⏭️  Already encoded: {skip_count}")
    print(f"❌ Failed: {fail_count}")
    print()

if __name__ == "__main__":
    main()

