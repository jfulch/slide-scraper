#!/usr/bin/env python3
"""
Batch processor for all lecture folders.
Automatically finds all lecture folders in slides/ and processes them with OCR.
"""

import os
import subprocess
import sys
from pathlib import Path

def get_lecture_folders():
    """Get all lecture folders in the slides directory."""
    slides_dir = Path("slides")
    if not slides_dir.exists():
        print("No slides directory found!")
        return []
    
    folders = []
    for item in slides_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            folders.append(item.name)
    
    return sorted(folders)

def process_lecture(lecture_name, output_format="txt"):
    """Process a single lecture folder."""
    print(f"\n{'='*60}")
    print(f"Processing: {lecture_name}")
    print(f"{'='*60}")
    
    try:
        cmd = [sys.executable, "read_slides.py", lecture_name, "--output-format", output_format]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Successfully processed {lecture_name}")
            return True
        else:
            print(f"❌ Error processing {lecture_name}:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error processing {lecture_name}: {e}")
        return False

def main():
    """Main batch processing function."""
    print("🎓 Batch OCR Processing for All Lectures")
    print("=" * 50)
    
    # Get all lecture folders
    lecture_folders = get_lecture_folders()
    
    if not lecture_folders:
        print("No lecture folders found in slides/")
        return
    
    print(f"Found {len(lecture_folders)} lecture folders:")
    for i, folder in enumerate(lecture_folders, 1):
        print(f"  {i}. {folder}")
    
    # Ask user for output format
    print("\nOutput format options:")
    print("  1. txt (fast, searchable text)")
    print("  2. pdf (formatted documents)")
    print("  3. docx (editable Word documents)")
    print("  4. all (txt + pdf + docx)")
    
    choice = input("\nEnter choice (1-4, default=1): ").strip()
    format_map = {"1": "txt", "2": "pdf", "3": "docx", "4": "all", "": "txt"}
    output_format = format_map.get(choice, "txt")
    
    print(f"\nProcessing all lectures with format: {output_format}")
    
    # Process all lectures
    successful = 0
    failed = 0
    
    for lecture in lecture_folders:
        if process_lecture(lecture, output_format):
            successful += 1
        else:
            failed += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"BATCH PROCESSING COMPLETE")
    print(f"{'='*60}")
    print(f"✅ Successfully processed: {successful} lectures")
    print(f"❌ Failed: {failed} lectures")
    print(f"📁 Output files saved to: {Path('output').absolute()}")
    
    if successful > 0:
        print(f"\n🎉 All your lecture materials are now ready for studying!")

if __name__ == "__main__":
    main()