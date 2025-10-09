# Slide Scraper

A Python script to download slide images from USC CS572 lecture presentations.

## What it does

This script automatically downloads all slide images from a lecture webpage and organizes them into folders by lecture name.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

Install dependencies:
```bash
pip install requests beautifulsoup4
```

## Usage

```bash
python extract.py <URL> <LECTURE_NAME>
```

### Example

```bash
python extract.py "https://bytes.usc.edu/cs572/f25-6-AIR/lectures/querying/index.html#(2)" "querying"
```

This will:
1. Download all images from the querying lecture page
2. Create a folder `slides/querying/`
3. Save all 52 slide images in that folder

## Output

The script creates the following structure:
```
slides/
└── querying/
    ├── s1.png
    ├── s2.png
    ├── s3.png
    └── ... (all slide images)
```

Each lecture gets its own subfolder within the `slides` directory.