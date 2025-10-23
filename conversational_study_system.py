#!/usr/bin/env python3
"""
Conversational Study System for CS572 Course Content

An enhanced version of the QA system that maintains conversation context,
allows follow-up questions, and provides a more natural study experience.

Features:
- Maintains conversation history for context
- Supports follow-up questions
- Study session management
- Context-aware responses
- Better formatting for study sessions
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict
import ollama
from datetime import datetime

class ConversationalStudySystem:
    def __init__(self):
        self.slides_dir = Path("slides")
        self.output_dir = Path("output")
        self.midterm_guide_dir = Path("midterm_guide")
        
        # Conversation state
        self.conversation_history = []
        self.current_topic = None
        self.study_session_start = datetime.now()
        
        # Content storage
        self.content_database = {}
        self.quick_facts = {}
        
        print("🎓 CS572 Conversational Study System")
        print("="*50)

    def load_course_content(self):
        """Load all available course content"""
        print("📚 Loading course content...")
        
        # Load from text files
        content_loaded = 0
        if self.output_dir.exists():
            for text_file in self.output_dir.glob("*_slides_text.txt"):
                lecture_name = text_file.stem.replace("_slides_text", "")
                
                try:
                    with open(text_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    self.content_database[lecture_name] = {
                        'raw_text': content,
                        'slides': self.extract_slides_from_text(content)
                    }
                    content_loaded += 1
                    
                except Exception as e:
                    print(f"   ⚠️ Error loading {text_file}: {e}")
        
        # Load structured content from midterm guide
        midterm_json = self.midterm_guide_dir / "midterm_study_content.json"
        if midterm_json.exists():
            try:
                with open(midterm_json, 'r', encoding='utf-8') as f:
                    midterm_data = json.load(f)
                
                self.quick_facts = midterm_data.get('consolidated', {})
                print(f"   ✅ Loaded structured study content")
                
            except Exception as e:
                print(f"   ⚠️ Could not load structured content: {e}")
        
        print(f"✅ Loaded {content_loaded} lectures")
        return content_loaded > 0

    def extract_slides_from_text(self, content):
        """Extract individual slides from lecture text"""
        slides = []
        slide_pattern = r'Slide: (.+?)\n-{30}(.*?)(?=Slide: |$)'
        matches = re.findall(slide_pattern, content, re.DOTALL)
        
        for slide_name, slide_content in matches:
            slides.append({
                'name': slide_name.strip(),
                'content': slide_content.strip()
            })
        
        return slides

    def find_relevant_content(self, question, conversation_context=""):
        """Find content relevant to the question and conversation context"""
        question_lower = question.lower()
        context_lower = conversation_context.lower()
        combined_query = (question_lower + " " + context_lower).strip()
        
        relevant_content = []
        
        # Search through lecture content
        for lecture_name, lecture_data in self.content_database.items():
            lecture_text = lecture_data['raw_text'].lower()
            
            # Simple keyword matching (can be enhanced with embeddings later)
            relevance_score = 0
            for word in combined_query.split():
                if len(word) > 3:  # Ignore short words
                    relevance_score += lecture_text.count(word)
            
            if relevance_score > 0:
                relevant_content.append({
                    'lecture': lecture_name,
                    'score': relevance_score,
                    'content': lecture_data['raw_text'][:2000] + "..." if len(lecture_data['raw_text']) > 2000 else lecture_data['raw_text']
                })
        
        # Sort by relevance
        relevant_content.sort(key=lambda x: x['score'], reverse=True)
        return relevant_content[:3]  # Return top 3 most relevant

    def get_conversation_context(self, last_n=3):
        """Get recent conversation context"""
        if len(self.conversation_history) <= last_n:
            return self.conversation_history
        return self.conversation_history[-last_n:]

    def answer_question(self, question):
        """Generate answer with conversation context"""
        
        # Get conversation context
        recent_context = self.get_conversation_context()
        context_summary = ""
        
        if recent_context:
            context_parts = []
            for entry in recent_context:
                if entry['type'] == 'question':
                    context_parts.append(f"Previous Q: {entry['content']}")
                elif entry['type'] == 'answer':
                    context_parts.append(f"Previous A: {entry['content'][:200]}...")
            context_summary = " | ".join(context_parts)
        
        # Find relevant content
        relevant_content = self.find_relevant_content(question, context_summary)
        
        # Build prompt with context
        if relevant_content:
            content_context = "\n\n".join([
                f"From {item['lecture']}: {item['content']}" 
                for item in relevant_content
            ])
            
            prompt = f"""You are a helpful CS572 Information Retrieval tutor having a conversation with a student.

CONVERSATION CONTEXT:
{context_summary}

CURRENT QUESTION: {question}

RELEVANT COURSE CONTENT:
{content_context}

Please provide a helpful, conversational answer that:
1. Directly addresses the current question
2. References the conversation context if relevant
3. Uses the course content to support your explanation
4. Encourages follow-up questions
5. Keeps a friendly, tutoring tone

If this seems like a follow-up question, acknowledge the connection to previous topics."""

        else:
            prompt = f"""You are a helpful CS572 Information Retrieval tutor. 

CONVERSATION CONTEXT:
{context_summary}

CURRENT QUESTION: {question}

I don't have specific course content for this question, but please provide a helpful answer about Information Retrieval concepts. Keep it conversational and encourage follow-up questions."""

        try:
            response = ollama.chat(model='llama3.1:8b', messages=[
                {'role': 'user', 'content': prompt}
            ])
            
            answer = response['message']['content']
            
            # Update conversation history
            self.conversation_history.append({
                'type': 'question',
                'content': question,
                'timestamp': datetime.now(),
                'relevant_lectures': [item['lecture'] for item in relevant_content]
            })
            
            self.conversation_history.append({
                'type': 'answer',
                'content': answer,
                'timestamp': datetime.now(),
                'sources_used': len(relevant_content)
            })
            
            return {
                'answer': answer,
                'sources_used': len(relevant_content),
                'relevant_lectures': [item['lecture'] for item in relevant_content],
                'conversation_length': len(self.conversation_history)
            }
            
        except Exception as e:
            return {
                'answer': f"Sorry, I encountered an error: {e}",
                'sources_used': 0,
                'relevant_lectures': [],
                'conversation_length': len(self.conversation_history)
            }

    def show_study_stats(self):
        """Show current study session statistics"""
        session_duration = datetime.now() - self.study_session_start
        questions_asked = len([h for h in self.conversation_history if h['type'] == 'question'])
        
        print(f"\n📊 STUDY SESSION STATS")
        print("="*40)
        print(f"⏱️  Session Duration: {session_duration}")
        print(f"❓ Questions Asked: {questions_asked}")
        print(f"💬 Total Exchanges: {len(self.conversation_history)}")
        
        if questions_asked > 0:
            # Show topics covered
            topics_covered = set()
            for entry in self.conversation_history:
                if entry['type'] == 'question' and 'relevant_lectures' in entry:
                    topics_covered.update(entry['relevant_lectures'])
            
            print(f"📚 Topics Covered: {len(topics_covered)}")
            if topics_covered:
                print(f"   • {', '.join(sorted(topics_covered))}")

    def show_help(self):
        """Show available commands"""
        print(f"\n💡 STUDY SYSTEM COMMANDS")
        print("="*40)
        print("• Ask any question about the course content")
        print("• 'stats' - Show study session statistics")
        print("• 'history' - Show recent conversation")
        print("• 'topics' - List available lecture topics")
        print("• 'clear' - Clear conversation history")
        print("• 'help' - Show this help message")
        print("• 'quit' or 'exit' - End study session")

    def show_history(self, last_n=5):
        """Show recent conversation history"""
        print(f"\n💭 RECENT CONVERSATION (last {last_n})")
        print("="*50)
        
        recent = self.get_conversation_context(last_n * 2)  # Get both questions and answers
        
        for i, entry in enumerate(recent):
            timestamp = entry['timestamp'].strftime("%H:%M")
            if entry['type'] == 'question':
                print(f"[{timestamp}] 🤔 You: {entry['content']}")
            else:
                print(f"[{timestamp}] 🤖 AI: {entry['content'][:100]}...")
            print()

    def list_topics(self):
        """List available lecture topics"""
        print(f"\n📚 AVAILABLE LECTURE TOPICS")
        print("="*40)
        for i, lecture in enumerate(sorted(self.content_database.keys()), 1):
            slide_count = len(self.content_database[lecture]['slides'])
            print(f"{i:2}. {lecture.replace('_', ' ').title()} ({slide_count} slides)")

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("✅ Conversation history cleared!")

    def start_study_session(self):
        """Start interactive study session"""
        
        if not self.load_course_content():
            print("❌ No course content found! Please make sure you have:")
            print("1. Run extract.py or read_slides.py to process slides")
            print("2. Generated midterm guide content")
            return
        
        print("\n🎯 Ready for your study session!")
        print("Ask me anything about your CS572 course content.")
        print("I'll remember our conversation context for follow-up questions.")
        print("Type 'help' to see available commands.\n")
        
        while True:
            try:
                print("─" * 60)
                user_input = input("🤔 Your question or command: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    self.show_study_stats()
                    print("\n🎓 Great study session! Good luck with your coursework! 📚")
                    break
                
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                elif user_input.lower() == 'stats':
                    self.show_study_stats()
                    continue
                
                elif user_input.lower() == 'history':
                    self.show_history()
                    continue
                
                elif user_input.lower() == 'topics':
                    self.list_topics()
                    continue
                
                elif user_input.lower() == 'clear':
                    self.clear_history()
                    continue
                
                # Process as question
                print("\n🤖 Thinking...")
                result = self.answer_question(user_input)
                
                print(f"\n💬 Response:")
                print("─" * 40)
                print(result['answer'])
                print("─" * 40)
                
                # Show source info
                if result['sources_used'] > 0:
                    lectures = ", ".join(result['relevant_lectures'])
                    print(f"📖 Referenced: {lectures}")
                
                print(f"💭 Conversation exchanges: {result['conversation_length']}")
                
            except KeyboardInterrupt:
                print("\n\n🎓 Study session ended. Good luck! 📚")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

def main():
    study_system = ConversationalStudySystem()
    study_system.start_study_session()

if __name__ == "__main__":
    main()