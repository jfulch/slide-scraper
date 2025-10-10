#!/usr/bin/env python3
"""
Quick AI Study Guide Generator
Creates study guides from lecture text using AI analysis (faster version).
"""

import os
import sys
from pathlib import Path
import argparse

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

def create_study_guide(lecture_name: str):
    """Generate a study guide for a lecture using AI."""
    
    print(f"🎓 Generating study guide for: {lecture_name}")
    
    # Get the extracted text
    text_file = Path("output") / f"{lecture_name}_slides_text.txt"
    if not text_file.exists():
        print(f"❌ Text file not found: {text_file}")
        print("Run the OCR extraction first: python read_slides.py {lecture_name}")
        return
    
    # Read the lecture content
    content = text_file.read_text(encoding='utf-8')
    
    # Create AI prompt
    prompt = f"""
    You are an expert study guide creator. Analyze this CS572 Information Retrieval lecture content and create a comprehensive study guide.

    Lecture: {lecture_name}
    Content: {content}

    Create a study guide with the following sections:

    ## 📋 LECTURE OVERVIEW
    - Main topic and objectives
    - Key difficulty level
    
    ## 🎯 KEY CONCEPTS TO MASTER
    List 8-12 most important concepts from this lecture that students should memorize for exams.
    
    ## 🧠 MEMORY AIDS & STUDY TIPS
    Provide specific mnemonics, acronyms, or memory tricks for complex algorithms, formulas, or concepts.
    
    ## ❓ PRACTICE QUESTIONS
    Create 8-10 exam-style questions covering different difficulty levels:
    - Basic recall questions
    - Application problems  
    - Analysis questions
    
    ## 🔗 CONNECTIONS
    How do these concepts connect to other CS/Information Retrieval topics?
    
    ## 📚 STUDY STRATEGY
    Recommend specific study approach and time allocation for mastering this material.

    Focus on creating actionable, memorable study material that helps with exam preparation.
    """
    
    print("🤖 Analyzing lecture content with AI...")
    
    try:
        # Generate study guide
        response = ollama.generate(
            model='llama3.1:8b',
            prompt=prompt,
            options={
                'num_predict': 1000,  # Allow longer response
                'temperature': 0.7,   # Some creativity but focused
            }
        )
        
        study_guide_content = response['response']
        
        # Save the study guide
        output_dir = Path("study_guides")
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / f"{lecture_name}_study_guide.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# 🎓 {lecture_name.replace('_', ' ').title()} - Study Guide\n\n")
            f.write(study_guide_content)
        
        print(f"✅ Study guide created: {output_file}")
        
        # Also create a quick reference card
        quick_ref_file = output_dir / f"{lecture_name}_quick_reference.txt"
        
        quick_prompt = f"""
        Create a 1-page quick reference card for the {lecture_name} lecture.
        
        Content: {content[:2000]}...  # First 2000 chars for speed
        
        Format as a compact reference with:
        - Key terms and definitions (5-7 items)
        - Important formulas or algorithms (if any)
        - Essential facts to remember
        
        Keep it under 300 words for quick review.
        """
        
        print("📋 Creating quick reference card...")
        
        quick_response = ollama.generate(
            model='llama3.1:8b',
            prompt=quick_prompt,
            options={'num_predict': 300}
        )
        
        with open(quick_ref_file, 'w', encoding='utf-8') as f:
            f.write(f"# {lecture_name.replace('_', ' ').title()} - Quick Reference\n\n")
            f.write(quick_response['response'])
        
        print(f"📋 Quick reference created: {quick_ref_file}")
        
        return output_file, quick_ref_file
        
    except Exception as e:
        print(f"❌ Error generating study guide: {e}")
        return None

def main():
    """Main function."""
    
    if not OLLAMA_AVAILABLE:
        print("❌ Ollama not installed. Install with:")
        print("brew install ollama")
        print("pip install ollama")
        return
    
    parser = argparse.ArgumentParser(description="Quick AI Study Guide Generator")
    parser.add_argument("lecture", nargs='?', help="Lecture name (or --all)")
    parser.add_argument("--all", action="store_true", help="Process all lectures")
    
    args = parser.parse_args()
    
    if not args.lecture and not args.all:
        # Show available lectures
        output_dir = Path("output")
        if output_dir.exists():
            text_files = list(output_dir.glob("*_slides_text.txt"))
            lectures = [f.stem.replace("_slides_text", "") for f in text_files]
            
            print("📚 Available lectures:")
            for i, lecture in enumerate(lectures, 1):
                print(f"  {i}. {lecture}")
            
            print(f"\nUsage:")
            print(f"  python quick_study_guide.py <lecture_name>")
            print(f"  python quick_study_guide.py --all")
        return
    
    # Get lectures to process
    if args.all:
        output_dir = Path("output")
        text_files = list(output_dir.glob("*_slides_text.txt"))
        lectures = [f.stem.replace("_slides_text", "") for f in text_files]
    else:
        lectures = [args.lecture]
    
    print(f"🚀 Processing {len(lectures)} lecture(s)")
    
    successful = 0
    for lecture in lectures:
        try:
            result = create_study_guide(lecture)
            if result:
                successful += 1
                print(f"✅ Completed: {lecture}\n")
            else:
                print(f"❌ Failed: {lecture}\n")
        except KeyboardInterrupt:
            print(f"\n⏸️  Interrupted. Completed {successful}/{len(lectures)} lectures.")
            break
        except Exception as e:
            print(f"❌ Error processing {lecture}: {e}\n")
    
    print(f"🎉 Generated {successful} study guides!")
    if successful > 0:
        print(f"📁 Check the 'study_guides/' folder for your materials!")

if __name__ == "__main__":
    main()