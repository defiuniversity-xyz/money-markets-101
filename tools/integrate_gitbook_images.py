#!/usr/bin/env python3
"""
Integrate generated infographic images into money markets gitbook markdown files.
Reads asset specifications and inserts image references at appropriate locations using GCS URLs.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class MoneyMarketsImageIntegrator:
    """Integrates images into money markets gitbook markdown files"""
    
    def __init__(self, base_dir: Optional[Path] = None, bucket_name: str = "money-markets-gitbook-images"):
        """Initialize integrator with paths"""
        if base_dir is None:
            self.base_dir = Path(__file__).parent.parent
        else:
            self.base_dir = Path(base_dir)
        
        # Update paths for money markets
        self.specs_path = self.base_dir.parent.parent.parent / 'assets' / 'infographics' / 'scripts' / 'money_markets_asset_specs.json'
        self.images_source = self.base_dir.parent.parent.parent / 'assets' / 'infographics' / 'output' / 'money-markets'
        self.lessons_dir = self.base_dir / 'content' / 'lessons'
        self.exercises_dir = self.base_dir / 'content' / 'exercises'
        self.bucket_name = bucket_name
        self.gcs_base_url = f"https://storage.googleapis.com/{bucket_name}"
        
        # Load asset specifications
        with open(self.specs_path, 'r') as f:
            self.specs = json.load(f)
    
    def find_insertion_point(self, content: str, placement: str, asset_title: str) -> Optional[int]:
        """
        Find insertion point in markdown content based on placement description.
        
        Args:
            content: Full markdown content
            placement: Placement description from specs (e.g., "After 'The Two Architectural Philosophies' section")
            asset_title: Asset title for context
        
        Returns:
            Index where image should be inserted, or None if not found
        """
        # Extract section name from placement
        match = re.search(r"['\"]([^'\"]+)['\"]", placement)
        if match:
            section_name = match.group(1)
        else:
            # Try to extract from placement text
            section_name = placement.replace("After", "").replace("section", "").strip().strip("'\"")
        
        if not section_name:
            return None
        
        # Try to find the section header
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('#') and section_name.lower() in line.lower():
                header_level = len(line) - len(line.lstrip('#'))
                
                # Look for next section
                for j in range(i + 1, len(lines)):
                    next_line = lines[j]
                    if next_line.strip() and next_line.startswith('#'):
                        next_level = len(next_line) - len(next_line.lstrip('#'))
                        if next_level <= header_level:
                            return '\n'.join(lines[:j]).__len__() if j > 0 else None
                
                # Insert after a couple of paragraphs
                insert_idx = i + 1
                paragraph_count = 0
                for j in range(i + 1, min(i + 20, len(lines))):
                    if lines[j].strip() and not lines[j].startswith('#'):
                        if not lines[j].strip().startswith('-') and not lines[j].strip().startswith('*'):
                            paragraph_count += 1
                            if paragraph_count >= 2:
                                insert_idx = j + 1
                                break
                
                return '\n'.join(lines[:insert_idx]).__len__() + (1 if insert_idx < len(lines) else 0)
        
        # Fallback: search for section name in content
        pattern = re.compile(re.escape(section_name), re.IGNORECASE)
        matches = list(pattern.finditer(content))
        if matches:
            match_pos = matches[0].end()
            next_newline = content.find('\n\n', match_pos)
            if next_newline != -1:
                return next_newline + 2
            return match_pos
        
        return None
    
    def get_actual_image_filename(self, asset_id: str, lesson_id: Optional[str] = None, exercise_id: Optional[str] = None) -> Optional[Path]:
        """Get actual image filename from source directory"""
        if lesson_id:
            source_dir = self.images_source / 'lessons' / lesson_id
        elif exercise_id:
            source_dir = self.images_source / 'exercises' / exercise_id
        else:
            return None
        
        # Find file matching asset_id
        pattern = f"{asset_id}_*.png"
        matches = list(source_dir.glob(pattern))
        if matches:
            return matches[0]
        return None
    
    def get_gcs_url(self, asset_id: str, lesson_id: Optional[str] = None, exercise_id: Optional[str] = None) -> Optional[str]:
        """Get GCS URL for an asset"""
        image_file = self.get_actual_image_filename(asset_id, lesson_id, exercise_id)
        if not image_file:
            return None
        
        # Get relative path from money-markets directory
        relative_path = image_file.relative_to(self.images_source)
        # Convert to GCS URL
        return f"{self.gcs_base_url}/{relative_path.as_posix()}"
    
    def insert_image_reference(self, content: str, insertion_point: int, gcs_url: str, asset_title: str) -> str:
        """Insert image markdown reference at specified point"""
        image_markdown = f"\n\n![{asset_title}]({gcs_url})\n\n"
        return content[:insertion_point] + image_markdown + content[insertion_point:]
    
    def replace_old_image_references(self, content: str, asset_id: str, gcs_url: str, asset_title: str) -> Tuple[str, bool]:
        """Replace existing image references (local or old GCS URLs) with new GCS URL"""
        # Pattern to match image markdown with this asset_id
        pattern = re.compile(rf"!\[.*?\]\((https?://storage\.googleapis\.com/[^/]+/.*?{re.escape(asset_id)}[^\)]*\.png|images/.*?{re.escape(asset_id)}[^\)]*\.png)\)", re.IGNORECASE)
        
        match = pattern.search(content)
        if match:
            old_image_markdown = match.group(0)
            if gcs_url not in old_image_markdown:
                new_image_markdown = f"![{asset_title}]({gcs_url})"
                content = content.replace(old_image_markdown, new_image_markdown)
                return content, True
        return content, False
    
    def integrate_lesson(self, lesson_id: str, dry_run: bool = False) -> Dict:
        """Integrate images for a specific lesson"""
        lesson_num = int(lesson_id.replace('lesson_', ''))
        
        # Find actual lesson file
        matches = list(self.lessons_dir.glob(f"lesson-{lesson_num:02d}-*.md"))
        if not matches:
            return {'error': f"Lesson file not found for {lesson_id}"}
        
        lesson_file = matches[0]
        
        # Get lesson assets
        lesson_data = self.specs.get('lessons', {}).get(lesson_id)
        if not lesson_data:
            return {'error': f"No assets found for {lesson_id}"}
        
        # Read lesson content
        with open(lesson_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        results = []
        
        # Process each asset
        for asset in lesson_data['assets']:
            asset_id = asset['asset_id']
            asset_title = asset['title']
            placement = asset.get('placement', '')
            
            # Get GCS URL
            gcs_url = self.get_gcs_url(asset_id, lesson_id=lesson_id)
            if not gcs_url:
                results.append({
                    'asset_id': asset_id,
                    'status': 'error',
                    'reason': 'Image file not found in source'
                })
                continue
            
            # Try to replace existing reference
            content, replaced = self.replace_old_image_references(content, asset_id, gcs_url, asset_title)
            if replaced:
                results.append({
                    'asset_id': asset_id,
                    'status': 'replaced',
                    'gcs_url': gcs_url
                })
                continue
            
            # Check if already exists with correct URL
            if gcs_url in content:
                results.append({
                    'asset_id': asset_id,
                    'status': 'skipped',
                    'reason': 'Already exists with correct GCS URL'
                })
                continue
            
            # Find insertion point
            insertion_point = self.find_insertion_point(content, placement, asset_title)
            
            if insertion_point is None:
                # Try keyword-based search
                keywords = re.findall(r'\b\w+\b', placement.lower())
                for keyword in keywords:
                    if len(keyword) > 4:
                        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
                        matches = list(pattern.finditer(content))
                        if matches:
                            match_pos = matches[0].end()
                            next_para = content.find('\n\n', match_pos)
                            insertion_point = next_para + 2 if next_para != -1 else match_pos
                            break
            
            if insertion_point is None:
                results.append({
                    'asset_id': asset_id,
                    'status': 'error',
                    'reason': f'Could not find insertion point for: {placement}'
                })
                continue
            
            # Insert image
            if not dry_run:
                content = self.insert_image_reference(content, insertion_point, gcs_url, asset_title)
                results.append({
                    'asset_id': asset_id,
                    'status': 'inserted',
                    'insertion_point': insertion_point,
                    'gcs_url': gcs_url
                })
            else:
                results.append({
                    'asset_id': asset_id,
                    'status': 'would_insert',
                    'insertion_point': insertion_point,
                    'gcs_url': gcs_url
                })
        
        # Write updated content
        if not dry_run and content != original_content:
            with open(lesson_file, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return {
            'lesson_id': lesson_id,
            'lesson_file': str(lesson_file),
            'results': results
        }
    
    def integrate_exercise(self, exercise_id: str, dry_run: bool = False) -> Dict:
        """Integrate images for a specific exercise"""
        exercise_num = int(exercise_id.replace('exercise_', ''))
        
        # Find actual exercise file
        matches = list(self.exercises_dir.glob(f"exercise-{exercise_num:02d}-*.md"))
        if not matches:
            return {'error': f"Exercise file not found for {exercise_id}"}
        
        exercise_file = matches[0]
        
        # Get exercise assets
        exercise_data = self.specs.get('exercises', {}).get(exercise_id)
        if not exercise_data:
            return {'error': f"No assets found for {exercise_id}"}
        
        # Read exercise content
        with open(exercise_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        results = []
        
        # Process each asset
        for asset in exercise_data['assets']:
            asset_id = asset['asset_id']
            asset_title = asset['title']
            placement = asset.get('placement', '')
            
            # Get GCS URL
            gcs_url = self.get_gcs_url(asset_id, exercise_id=exercise_id)
            if not gcs_url:
                results.append({
                    'asset_id': asset_id,
                    'status': 'error',
                    'reason': 'Image file not found in source'
                })
                continue
            
            # Try to replace existing reference
            content, replaced = self.replace_old_image_references(content, asset_id, gcs_url, asset_title)
            if replaced:
                results.append({
                    'asset_id': asset_id,
                    'status': 'replaced',
                    'gcs_url': gcs_url
                })
                continue
            
            # Check if already exists
            if gcs_url in content:
                results.append({
                    'asset_id': asset_id,
                    'status': 'skipped',
                    'reason': 'Already exists with correct GCS URL'
                })
                continue
            
            # Find insertion point
            insertion_point = self.find_insertion_point(content, placement, asset_title)
            
            if insertion_point is None:
                keywords = re.findall(r'\b\w+\b', placement.lower())
                for keyword in keywords:
                    if len(keyword) > 4:
                        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
                        matches = list(pattern.finditer(content))
                        if matches:
                            match_pos = matches[0].end()
                            next_para = content.find('\n\n', match_pos)
                            insertion_point = next_para + 2 if next_para != -1 else match_pos
                            break
            
            if insertion_point is None:
                results.append({
                    'asset_id': asset_id,
                    'status': 'error',
                    'reason': f'Could not find insertion point for: {placement}'
                })
                continue
            
            # Insert image
            if not dry_run:
                content = self.insert_image_reference(content, insertion_point, gcs_url, asset_title)
                results.append({
                    'asset_id': asset_id,
                    'status': 'inserted',
                    'insertion_point': insertion_point,
                    'gcs_url': gcs_url
                })
            else:
                results.append({
                    'asset_id': asset_id,
                    'status': 'would_insert',
                    'insertion_point': insertion_point,
                    'gcs_url': gcs_url
                })
        
        # Write updated content
        if not dry_run and content != original_content:
            with open(exercise_file, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return {
            'exercise_id': exercise_id,
            'exercise_file': str(exercise_file),
            'results': results
        }
    
    def integrate_all(self, dry_run: bool = False) -> Dict:
        """Integrate images for all lessons and exercises"""
        results = {
            'lessons': [],
            'exercises': []
        }
        
        # Process lessons
        for lesson_id in sorted(self.specs.get('lessons', {}).keys()):
            result = self.integrate_lesson(lesson_id, dry_run=dry_run)
            results['lessons'].append(result)
        
        # Process exercises
        for exercise_id in sorted(self.specs.get('exercises', {}).keys()):
            result = self.integrate_exercise(exercise_id, dry_run=dry_run)
            results['exercises'].append(result)
        
        return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Integrate money markets images into gitbook markdown files')
    parser.add_argument('--lesson', help='Integrate specific lesson (e.g., lesson_01)')
    parser.add_argument('--exercise', help='Integrate specific exercise (e.g., exercise_01)')
    parser.add_argument('--all', action='store_true', help='Integrate all lessons and exercises')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--bucket', default='money-markets-gitbook-images', help='GCS bucket name')
    
    args = parser.parse_args()
    
    integrator = MoneyMarketsImageIntegrator(bucket_name=args.bucket)
    
    if args.all:
        results = integrator.integrate_all(dry_run=args.dry_run)
        print(f"\n{'DRY RUN: ' if args.dry_run else ''}Integration complete!")
        print(f"Lessons processed: {len(results['lessons'])}")
        print(f"Exercises processed: {len(results['exercises'])}")
    elif args.lesson:
        result = integrator.integrate_lesson(args.lesson, dry_run=args.dry_run)
        print(json.dumps(result, indent=2))
    elif args.exercise:
        result = integrator.integrate_exercise(args.exercise, dry_run=args.dry_run)
        print(json.dumps(result, indent=2))
    else:
        print("Usage:")
        print("  Integrate all: python integrate_gitbook_images.py --all")
        print("  Integrate lesson: python integrate_gitbook_images.py --lesson lesson_01")
        print("  Integrate exercise: python integrate_gitbook_images.py --exercise exercise_01")
        print("  Dry run: python integrate_gitbook_images.py --all --dry-run")

