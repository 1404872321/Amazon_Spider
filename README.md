# Amazon_Spider

An Amazon seller info crawler with multithreading, rotating User-Agent, and optional proxy support. Refactored into a reusable Python package and CLI.

## Features
- Multithreaded crawling with configurable workers
- Rotating User-Agent per request
- Optional HTTP/HTTPS/SOCKS proxy support
- Robust retries with backoff for 429/5xx responses
- Defensive HTML parsing for seller name, time-window ratings, and histogram percentages
- Read URLs from Excel/CSV; write results to Excel/CSV/JSON

## Installation
```bash
pip install -r requirements.txt
```

## Usage
Prepare an input file with a column containing seller profile URLs (default column name: `url`). For Excel, you can specify a `--sheet-name`.

```bash
python cli.py crawl \
  --input-file ./input.xlsx \
  --sheet-name "Sheet1" \
  --column url \
  --output-file ./output.xlsx \
  --max-workers 20 \
  --timeout 30 \
  --max-retries 3 \
  --backoff 0.5 \
  --socks-proxy socks5h://127.0.0.1:8443
```

You can also use `--http-proxy` or `--https-proxy`. If not provided, environment variables `HTTP_PROXY`, `HTTPS_PROXY`, or `SOCKS_PROXY` will be used when set.

## Notes
- Amazon actively employs anti-bot protections. Use responsible crawling settings and respect the website's terms.
- Selectors may require adjustments if Amazon updates their markup.
- The original notebook `amazon_seller_crawl.ipynb` remains in the repo but the recommended entrypoint is the CLI above.
