#!/usr/bin/env python3
"""
CS572 Course Content Q&A System

A RAG (Retrieval-Augmented Generation) system that allows you to ask questions
about your course materials and get AI-powered answers based on the actual
slide content you've extracted.

Usage:
    python course_qa_system.py
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict
import ollama
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle

class CourseQASystem:
    def __init__(self):
        self.slides_dir = Path("slides")
        self.output_dir = Path("output")
        self.qa_data_dir = Path("qa_system_data")
        self.qa_data_dir.mkdir(exist_ok=True)
        
        # Initialize embeddings model for semantic search
        print("🤖 Loading sentence transformer model...")
        self.embeddings_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Storage for course content
        self.content_database = []
        self.content_embeddings = None
        
        print("🎓 CS572 Course Q&A System initialized")

    def extract_text_from_files(self):
        """Extract text content from all processed lecture files"""
        print("\n📚 Building course content database...")
        
        content_count = 0
        
        # Check for existing text files in output directory
        if self.output_dir.exists():
            for text_file in self.output_dir.glob("*_slides_text.txt"):
                lecture_name = text_file.stem.replace("_slides_text", "")
                
                try:
                    with open(text_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Split content into chunks by slides
                    slides = self.split_into_slides(content, lecture_name)
                    self.content_database.extend(slides)
                    content_count += len(slides)
                    
                    print(f"   📄 {lecture_name}: {len(slides)} slides added")
                    
                except Exception as e:
                    print(f"   ❌ Error reading {text_file}: {e}")
        
        # Also extract from midterm guide if available
        midterm_json = Path("midterm_guide/midterm_study_content.json")
        if midterm_json.exists():
            try:
                with open(midterm_json, 'r', encoding='utf-8') as f:
                    midterm_data = json.load(f)
                
                # Extract from consolidated content
                consolidated = midterm_data.get('consolidated', {})
                for category in ['key_concepts', 'definitions', 'formulas', 'algorithms']:
                    for item in consolidated.get(category, []):
                        self.content_database.append({
                            'lecture': item.get('lecture', 'unknown'),
                            'type': category,
                            'content': item.get('text', ''),
                            'source': 'midterm_guide'
                        })
                        content_count += 1
                
                print(f"   🎯 Midterm guide: {len(consolidated.get('key_concepts', []))} concepts, {len(consolidated.get('definitions', []))} definitions added")
                
            except Exception as e:
                print(f"   ⚠️ Could not load midterm guide data: {e}")
        
        print(f"\n✅ Content database built: {content_count} total entries")
        return content_count > 0

    def split_into_slides(self, content, lecture_name):
        """Split lecture content into individual slide chunks"""
        slides = []
        
        # Split by slide markers (common patterns)
        slide_patterns = [
            r'--- Slide \d+ ---',
            r'=== Slide \d+ ===',
            r'Slide \d+:',
            r'\n\n\d+\.\s',  # Numbered sections
            r'\n\n[A-Z][^.]*:\n'  # Title-like sections
        ]
        
        # Try to split by patterns, fallback to paragraph chunks
        for pattern in slide_patterns:
            parts = re.split(pattern, content, flags=re.IGNORECASE)
            if len(parts) > 1:
                for i, part in enumerate(parts[1:], 1):  # Skip first empty part
                    clean_part = part.strip()
                    if len(clean_part) > 50:  # Only include substantial content
                        slides.append({
                            'lecture': lecture_name,
                            'slide_number': i,
                            'content': clean_part,
                            'type': 'slide_content',
                            'source': 'extracted_text'
                        })
                return slides
        
        # Fallback: split into paragraph chunks
        paragraphs = content.split('\n\n')
        for i, paragraph in enumerate(paragraphs):
            clean_paragraph = paragraph.strip()
            if len(clean_paragraph) > 50:
                slides.append({
                    'lecture': lecture_name,
                    'slide_number': i + 1,
                    'content': clean_paragraph,
                    'type': 'paragraph',
                    'source': 'extracted_text'
                })
        
        return slides

    def build_embeddings(self):
        """Create embeddings for all content for semantic search"""
        print("\n🧠 Building semantic search embeddings...")
        
        embeddings_file = self.qa_data_dir / "content_embeddings.pkl"
        content_file = self.qa_data_dir / "content_database.pkl"
        
        # Check if embeddings already exist
        if embeddings_file.exists() and content_file.exists():
            print("   📂 Loading existing embeddings...")
            try:
                with open(embeddings_file, 'rb') as f:
                    self.content_embeddings = pickle.load(f)
                with open(content_file, 'rb') as f:
                    saved_content = pickle.load(f)
                
                # Verify content matches
                if len(saved_content) == len(self.content_database):
                    print("   ✅ Embeddings loaded successfully")
                    return
            except Exception as e:
                print(f"   ⚠️ Error loading embeddings: {e}")
        
        # Generate new embeddings
        print("   🔄 Generating new embeddings (this may take a moment)...")
        
        # Extract text for embedding
        texts = [item['content'] for item in self.content_database]
        
        # Generate embeddings in batches to avoid memory issues
        batch_size = 32
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = self.embeddings_model.encode(batch)
            all_embeddings.extend(batch_embeddings)
            
            if i % (batch_size * 10) == 0:
                print(f"   📊 Progress: {i}/{len(texts)} embeddings generated")
        
        self.content_embeddings = np.array(all_embeddings)
        
        # Save embeddings for future use
        with open(embeddings_file, 'wb') as f:
            pickle.dump(self.content_embeddings, f)
        with open(content_file, 'wb') as f:
            pickle.dump(self.content_database, f)
        
        print(f"   ✅ Generated {len(all_embeddings)} embeddings")

    def search_relevant_content(self, query, top_k=5):
        """Search for content most relevant to the query"""
        if self.content_embeddings is None:
            print("❌ Embeddings not built. Run build_embeddings() first.")
            return []
        
        # Generate query embedding
        query_embedding = self.embeddings_model.encode([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_embedding, self.content_embeddings)[0]
        
        # Get top matches
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Minimum similarity threshold
                results.append({
                    'content': self.content_database[idx],
                    'similarity': similarities[idx]
                })
        
        return results

    def answer_question(self, question, use_context=True):
        """Generate an answer using AI with relevant course content"""
        
        if use_context and len(self.content_database) > 0:
            # Search for relevant content
            relevant_results = self.search_relevant_content(question, top_k=5)
            
            if relevant_results:
                # Build context from relevant content
                context_parts = []
                for result in relevant_results:
                    content = result['content']
                    similarity = result['similarity']
                    
                    context_parts.append(f"From {content['lecture']} ({content['type']}): {content['content']}")
                
                context = "\n\n".join(context_parts)
                
                prompt = f"""Based on the CS572 Information Retrieval course content below, please answer the following question:

QUESTION: {question}

RELEVANT COURSE CONTENT:
{context}

Please provide a comprehensive answer based on the course materials. If the content doesn't fully address the question, mention what information is available and what might be missing."""

            else:
                prompt = f"""I have a question about CS572 Information Retrieval, but I couldn't find directly relevant content in the course materials. Please provide a general answer about: {question}

Please note that this answer is not based on the specific course content."""

        else:
            prompt = f"Please answer this question about Information Retrieval: {question}"

        try:
            response = ollama.chat(model='llama3.1:8b', messages=[
                {'role': 'user', 'content': prompt}
            ])
            
            return {
                'answer': response['message']['content'],
                'sources_used': len(relevant_results) if use_context else 0,
                'has_context': use_context and len(relevant_results) > 0
            }
            
        except Exception as e:
            return {
                'answer': f"Error generating answer: {e}",
                'sources_used': 0,
                'has_context': False
            }

    def interactive_qa(self):
        """Interactive Q&A session"""
        print("\n" + "="*60)
        print("🎓 CS572 Course Content Q&A System")
        print("="*60)
        print("Ask questions about your course materials!")
        print("Type 'quit', 'exit', or 'q' to end the session.")
        print("Type 'stats' to see system statistics.")
        print("-"*60)
        
        while True:
            try:
                question = input("\n💭 Your question: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("\n🎓 Happy studying! Good luck with your coursework! 📚")
                    break
                
                if question.lower() == 'stats':
                    self.show_stats()
                    continue
                
                if not question:
                    print("Please enter a question.")
                    continue
                
                print("🔍 Searching course content...")
                result = self.answer_question(question)
                
                print(f"\n📖 Answer:")
                print("-" * 40)
                print(result['answer'])
                
                if result['has_context']:
                    print(f"\n💡 Based on {result['sources_used']} relevant course content sections")
                else:
                    print(f"\n⚠️  Answer not based on specific course content")
                
            except KeyboardInterrupt:
                print("\n\n🎓 Happy studying! Good luck with your coursework! 📚")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

    def show_stats(self):
        """Show system statistics"""
        print(f"\n📊 SYSTEM STATISTICS")
        print("-" * 30)
        print(f"📚 Total content entries: {len(self.content_database)}")
        
        if self.content_database:
            # Count by lecture
            lectures = defaultdict(int)
            content_types = defaultdict(int)
            
            for item in self.content_database:
                lectures[item['lecture']] += 1
                content_types[item['type']] += 1
            
            print(f"🏫 Lectures covered: {len(lectures)}")
            for lecture, count in sorted(lectures.items()):
                print(f"   • {lecture}: {count} entries")
            
            print(f"📝 Content types:")
            for content_type, count in sorted(content_types.items()):
                print(f"   • {content_type}: {count} entries")
        
        print(f"🧠 Embeddings ready: {'Yes' if self.content_embeddings is not None else 'No'}")

    def run(self):
        """Main execution"""
        print("🎓 Starting CS572 Course Q&A System")
        print("=" * 50)
        
        # Build content database
        if not self.extract_text_from_files():
            print("❌ No course content found!")
            print("Make sure you have:")
            print("1. Run read_slides.py to extract text from slides")
            print("2. Or run midterm_study_guide.py to generate comprehensive content")
            return
        
        # Build embeddings
        self.build_embeddings()
        
        # Start interactive session
        self.interactive_qa()

def main():
    qa_system = CourseQASystem()
    qa_system.run()

if __name__ == "__main__":
    main()