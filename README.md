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

### Step 2: Convert to Study Materials

```bash
# Generate all formats (recommended)
python read_slides.py se-basics --output-format all

# Or choose specific formats
python read_slides.py querying --output-format pdf
python read_slides.py lecture-name --output-format docx
```

### 📋 Complete Workflow Example

```bash
# 1. Download slides from any source
python extract.py "https://example.com/lecture.pdf" "my-lecture"

# 2. Convert to searchable documents
python read_slides.py my-lecture --output-format all

# 3. Study materials are ready in output/ folder!
```

## Output Structure

```
slides/
├── se-basics/          # PDF-converted slides
│   ├── slide_001.png
│   ├── slide_002.png
│   └── ...
└── querying/           # HTML presentation slides
    ├── s1.png
    ├── s2.png
    └── ...

output/
├── se-basics_slides_text.txt   # Plain text
├── se-basics_slides_text.pdf   # PDF document
└── se-basics_slides_text.docx  # Word document
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
- 🔄 **Batch Processing** - Process entire lecture folders at once

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