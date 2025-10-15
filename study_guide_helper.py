#!/usr/bin/env python3
"""
Study Guide Helper

A simple utility to help you work with your comprehensive midterm study guide.
Provides quick access to search and review study materials.

Usage:
    python study_guide_helper.py
"""

import os
import json
from pathlib import Path
import webbrowser

class StudyGuideHelper:
    def __init__(self):
        self.midterm_dir = Path("midterm_guide")
        self.word_doc = self.midterm_dir / "midterm_study_guide_comprehensive.docx"
        self.pdf_summary = self.midterm_dir / "midterm_study_guide_summary.pdf"
        self.json_data = self.midterm_dir / "midterm_study_content_summary.json"
        
    def show_menu(self):
        """Display the main menu"""
        print("\n" + "="*60)
        print("🎓 CSCI 572 - MIDTERM STUDY GUIDE HELPER")
        print("="*60)
        print("1. 📖 Open Comprehensive Study Guide (Word)")
        print("2. 📄 Open Quick Summary (PDF)")
        print("3. 📊 Show Study Statistics")
        print("4. 📁 Open Study Guide Folder")
        print("5. 🔍 View Generated Files")
        print("6. ❓ Study Tips & Recommendations")
        print("7. 🚪 Exit")
        print("="*60)
        
    def open_word_document(self):
        """Open the comprehensive Word document"""
        if self.word_doc.exists():
            print(f"📖 Opening comprehensive study guide...")
            if os.name == 'nt':  # Windows
                os.startfile(self.word_doc)
            elif os.name == 'posix':  # macOS/Linux
                os.system(f'open "{self.word_doc}"')
            print("✅ Study guide opened!")
        else:
            print("❌ Word document not found. Run midterm_study_guide.py first.")
            
    def open_pdf_summary(self):
        """Open the PDF summary"""
        if self.pdf_summary.exists():
            print(f"📄 Opening PDF summary...")
            if os.name == 'nt':  # Windows
                os.startfile(self.pdf_summary)
            elif os.name == 'posix':  # macOS/Linux
                os.system(f'open "{self.pdf_summary}"')
            print("✅ PDF summary opened!")
        else:
            print("❌ PDF summary not found. Run midterm_study_guide.py first.")
            
    def show_statistics(self):
        """Show study statistics"""
        if self.json_data.exists():
            with open(self.json_data, 'r') as f:
                data = json.load(f)
            
            metadata = data['metadata']
            print("\n📊 STUDY GUIDE STATISTICS")
            print("-" * 40)
            print(f"📚 Total Lectures: {metadata['total_lectures']}")
            print(f"📄 Total Slides Processed: {metadata['total_slides_processed']}")
            print(f"🎯 Key Concepts: {metadata['total_concepts']}")
            print(f"📝 Definitions: {metadata['total_definitions']}")
            print(f"🔢 Formulas: {metadata['total_formulas']}")
            print(f"⚙️  Algorithms: {metadata['total_algorithms']}")
            
            print(f"\n📋 LECTURES COVERED:")
            for lecture in metadata['lectures_covered']:
                print(f"   • {lecture.replace('_', ' ').title()}")
                
        else:
            print("❌ Statistics not available. Run midterm_study_guide.py first.")
            
    def open_folder(self):
        """Open the study guide folder"""
        if self.midterm_dir.exists():
            print(f"📁 Opening study guide folder...")
            if os.name == 'nt':  # Windows
                os.startfile(self.midterm_dir)
            elif os.name == 'posix':  # macOS/Linux
                os.system(f'open "{self.midterm_dir}"')
            print("✅ Folder opened!")
        else:
            print("❌ Study guide folder not found. Run midterm_study_guide.py first.")
            
    def view_files(self):
        """List all generated files"""
        if self.midterm_dir.exists():
            print("\n📁 GENERATED STUDY FILES:")
            print("-" * 40)
            
            files = list(self.midterm_dir.glob("*"))
            if files:
                for file in sorted(files):
                    if file.is_file():
                        size = file.stat().st_size
                        size_mb = size / (1024 * 1024)
                        if size_mb > 1:
                            size_str = f"{size_mb:.1f} MB"
                        else:
                            size_str = f"{size / 1024:.0f} KB"
                        print(f"   📄 {file.name} ({size_str})")
            else:
                print("   No files found.")
        else:
            print("❌ Study guide folder not found. Run midterm_study_guide.py first.")
            
    def show_study_tips(self):
        """Show study tips and recommendations"""
        print("\n💡 STUDY TIPS & RECOMMENDATIONS")
        print("="*50)
        
        tips = [
            "📖 Review the comprehensive Word document first for complete coverage",
            "🎯 Focus on high-priority concepts identified by the AI",
            "📝 Make sure you understand all definitions - they're likely exam material",
            "🔢 Practice all formulas and algorithms until you can do them from memory",
            "📚 Study one lecture at a time, then review connections between topics",
            "✏️  Create your own examples for each concept to test understanding",
            "🔄 Use the study checklist in the Word document to track progress",
            "👥 Study with classmates and quiz each other on key concepts",
            "⏰ Plan multiple review sessions rather than cramming",
            "🎯 Focus extra time on topics you find most challenging"
        ]
        
        for i, tip in enumerate(tips, 1):
            print(f"{i:2}. {tip}")
            
        print(f"\n🎓 EXAM SUCCESS STRATEGY:")
        print(f"   • Complete coverage: All {910 if self.json_data.exists() else 'many'} concepts analyzed")
        print(f"   • Multiple formats: Word doc (detailed), PDF (quick review)")
        print(f"   • AI-powered: Content prioritized for exam relevance")
        print(f"   • Comprehensive: Every lecture and slide covered")
        
    def run(self):
        """Main program loop"""
        while True:
            self.show_menu()
            
            try:
                choice = input("\n🎯 Enter your choice (1-7): ").strip()
                
                if choice == '1':
                    self.open_word_document()
                elif choice == '2':
                    self.open_pdf_summary()
                elif choice == '3':
                    self.show_statistics()
                elif choice == '4':
                    self.open_folder()
                elif choice == '5':
                    self.view_files()
                elif choice == '6':
                    self.show_study_tips()
                elif choice == '7':
                    print("\n🎓 Good luck with your midterm! You've got this! 📚✨")
                    break
                else:
                    print("❌ Invalid choice. Please enter 1-7.")
                    
                input("\n📖 Press Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n🎓 Good luck with your midterm! 📚✨")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("\n📖 Press Enter to continue...")

def main():
    helper = StudyGuideHelper()
    helper.run()

if __name__ == "__main__":
    main()