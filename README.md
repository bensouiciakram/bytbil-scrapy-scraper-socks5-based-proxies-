# Scrapy Car Data Extractor

This project is a Scrapy-based web scraper that extracts car make and model information, as well as detailed car listings, from `https://www.bytbil.com/`. It supports proxy usage and integrates with PocketBase for database storage.

## Features
- Scrapes car makes and models.
- Extracts detailed car listing data.
- Supports **SOCKS5 proxies** for anonymous scraping.
- Stores data using **PocketBase**.
- Modular and extendable code structure.

## Installation

### Prerequisites
- **Python 3.x** installed
- **pip** (or pip3 for macOS)
- **Git** (for dependency installation)
- Optional: **PocketBase** (for database integration)

### Install Dependencies
On **Windows**, double-click `install_requirements.bat`.  
On **Linux/macOS**, run:
```bash
pip install -r requirements.txt
# For macOS, use: pip3 install -r requirements.txt
```

## Usage
### 1. Adding Proxies
Add your SOCKS5 proxies to proxies.txt, one per line.
### 2. Running the Scraper
To extract only car makes and models:

```bash
python main.py makes_models
```

To extract detailed car information:

```bash
python main.py cars
```

## PocketBase Integration

1. Place pocketbase.exe inside the db/ directory.
2. Start the database server:
```bash
db/pocketbase serve
```
3. Open your browser and visit http://127.0.0.1:8090/_/, then register a new user.
4. Add your PocketBase credentials to utils/pipelines.py (lines 26, 27).
5. Run the scraper as described above.

## Dependencies
This project requires the following Python libraries:
```bash
scrapy
git+https://github.com/russian-developer/txsocksx.git
loguru
requests
pocketbase
```
All dependencies are listed in requirements.txt.


