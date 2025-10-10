#!/usr/bin/env python3
"""
Content-Focused Study Material Generator
Extracts actual lecture content and creates focused study materials for memorization.

This creates:
- Key facts and definitions to memorize
- Algorithm step-by-step breakdowns  
- Formula explanations with examples
- Important diagrams/concepts described in detail
- Flash cards for memorization
- Condensed "cheat sheets" with essential information
"""

import os
import sys
from pathlib import Path
import argparse
import re

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

class StudyMaterialExtractor:
    def __init__(self):
        self.study_dir = Path("study_materials")
        self.study_dir.mkdir(exist_ok=True)
    
    def extract_study_content(self, lecture_name: str):
        """Extract actual content for studying from lecture text."""
        
        print(f"📚 Extracting study content for: {lecture_name}")
        
        # Get the extracted text
        text_file = Path("output") / f"{lecture_name}_slides_text.txt"
        if not text_file.exists():
            print(f"❌ Text file not found: {text_file}")
            return None
        
        content = text_file.read_text(encoding='utf-8')
        
        # Create comprehensive extraction prompt
        extraction_prompt = f"""
        You are extracting the essential content from this CS572 Information Retrieval lecture for a student to study and memorize.

        Lecture: {lecture_name}
        Content: {content}

        Extract and organize the ACTUAL CONTENT into these sections:

        ## DEFINITIONS & KEY TERMS
        List every important term, concept, or algorithm mentioned with clear, memorizable definitions. 
        Format: **Term**: Definition
        
        ## ALGORITHMS & PROCESSES  
        For each algorithm/process mentioned, provide:
        - Step-by-step breakdown
        - When/why it's used
        - Key characteristics
        
        ## FORMULAS & CALCULATIONS
        Extract any mathematical formulas, equations, or calculations with:
        - The formula itself
        - What each variable means
        - Example calculation if possible
        
        ## IMPORTANT FACTS & NUMBERS
        List specific facts, statistics, comparisons, or numerical data mentioned
        
        ## CORE CONCEPTS EXPLAINED
        Explain the main concepts in simple, clear language that a student can memorize
        
        ## EXAMPLES & APPLICATIONS
        Real-world examples or applications mentioned in the slides
        
        Focus on extracting actual information content, not study advice. Give me the facts, definitions, and knowledge to memorize.
        """
        
        print("🧠 Extracting key content with AI...")
        
        try:
            response = ollama.generate(
                model='llama3.1:8b',
                prompt=extraction_prompt,
                options={
                    'num_predict': 1500,
                    'temperature': 0.3,  # Lower temperature for more factual extraction
                }
            )
            
            extracted_content = response['response']
            
            # Save the main study material
            main_file = self.study_dir / f"{lecture_name}_study_content.md"
            with open(main_file, 'w', encoding='utf-8') as f:
                f.write(f"# 📖 {lecture_name.replace('_', ' ').title()} - Study Content\n\n")
                f.write(extracted_content)
            
            print(f"📖 Main study material: {main_file}")
            
            # Create flash cards
            self.create_flashcards(lecture_name, content)
            
            # Create a condensed cheat sheet
            self.create_cheat_sheet(lecture_name, extracted_content)
            
            return main_file
            
        except Exception as e:
            print(f"❌ Error extracting content: {e}")
            return None
    
    def create_flashcards(self, lecture_name: str, content: str):
        """Create flashcard-style Q&A for memorization."""
        
        flashcard_prompt = f"""
        Create flashcards for memorization from this lecture content.

        Content: {content[:3000]}...  # Limit for speed

        Create 15-20 flashcard pairs in this format:
        
        Q: [Question about a specific fact, definition, or concept]
        A: [Concise, memorizable answer]
        
        ---
        
        Focus on:
        - Key definitions and what they mean
        - Algorithm names and their purposes  
        - Important facts and numbers
        - How things work or are calculated
        - Differences between concepts
        
        Make questions specific and answers short but complete.
        """
        
        print("🃏 Creating flashcards...")
        
        try:
            response = ollama.generate(
                model='llama3.1:8b',
                prompt=flashcard_prompt,
                options={'num_predict': 800, 'temperature': 0.4}
            )
            
            flashcard_file = self.study_dir / f"{lecture_name}_flashcards.txt"
            with open(flashcard_file, 'w', encoding='utf-8') as f:
                f.write(f"# 🃏 {lecture_name.replace('_', ' ').title()} - Flashcards\n\n")
                f.write(response['response'])
            
            print(f"🃏 Flashcards created: {flashcard_file}")
            
        except Exception as e:
            print(f"⚠️  Could not create flashcards: {e}")
    
    def create_cheat_sheet(self, lecture_name: str, extracted_content: str):
        """Create a 1-page condensed cheat sheet."""
        
        cheat_sheet_prompt = f"""
        Create a condensed 1-page cheat sheet from this extracted content.

        Content: {extracted_content}

        Format as a compact reference with:
        
        ## KEY TERMS (most important definitions)
        ## ALGORITHMS (names and what they do)
        ## FORMULAS (if any)
        ## MUST-KNOW FACTS
        ## QUICK REFERENCE
        
        Keep it under 400 words. Focus on what a student needs to know for an exam.
        Make it scannable and easy to review quickly.
        """
        
        print("📋 Creating cheat sheet...")
        
        try:
            response = ollama.generate(
                model='llama3.1:8b',
                prompt=cheat_sheet_prompt,
                options={'num_predict': 400, 'temperature': 0.3}
            )
            
            cheat_file = self.study_dir / f"{lecture_name}_cheat_sheet.txt"
            with open(cheat_file, 'w', encoding='utf-8') as f:
                f.write(f"# 📋 {lecture_name.replace('_', ' ').title()} - Cheat Sheet\n\n")
                f.write(response['response'])
            
            print(f"📋 Cheat sheet created: {cheat_file}")
            
        except Exception as e:
            print(f"⚠️  Could not create cheat sheet: {e}")
    
    def create_summary_document(self, lecture_name: str, content: str):
        """Create a comprehensive summary with all key information."""
        
        summary_prompt = f"""
        Create a comprehensive study summary that contains all the important information a student needs to know from this lecture.

        Lecture: {lecture_name}
        Content: {content}

        Include:
        
        ## WHAT THIS LECTURE COVERS
        Brief overview of the main topic
        
        ## EVERYTHING YOU NEED TO KNOW
        - All key concepts explained clearly
        - All algorithms and how they work
        - All formulas and what they calculate
        - All important facts and details
        - All examples and applications
        
        ## MEMORIZATION CHECKLIST
        List of specific items to memorize for exams
        
        Write this as if you're teaching someone who needs to master this material completely.
        Include all the actual content, not just study tips.
        """
        
        print("📚 Creating comprehensive summary...")
        
        try:
            response = ollama.generate(
                model='llama3.1:8b',
                prompt=summary_prompt,
                options={
                    'num_predict': 1200,
                    'temperature': 0.2  # Very factual
                }
            )
            
            summary_file = self.study_dir / f"{lecture_name}_complete_summary.md"
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(f"# 📚 {lecture_name.replace('_', ' ').title()} - Complete Study Summary\n\n")
                f.write(response['response'])
            
            print(f"📚 Complete summary: {summary_file}")
            
            return summary_file
            
        except Exception as e:
            print(f"❌ Error creating summary: {e}")
            return None

def main():
    """Main function."""
    
    if not OLLAMA_AVAILABLE:
        print("❌ Ollama not installed. Install with:")
        print("brew install ollama && pip install ollama")
        return
    
    parser = argparse.ArgumentParser(
        description="Extract actual study content from lectures",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python study_extractor.py querying
  python study_extractor.py --all
  python study_extractor.py se-basics --summary-only
        """
    )
    
    parser.add_argument("lecture", nargs='?', help="Lecture name")
    parser.add_argument("--all", action="store_true", help="Process all lectures")
    parser.add_argument("--summary-only", action="store_true", help="Create comprehensive summary only")
    
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
            
            print(f"\nUsage examples:")
            print(f"  python study_extractor.py querying")
            print(f"  python study_extractor.py --all")
        return
    
    extractor = StudyMaterialExtractor()
    
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
            if args.summary_only:
                content = Path("output") / f"{lecture}_slides_text.txt"
                if content.exists():
                    content_text = content.read_text(encoding='utf-8')
                    result = extractor.create_summary_document(lecture, content_text)
                else:
                    print(f"❌ No text file for {lecture}")
                    continue
            else:
                result = extractor.extract_study_content(lecture)
            
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
    
    print(f"🎉 Created study materials for {successful} lectures!")
    if successful > 0:
        print(f"📁 Check the 'study_materials/' folder for:")
        print(f"   📖 *_study_content.md - Main study materials")
        print(f"   🃏 *_flashcards.txt - Memorization flashcards") 
        print(f"   📋 *_cheat_sheet.txt - Quick reference")
        print(f"   📚 *_complete_summary.md - Comprehensive summaries")

if __name__ == "__main__":
    main()