#!/usr/bin/env python3
"""
Fix embed formatting in lesson files to match investor mindset format.
Adds blank line between audio and video embeds.
"""

from pathlib import Path
import re

# Configuration
SCRIPT_DIR = Path(__file__).parent
GITBOOK_DIR = SCRIPT_DIR.parent
LESSONS_DIR = GITBOOK_DIR / "content" / "lessons"

def fix_embed_formatting(lesson_file: Path) -> tuple[bool, str]:
    """
    Fix embed formatting to match investor mindset format.
    Changes: audio embed, blank line, video embed, blank line, content
    """
    # Read current content
    with open(lesson_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match two consecutive embed lines without blank line between
    # Matches: embed\nembed\n
    pattern = r'(\{% embed url="[^"]+" %\})\n(\{% embed url="[^"]+" %\})\n'
    
    # Replace with: embed\n\nembed\n
    replacement = r'\1\n\n\2\n'
    
    # Check if pattern exists
    if re.search(pattern, content):
        # Replace the pattern
        new_content = re.sub(pattern, replacement, content)
        
        # Write back to file
        with open(lesson_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, f"Fixed formatting in {lesson_file.name}"
    else:
        # Check if already correct (has blank line between)
        pattern_correct = r'(\{% embed url="[^"]+" %\})\n\n(\{% embed url="[^"]+" %\})\n'
        if re.search(pattern_correct, content):
            return True, f"Already correct format in {lesson_file.name}"
        else:
            return False, f"Could not find expected embed pattern in {lesson_file.name}"

def main():
    """Process all lesson files"""
    print("=" * 60)
    print("Fixing Embed Formatting in Lesson Files")
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
        success, message = fix_embed_formatting(lesson_file)
        
        if success:
            if "Already correct" in message:
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
    print(f"⏭️  Already correct: {skip_count}")
    print(f"❌ Failed: {fail_count}")
    print()

if __name__ == "__main__":
    main()

