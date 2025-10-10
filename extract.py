#!/usr/bin/env python3
"""
Slide Image Scraper
Downloads all slide images from USC CS572 lecture presentations.
Supports both HTML presentations and PDF files.

Usage:
    python extract.py <URL> <LECTURE_NAME>
    
Example:
    python extract.py "https://bytes.usc.edu/cs572/f25-6-AIR/lectures/querying/index.html#(2)" "querying"
    python extract.py "https://bytes.usc.edu/cs572/f25-6-AIR/lectures/SEBasics/SearchEngineBasics.pdf" "se-basics"
"""

import os
import re
import sys
import argparse
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from pathlib import Path
import time

try:
    import fitz  # PyMuPDF
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

def create_lecture_directory(lecture_name):
    """Create the slides directory and lecture subdirectory if they don't exist."""
    slides_dir = Path("slides")
    slides_dir.mkdir(exist_ok=True)
    
    # Clean the lecture name to be filesystem-friendly
    clean_name = re.sub(r'[^\w\-_\.]', '_', lecture_name.strip())
    clean_name = re.sub(r'_+', '_', clean_name)  # Replace multiple underscores with single
    clean_name = clean_name.strip('_')  # Remove leading/trailing underscores
    
    lecture_dir = slides_dir / clean_name
    lecture_dir.mkdir(exist_ok=True)
    return lecture_dir

def is_pdf_url(url):
    """Check if the URL points to a PDF file."""
    parsed_url = urlparse(url)
    return parsed_url.path.lower().endswith('.pdf')

def download_file(url):
    """Download content from the given URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Error fetching content from {url}: {e}")
        return None

def get_page_content(url):
    """Fetch the HTML content from the given URL."""
    response = download_file(url)
    if response:
        return response.text
    return None

def extract_image_urls(html_content, base_url):
    """Extract all image URLs from the HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all img tags
    img_tags = soup.find_all('img')
    image_urls = []
    
    for img in img_tags:
        src = img.get('src')
        if src:
            # Convert relative URLs to absolute URLs
            full_url = urljoin(base_url, src)
            image_urls.append(full_url)
    
    # Also look for background images in style attributes
    elements_with_style = soup.find_all(attrs={'style': True})
    for element in elements_with_style:
        style = element.get('style', '')
        # Look for background-image URLs
        bg_matches = re.findall(r'background-image:\s*url\(["\']?([^"\')\s]+)["\']?\)', style)
        for match in bg_matches:
            full_url = urljoin(base_url, match)
            image_urls.append(full_url)
    
    return list(set(image_urls))  # Remove duplicates

def convert_pdf_to_images(pdf_content, lecture_dir):
    """Convert PDF pages to images and save them."""
    if not PDF_SUPPORT:
        print("PDF support not available. Please install PyMuPDF:")
        print("pip install PyMuPDF")
        return 0
    
    try:
        # Open PDF from memory
        pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
        
        successful_conversions = 0
        
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            
            # Convert page to image (PNG)
            # Higher resolution for better quality
            mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better quality
            pix = page.get_pixmap(matrix=mat)
            
            # Save as PNG
            filename = f"slide_{page_num + 1:03d}.png"
            file_path = lecture_dir / filename
            
            pix.save(file_path)
            print(f"Converted page {page_num + 1} to: {filename}")
            successful_conversions += 1
        
        pdf_document.close()
        return successful_conversions
        
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        return 0

def download_image(url, lecture_dir, index=None):
    """Download a single image from the given URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        
        # Extract filename from URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        # If no filename or extension, create one
        if not filename or '.' not in filename:
            extension = '.png'  # Default extension
            if 'content-type' in response.headers:
                content_type = response.headers['content-type']
                if 'jpeg' in content_type or 'jpg' in content_type:
                    extension = '.jpg'
                elif 'png' in content_type:
                    extension = '.png'
                elif 'gif' in content_type:
                    extension = '.gif'
            
            if index is not None:
                filename = f"slide_{index:03d}{extension}"
            else:
                filename = f"image_{int(time.time())}{extension}"
        
        # Ensure unique filename
        file_path = lecture_dir / filename
        counter = 1
        original_stem = file_path.stem
        original_suffix = file_path.suffix
        
        while file_path.exists():
            file_path = lecture_dir / f"{original_stem}_{counter}{original_suffix}"
            counter += 1
        
        # Download and save the image
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Downloaded: {filename}")
        return True
        
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return False

def process_pdf_file(url, lecture_name):
    """Process a PDF file by converting each page to an image."""
    print(f"Processing PDF from: {url}")
    print(f"Lecture: {lecture_name}")
    
    # Create lecture directory
    lecture_dir = create_lecture_directory(lecture_name)
    print(f"Saving images to: {lecture_dir.absolute()}")
    
    # Download PDF
    print("Downloading PDF...")
    response = download_file(url)
    if not response:
        print("Failed to download PDF")
        return
    
    # Convert PDF to images
    print("Converting PDF pages to images...")
    successful_conversions = convert_pdf_to_images(response.content, lecture_dir)
    
    print(f"\nCompleted! Successfully converted {successful_conversions} PDF pages to images.")

def process_html_presentation(url, lecture_name):
    """Process an HTML presentation by extracting and downloading images."""
    print(f"Processing HTML presentation from: {url}")
    print(f"Lecture: {lecture_name}")
    
    # Create lecture directory
    lecture_dir = create_lecture_directory(lecture_name)
    print(f"Saving images to: {lecture_dir.absolute()}")
    
    # Get page content
    html_content = get_page_content(url)
    if not html_content:
        return
    
    # Extract image URLs
    base_url = url.split('#')[0]  # Remove fragment identifier
    image_urls = extract_image_urls(html_content, base_url)
    
    if not image_urls:
        print("No images found on the page.")
        return
    
    print(f"Found {len(image_urls)} images:")
    for i, img_url in enumerate(image_urls, 1):
        print(f"  {i}. {img_url}")
    
    # Download images
    print("\nDownloading images...")
    successful_downloads = 0
    
    for i, img_url in enumerate(image_urls, 1):
        print(f"Downloading {i}/{len(image_urls)}: ", end="", flush=True)
        if download_image(img_url, lecture_dir, i):
            successful_downloads += 1
        
        # Be respectful to the server
        time.sleep(0.5)
    
    print(f"\nCompleted! Successfully downloaded {successful_downloads}/{len(image_urls)} images.")

def scrape_slide_images(url, lecture_name):
    """Main function to process slides from either HTML presentations or PDF files."""
    if is_pdf_url(url):
        process_pdf_file(url, lecture_name)
    else:
        process_html_presentation(url, lecture_name)

def main():
    """Parse command line arguments and run the scraper."""
    parser = argparse.ArgumentParser(
        description="Download slide images from USC CS572 lecture presentations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python extract.py "https://bytes.usc.edu/cs572/f25-6-AIR/lectures/querying/index.html#(2)" "querying"
  python extract.py "https://bytes.usc.edu/cs572/f25-6-AIR/lectures/SEBasics/SearchEngineBasics.pdf" "se-basics"
  python extract.py "https://example.com/lecture.html" "information-retrieval"
        """
    )
    
    parser.add_argument("url", help="URL of the lecture presentation page")
    parser.add_argument("lecture_name", help="Name of the lecture (will be used as folder name)")
    
    args = parser.parse_args()
    
    # Validate URL
    if not (args.url.startswith('http://') or args.url.startswith('https://')):
        print("Error: URL must start with http:// or https://")
        sys.exit(1)
    
    # Validate lecture name
    if not args.lecture_name.strip():
        print("Error: Lecture name cannot be empty")
        sys.exit(1)
    
    scrape_slide_images(args.url, args.lecture_name)

if __name__ == "__main__":
    main()
