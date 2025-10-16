# 🎓 USC CS572 Slide Scraper & Text Extractor

A comprehensive Python toolkit for downloading lecture slides and converting them into searchable, studyable documents. Perfect for USC CS572 students who want to transform lecture presentations into organized study materials.

## ✨ What it does

This project provides a complete workflow for processing lecture materials:

### 📥 **Slide Extraction (`extract.py`)**
- **HTML Presentations**: Automatically finds and downloads all slide images from web-based presentations
- **PDF Lectures**: Downloads PDF files and converts each page to high-quality images
- **Smart Detection**: Automatically detects file type and uses appropriate processing method
- **Organized Storage**: Creates clean folder structure with lecture-specific directories

### 🔍 **Text Extraction (`read_slides.py`)**
- **OCR Processing**: Uses Tesseract OCR to extract text from slide images
- **Smart Cleaning**: Removes university branding, headers, and irrelevant text
- **Multiple Formats**: Generates study materials in PDF, Word, and plain text formats
- **Lecture Organization**: Processes entire lecture folders with proper slide sequencing

### 🤖 **AI-Powered Study Materials (`study_extractor.py`)**
- **Content Extraction**: Uses local AI to extract key concepts, definitions, and facts
- **Smart Flashcards**: Generates Q&A pairs for active recall and memorization
- **Cheat Sheets**: Creates condensed 1-page reference guides for quick review
- **Study Organization**: Structures content specifically for learning and exam preparation
- **Batch Processing**: Generate study materials for all lectures automatically

### 📚 **Comprehensive Midterm Study Guide (`midterm_study_guide.py`)**
- **Complete Analysis**: Processes ALL slides from ALL lectures in one comprehensive guide
- **AI-Powered Extraction**: Uses AI to identify the most important concepts, definitions, formulas, and algorithms
- **Multiple Formats**: Generates Word document (detailed), PDF (summary), and text files for different study needs  
- **Exam Focused**: Specifically designed to ensure nothing is missed for midterm preparation
- **Statistical Overview**: Tracks and reports exactly what content was extracted from each lecture

### 🤖 **Course Content Q&A System (`course_qa_system.py`)**
- **RAG-Based AI**: Ask questions about your course materials and get answers based on your actual content
- **Semantic Search**: Uses advanced embeddings to find relevant content across all lectures
- **Interactive Chat**: Natural language Q&A interface powered by local AI (Ollama)
- **Source Attribution**: Shows which course materials were used to generate each answer
- **Comprehensive Database**: Searches through 2000+ content entries from all processed lectures

## Requirements

Install all dependencies:
```bash
pip install -r requirements.txt
```

For PDF support, you also need Tesseract OCR:
```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr
```

For AI-powered study materials and Q&A system, install and set up Ollama:
```bash
# macOS
brew install ollama
ollama pull llama3.1:8b
pip install ollama

# For Q&A system, also install:
pip install sentence-transformers scikit-learn numpy
```

## 🚀 Quick Start

### Step 1: Download Lecture Slides

**For HTML-based slide presentations:**
```bash
python extract.py "https://bytes.usc.edu/cs572/f25-6-AIR/lectures/querying/index.html#(2)" "querying"
# Downloads 52 individual slide images
```

**For PDF lecture files:**
```bash
python extract.py "https://bytes.usc.edu/cs572/f25-6-AIR/lectures/Web/CharacterizingtheWeb.pdf" "web serving basics"
# Converts 31 PDF pages to high-quality images
```

### Step 2: Extract Text from Slides

```bash
# Generate searchable text documents
python read_slides.py se-basics --output-format all
python process_all.py  # Process all lectures at once

# Or choose specific formats
python read_slides.py querying --output-format pdf
```

### Step 3: Create AI Study Materials & Q&A System

```bash
# Generate comprehensive midterm study guide
python midterm_study_guide.py

# Create interactive Q&A system for asking questions
python course_qa_system.py

# Or generate individual lecture study materials
python study_extractor.py se-basics
python study_extractor.py --all  # Process all lectures

# Creates flashcards, cheat sheets, and study content
```

### 📋 Complete Workflow Example

```bash
# 1. Download slides from any source
python extract.py "https://example.com/lecture.pdf" "my-lecture"

# 2. Extract text from slides  
python read_slides.py my-lecture --output-format all

# 3. Generate AI-powered study materials
python study_extractor.py my-lecture

# 4. Everything ready for studying!
```

## Output Structure

```
slides/                 # Downloaded slide images
├── se-basics/          # PDF-converted slides
│   ├── slide_001.png
│   └── ...
└── querying/           # HTML presentation slides
    ├── s1.png
    └── ...

output/                 # OCR-extracted text
├── se-basics_slides_text.txt
├── se-basics_slides_text.pdf
└── se-basics_slides_text.docx

study_materials/        # AI-generated study materials  
├── se-basics_study_content.md    # Key concepts & definitions
├── se-basics_flashcards.txt      # Q&A for memorization
├── se-basics_cheat_sheet.txt     # Quick reference guide
└── ...

midterm_guide/          # Comprehensive midterm study guide
├── midterm_study_guide_comprehensive.docx  # Complete study guide
├── midterm_study_guide_summary.pdf         # Quick overview
├── midterm_study_content_summary.json      # Data export
└── quick_study_overview.txt                # Processing summary
```

## 🌟 Key Features

### 📊 **Universal Compatibility**
- ✅ HTML slide presentations (like querying lectures)
- ✅ PDF lecture files (like SearchEngineBasics.pdf)
- ✅ Automatic format detection and processing
- ✅ Works with any USC CS572 lecture URL

### 🧠 **Smart Text Processing**
- 🔍 Advanced OCR with Tesseract integration
- 🧹 Automatic removal of university headers and branding
- 📝 Preserves lecture content while filtering noise
- 🎯 Slide-by-slide organization with clear separation

### 📚 **Multiple Study Formats**
- 📄 **Plain Text** (`.txt`) - Easy to search and copy
- 📑 **PDF Documents** (`.pdf`) - Professional formatting for printing
- 📝 **Word Documents** (`.docx`) - Editable for notes and annotations
- 🤖 **AI Study Materials** - Flashcards, cheat sheets, and organized content
- � **Comprehensive Study Guide** - Complete midterm guide analyzing all lectures  
- �🔄 **Batch Processing** - Process entire lecture folders at once

### ⚡ **Quality & Performance**
- 🖼️ High-resolution image conversion (2x zoom for PDFs)
- 📁 Organized file structure with lecture-specific folders
- 🚀 Efficient processing with progress tracking
- 💾 Automatic duplicate handling and file naming

## 🎯 Perfect For
- 📖 Creating searchable study guides from lecture slides
- 🔍 Finding specific topics across multiple lectures  
- 📝 Preparing annotated notes for exams
- 📚 Building a personal knowledge base of course materials
- 🧠 Active recall study sessions with AI-generated flashcards
- 📋 Quick exam prep with condensed cheat sheets  
- 🎓 Comprehensive midterm preparation with complete content analysis
- 📚 Ensuring no important material is missed for exams

## 🚀 Available Scripts

| Script | Purpose | Example |
|--------|---------|---------|
| `extract.py` | Download slides from URLs | `python extract.py <url> <name>` |
| `read_slides.py` | Extract text via OCR | `python read_slides.py <lecture> --output-format txt` |
| `process_all.py` | Batch OCR processing | `python process_all.py` |
| `study_extractor.py` | AI study materials | `python study_extractor.py <lecture>` |
| `quick_study_guide.py` | Alternative AI analysis | `python quick_study_guide.py <lecture>` |
| `midterm_study_guide.py` | **Comprehensive midterm guide** | `python midterm_study_guide.py` |
| `course_qa_system.py` | **Interactive Q&A with course content** | `python course_qa_system.py` |
| `study_guide_helper.py` | Study guide navigation | `python study_guide_helper.py` |
| `qa_demo.py` | Q&A system demonstration | `python qa_demo.py` |