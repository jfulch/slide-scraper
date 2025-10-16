#!/usr/bin/env python3
"""
Quick Q&A Demo

A simple demo of the course Q&A system to show how it works.
"""

from course_qa_system import CourseQASystem

def demo_qa_system():
    """Demonstrate the Q&A system with sample questions"""
    print("🎓 CS572 Course Q&A System Demo")
    print("=" * 50)
    
    # Initialize system
    qa_system = CourseQASystem()
    
    # Build content database
    print("📚 Loading course content...")
    has_content = qa_system.extract_text_from_files()
    
    if not has_content:
        print("❌ No content found. Make sure you've run the text extraction scripts.")
        return
    
    print(f"✅ Loaded {len(qa_system.content_database)} content entries")
    
    # Build embeddings
    print("🧠 Building semantic search capabilities...")
    qa_system.build_embeddings()
    
    # Demo questions
    demo_questions = [
        "What is TF-IDF?",
        "How does an inverted index work?",
        "What are the main steps in web crawling?",
        "Explain precision and recall in search evaluation",
        "What is the difference between boolean and vector space models?"
    ]
    
    print("\n🤖 Demo Questions & Answers:")
    print("=" * 50)
    
    for i, question in enumerate(demo_questions, 1):
        print(f"\n{i}. 💭 Question: {question}")
        print("-" * 40)
        
        result = qa_system.answer_question(question)
        print(f"📖 Answer: {result['answer'][:300]}...")
        
        if result['has_context']:
            print(f"💡 Based on {result['sources_used']} course content sections")
        else:
            print("⚠️  General knowledge answer (no specific course content found)")
    
    print(f"\n🎉 Demo complete! You can now use the full system with:")
    print(f"   python course_qa_system.py")

if __name__ == "__main__":
    demo_qa_system()