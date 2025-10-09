#!/usr/bin/env python3
"""
Slide Image Scraper
Downloads all slide images from a USC CS572 lecture presentation.

Usage:
    python extract.py <URL> <LECTURE_NAME>
    
Example:
    python extract.py "https://bytes.usc.edu/cs572/f25-6-AIR/lectures/querying/index.html#(2)" "querying"
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

def get_page_content(url):
    """Fetch the HTML content from the given URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
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

def scrape_slide_images(url, lecture_name):
    """Main function to scrape all slide images from the presentation."""
    print(f"Scraping images from: {url}")
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

def main():
    """Parse command line arguments and run the scraper."""
    parser = argparse.ArgumentParser(
        description="Download slide images from USC CS572 lecture presentations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python extract.py "https://bytes.usc.edu/cs572/f25-6-AIR/lectures/querying/index.html#(2)" "querying"
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
