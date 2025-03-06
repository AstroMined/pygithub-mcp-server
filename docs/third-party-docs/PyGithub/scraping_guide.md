# PyGithub Documentation Scraping Guide

This guide outlines the process for scraping the PyGithub documentation from ReadTheDocs and saving the raw content for later processing.

## Overview

The scraping process involves:
1. Reading the sitemap.md file to identify pages that haven't been scraped yet
2. Using FireCrawl to scrape the content from ReadTheDocs
3. Saving the raw scraped content to the appropriate local file path
4. Updating the sitemap.md to mark the page as scraped

## Detailed Process

### 1. Identifying Pages to Scrape

- Read the `sitemap.md` file located at `E:\code\python-mcp-servers\pygithub-mcp-server\docs\PyGithub\sitemap.md`
- Look for entries with empty checkboxes `[ ]` - these are pages that haven't been scraped yet
- Each entry follows this format: `[ ] [relative/path/to/file.md](https://pygithub.readthedocs.io/en/stable/path/to/page.html)`

### 2. Scraping Content

Use FireCrawl to scrape the content with these settings:
- URL: The URL in parentheses from the sitemap entry
- Format: "markdown"
- Exclude Tags: "readthedocs-ea" (to avoid scraping ads)
- Only Main Content: true

### 3. Saving Raw Content

1. Determine the correct file path from the sitemap entry (the part in square brackets)
2. Convert forward slashes to backslashes for Windows compatibility
3. Create any necessary directories if they don't exist
4. Save the raw scraped content to the file without processing

### 4. Updating the Sitemap

Update the sitemap.md file to mark the page as scraped:
- Change `[ ] [path/to/file.md](url)` to `[x] [path/to/file.md](url)`

## Examples

### Example Sitemap Entry
```
[ ] [examples/PullRequest.md](https://pygithub.readthedocs.io/en/stable/examples/PullRequest.html)
```

### Example Save Path
```
E:\code\python-mcp-servers\pygithub-mcp-server\docs\PyGithub\examples\PullRequest.md
```

## Troubleshooting

- If directories don't exist, create them before writing files
- Be careful with path separators (use backslashes for Windows paths)
- When editing the sitemap, make sure to match the exact line to be replaced

## Progress Tracking

The sitemap.md file serves as a progress tracker:
- `[ ]` indicates a page that hasn't been scraped yet
- `[x]` indicates a page that has been successfully scraped

## Next Steps

After scraping, the content will need to be processed according to the rules in `processing_guide.md`.
