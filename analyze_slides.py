#!/usr/bin/env python3
"""
AI-Powered Study Guide Generator
Creates intelligent study guides from lecture slides using AI analysis.

This script processes slide images and extracted text to generate:
- Comprehensive study guides with key concepts
- Practice questions and answers
- Algorithm explanations and breakdowns
- Memory aids and mnemonics
- Concept relationships and connections
"""

import os
import sys
import json
import base64
from pathlib import Path
from typing import List, Dict, Optional
import argparse

# AI Package imports (install as needed)
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    GOOGLE_AI_AVAILABLE = False

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

class StudyGuideGenerator:
    def __init__(self, ai_provider="openai", api_key=None):
        self.ai_provider = ai_provider
        self.api_key = api_key
        self.setup_ai_client()
    
    def setup_ai_client(self):
        """Initialize the AI client based on the provider."""
        if self.ai_provider == "openai" and OPENAI_AVAILABLE:
            if not self.api_key:
                self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable.")
            openai.api_key = self.api_key
            self.client = openai
            
        elif self.ai_provider == "google" and GOOGLE_AI_AVAILABLE:
            if not self.api_key:
                self.api_key = os.getenv("GOOGLE_API_KEY")
            if not self.api_key:
                raise ValueError("Google API key required. Set GOOGLE_API_KEY environment variable.")
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel('gemini-pro-vision')
            
        elif self.ai_provider == "anthropic" and ANTHROPIC_AVAILABLE:
            if not self.api_key:
                self.api_key = os.getenv("ANTHROPIC_API_KEY")
            if not self.api_key:
                raise ValueError("Anthropic API key required. Set ANTHROPIC_API_KEY environment variable.")
            self.client = Anthropic(api_key=self.api_key)
            
        elif self.ai_provider == "ollama" and OLLAMA_AVAILABLE:
            self.client = ollama
            
        else:
            raise ValueError(f"AI provider '{self.ai_provider}' not available or not installed.")

    def encode_image(self, image_path: Path) -> str:
        """Encode image to base64 for API submission."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def get_slide_text(self, lecture_name: str) -> str:
        """Get extracted text for a lecture."""
        text_file = Path("output") / f"{lecture_name}_slides_text.txt"
        if text_file.exists():
            return text_file.read_text(encoding='utf-8')
        return ""

    def analyze_slide_content(self, image_path: Path, slide_text: str, lecture_context: str) -> Dict:
        """Analyze a single slide using AI to extract study information."""
        
        if self.ai_provider == "openai":
            return self._analyze_with_openai(image_path, slide_text, lecture_context)
        elif self.ai_provider == "google":
            return self._analyze_with_google(image_path, slide_text, lecture_context)
        elif self.ai_provider == "anthropic":
            return self._analyze_with_anthropic(image_path, slide_text, lecture_context)
        elif self.ai_provider == "ollama":
            return self._analyze_with_ollama(slide_text, lecture_context)

    def _analyze_with_openai(self, image_path: Path, slide_text: str, lecture_context: str) -> Dict:
        """Analyze using OpenAI GPT-4 Vision."""
        
        # Encode image
        base64_image = self.encode_image(image_path)
        
        prompt = f"""
        Analyze this lecture slide from a CS572 Information Retrieval course.
        
        Context: {lecture_context}
        Extracted Text: {slide_text}
        
        Please provide a comprehensive study analysis in JSON format with these sections:
        {{
            "key_concepts": ["list of main concepts covered"],
            "algorithms": ["any algorithms mentioned with brief explanations"],
            "equations": ["mathematical formulas with explanations"],
            "study_points": ["important points to remember for exams"],
            "practice_questions": ["3-5 potential exam questions about this content"],
            "memory_aids": ["mnemonics or memory tricks for complex concepts"],
            "connections": ["how this relates to other CS/IR concepts"],
            "difficulty_level": "beginner/intermediate/advanced",
            "estimated_study_time": "time in minutes to master this slide"
        }}
        
        Focus on creating actionable study material that helps with memorization and understanding.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            # Try to extract JSON from the response
            try:
                json_start = content.find('{')
                json_end = content.rfind('}') + 1
                json_str = content[json_start:json_end]
                return json.loads(json_str)
            except:
                # Fallback if JSON parsing fails
                return {"analysis": content}
                
        except Exception as e:
            return {"error": str(e)}

    def _analyze_with_ollama(self, slide_text: str, lecture_context: str) -> Dict:
        """Analyze using local Ollama model (text-only)."""
        
        prompt = f"""
        Analyze this lecture slide content from a CS572 Information Retrieval course.
        
        Context: {lecture_context}
        Slide Content: {slide_text}
        
        Create a concise study analysis with:
        - Key concepts (2-3 main points)
        - Study tip (1 memory aid)
        - Practice question (1 exam-style question)
        
        Keep response under 200 words and focus on the most important information.
        """
        
        try:
            response = self.client.generate(
                model='llama3.1:8b',
                prompt=prompt,
                options={'num_predict': 150}  # Limit response length for speed
            )
            
            return {
                "analysis": response['response'],
                "provider": "ollama"
            }
        except Exception as e:
            return {"error": str(e)}

    def generate_lecture_study_guide(self, lecture_name: str) -> Dict:
        """Generate a complete study guide for an entire lecture."""
        
        print(f"🎓 Generating AI study guide for: {lecture_name}")
        
        # Get lecture folder and text
        slides_dir = Path("slides") / lecture_name
        if not slides_dir.exists():
            return {"error": f"Lecture folder '{lecture_name}' not found"}
        
        lecture_text = self.get_slide_text(lecture_name)
        
        # Get all slide images
        image_files = []
        for ext in ['.png', '.jpg', '.jpeg']:
            image_files.extend(slides_dir.glob(f"*{ext}"))
        
        image_files.sort()
        
        if not image_files:
            return {"error": "No slide images found"}
        
        print(f"📊 Analyzing {len(image_files)} slides...")
        
        study_guide = {
            "lecture_name": lecture_name,
            "total_slides": len(image_files),
            "slides": [],
            "summary": {}
        }
        
        # Analyze each slide
        for i, image_path in enumerate(image_files, 1):
            print(f"🔍 Analyzing slide {i}/{len(image_files)}: {image_path.name}")
            
            # Get slide-specific text (simplified)
            slide_text_section = f"Slide {i} content from lecture"
            
            analysis = self.analyze_slide_content(
                image_path, 
                slide_text_section, 
                f"CS572 Information Retrieval - {lecture_name}"
            )
            
            analysis["slide_number"] = i
            analysis["slide_file"] = image_path.name
            study_guide["slides"].append(analysis)
        
        # Generate overall summary
        study_guide["summary"] = self._generate_lecture_summary(study_guide["slides"], lecture_name)
        
        return study_guide

    def _generate_lecture_summary(self, slide_analyses: List[Dict], lecture_name: str) -> Dict:
        """Generate an overall summary and study plan for the lecture."""
        
        # Collect all concepts, questions, etc.
        all_concepts = []
        all_questions = []
        all_algorithms = []
        
        for slide in slide_analyses:
            if "key_concepts" in slide:
                all_concepts.extend(slide.get("key_concepts", []))
            if "practice_questions" in slide:
                all_questions.extend(slide.get("practice_questions", []))
            if "algorithms" in slide:
                all_algorithms.extend(slide.get("algorithms", []))
        
        return {
            "total_concepts": len(set(all_concepts)),
            "key_concepts_summary": list(set(all_concepts))[:10],  # Top 10 unique
            "practice_exam_questions": all_questions[:15],  # Top 15 questions
            "algorithms_covered": list(set(all_algorithms)),
            "recommended_study_time": f"{len(slide_analyses) * 5}-{len(slide_analyses) * 8} minutes",
            "study_strategy": f"Focus on {lecture_name} concepts with emphasis on practical applications"
        }

    def save_study_guide(self, study_guide: Dict, lecture_name: str):
        """Save the study guide to files."""
        
        output_dir = Path("study_guides")
        output_dir.mkdir(exist_ok=True)
        
        # Save JSON version
        json_file = output_dir / f"{lecture_name}_study_guide.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(study_guide, f, indent=2, ensure_ascii=False)
        
        # Save readable text version
        text_file = output_dir / f"{lecture_name}_study_guide.txt"
        self._save_readable_guide(study_guide, text_file)
        
        print(f"📚 Study guide saved:")
        print(f"   📄 JSON: {json_file}")
        print(f"   📝 Text: {text_file}")

    def _save_readable_guide(self, study_guide: Dict, file_path: Path):
        """Save a human-readable study guide."""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            lecture_name = study_guide.get('lecture_name', 'Unknown')
            
            f.write(f"# 🎓 Study Guide: {lecture_name.title()}\n")
            f.write("=" * 60 + "\n\n")
            
            # Summary
            summary = study_guide.get('summary', {})
            f.write("## 📋 Lecture Overview\n")
            f.write(f"- **Total Slides**: {study_guide.get('total_slides', 0)}\n")
            f.write(f"- **Key Concepts**: {summary.get('total_concepts', 0)}\n")
            f.write(f"- **Study Time**: {summary.get('recommended_study_time', 'N/A')}\n\n")
            
            # Key concepts
            if summary.get('key_concepts_summary'):
                f.write("## 🎯 Key Concepts to Master\n")
                for i, concept in enumerate(summary['key_concepts_summary'], 1):
                    f.write(f"{i}. {concept}\n")
                f.write("\n")
            
            # Practice questions
            if summary.get('practice_exam_questions'):
                f.write("## ❓ Practice Questions\n")
                for i, question in enumerate(summary['practice_exam_questions'], 1):
                    f.write(f"{i}. {question}\n")
                f.write("\n")
            
            # Slide-by-slide breakdown
            f.write("## 📊 Slide-by-Slide Analysis\n")
            for slide in study_guide.get('slides', []):
                slide_num = slide.get('slide_number', 'Unknown')
                f.write(f"### Slide {slide_num}\n")
                
                if 'key_concepts' in slide:
                    f.write("**Key Points:**\n")
                    for concept in slide['key_concepts']:
                        f.write(f"- {concept}\n")
                
                if 'study_points' in slide:
                    f.write("**Study Focus:**\n")
                    for point in slide['study_points']:
                        f.write(f"- {point}\n")
                
                f.write("\n")

def main():
    """Main function with CLI interface."""
    
    parser = argparse.ArgumentParser(
        description="Generate AI-powered study guides from lecture slides",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze_slides.py querying --provider openai
  python analyze_slides.py --all --provider google
  python analyze_slides.py se-basics --provider ollama
  
Setup:
  1. Install AI packages: pip install openai google-generativeai anthropic ollama-python
  2. Set API keys: export OPENAI_API_KEY="your-key"
  3. For Ollama: install Ollama and pull a model (ollama pull llama3.1:8b)
        """
    )
    
    parser.add_argument("lecture", nargs='?', help="Lecture name to analyze (or use --all)")
    parser.add_argument("--all", action="store_true", help="Analyze all lectures")
    parser.add_argument("--provider", choices=["openai", "google", "anthropic", "ollama"], 
                       default="openai", help="AI provider to use")
    parser.add_argument("--api-key", help="API key (or set environment variable)")
    
    args = parser.parse_args()
    
    if not args.lecture and not args.all:
        print("❌ Please specify a lecture name or use --all")
        parser.print_help()
        return
    
    # Check available providers
    available_providers = []
    if OPENAI_AVAILABLE: available_providers.append("openai")
    if GOOGLE_AI_AVAILABLE: available_providers.append("google") 
    if ANTHROPIC_AVAILABLE: available_providers.append("anthropic")
    if OLLAMA_AVAILABLE: available_providers.append("ollama")
    
    if args.provider not in available_providers:
        print(f"❌ Provider '{args.provider}' not available.")
        print(f"Available providers: {', '.join(available_providers)}")
        print("\nInstall packages with:")
        print("pip install openai google-generativeai anthropic ollama-python")
        return
    
    try:
        # Initialize AI client
        generator = StudyGuideGenerator(args.provider, args.api_key)
        
        # Get lectures to process
        if args.all:
            slides_dir = Path("slides")
            lectures = [d.name for d in slides_dir.iterdir() if d.is_dir()]
        else:
            lectures = [args.lecture]
        
        print(f"🤖 Using AI provider: {args.provider}")
        print(f"📚 Processing {len(lectures)} lecture(s)")
        
        # Process each lecture
        for lecture in lectures:
            try:
                study_guide = generator.generate_lecture_study_guide(lecture)
                if "error" not in study_guide:
                    generator.save_study_guide(study_guide, lecture)
                    print(f"✅ Completed: {lecture}")
                else:
                    print(f"❌ Error processing {lecture}: {study_guide['error']}")
            except Exception as e:
                print(f"❌ Error processing {lecture}: {e}")
        
        print(f"\n🎉 Study guide generation complete!")
        print(f"📁 Check the 'study_guides/' folder for your AI-generated materials!")
        
    except Exception as e:
        print(f"❌ Setup error: {e}")

if __name__ == "__main__":
    main()
