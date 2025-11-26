# Simple Amazon Scraper API

Simple API for scraping websites using Selenium and BeautifulSoup.

## Installation

```bash
pip install -r requirements.txt
```

## Running

1. Make sure Chrome is running with debugging on port 10192
2. Start the API:

```bash
python app.py
```

## Endpoints

### GET /search?keyword=

Searches for a keyword in Google and returns results.

Example:

```bash
curl "http://localhost:5000/search?keyword=python"
```

### GET /product?url=

Retrieves product/page information from the given URL.

Example:

```bash
curl "http://localhost:5000/product?url=https://example.com"
```

### GET /health

Checks API status.

Example:

```bash
curl "http://localhost:5000/health"
```

## Configuration

Edit `config.py` to change:

-   Chrome port (CHROME_DEBUG_PORT)
-   API host and port (API_HOST, API_PORT)
-   Timeouts and delays
