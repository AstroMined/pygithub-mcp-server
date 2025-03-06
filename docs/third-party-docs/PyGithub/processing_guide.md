# PyGithub Documentation Processing Guide

This guide outlines the process for processing the raw PyGithub documentation that was scraped using the instructions in `scraping_guide.md`.

## Overview

The processing steps involve:
1. Reading the raw scraped markdown files
2. Reformatting the content according to specific rules
3. Saving the processed content back to the files

## Processing Rules

### 1. Breadcrumb Formatting

**IMPORTANT:** Only format the breadcrumb navigation at the top of the page. Do NOT modify any other links in the document.

- Convert the bulleted list breadcrumb to a clean single-line format:

**Original format (usually at the very top of the file):**
```
- »
- [Link](https://pygithub.readthedocs.io/en/stable/page.html) »
- CurrentPage
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/page.rst.txt)
```

**Desired format:**
```
» [Link](../page.md) » CurrentPage  
[View page source](https://pygithub.readthedocs.io/en/stable/page.html)
```

### 2. Convert ONLY Breadcrumb Links

**IMPORTANT:** Only convert links that appear in the breadcrumb navigation at the top of the page. Do NOT modify any other links in the document.

1. Identify links in the breadcrumb in the format `[Link Text](https://pygithub.readthedocs.io/en/stable/path/to/page.html)`
2. Convert only these breadcrumb links to relative links:
   - For pages in the same directory: `[Link Text](page.md)`
   - For pages in parent directories: `[Link Text](../page.md)` or `[Link Text](../../page.md)`
   - For pages in subdirectories: `[Link Text](subdir/page.md)`

### 3. Handle "View page source" Link

**IMPORTANT:** Not all pages will have a "View page source" link. If it doesn't exist, you need to create it.

- If a "View page source" link exists (usually points to a .rst.txt file):
  - Change it to point to the HTML page instead of the .rst.txt file
  - Example: `[View page source](https://pygithub.readthedocs.io/en/stable/page.html)`

- If no "View page source" link exists:
  - Create one using the page's URL
  - Add it after the breadcrumb navigation and before the content
  - Example: `[View page source](https://pygithub.readthedocs.io/en/stable/examples/PullRequest.html)`

### 4. Remove Advertisements

- Remove any advertisement content that might have been scraped (usually at the bottom of the page)
- These often appear as blocks with "Sponsored:", "Ads by...", etc.

## Link Path Calculation Guide (ONLY for Breadcrumb Links)

To calculate the correct relative path for breadcrumb links only, follow these steps:

1. Identify the current file's directory depth in the project structure
2. Identify the target file's location in the project structure
3. Calculate the path to navigate from the current location to the target

### Example Scenarios

If the current file is at:
`examples/PullRequest.md`

And you're linking to a breadcrumb page:
- `examples.md` (parent directory): use `../examples.md`
- `examples/Repository.md` (same directory): use `Repository.md`
- `github_objects/Repository.md` (sibling directory): use `../github_objects/Repository.md`
- `index.md` (root directory): use `../index.md`

### Common URL Patterns and Their Relative Paths (ONLY for Breadcrumb Links)

| URL Pattern | File Location | Relative Path from examples/PullRequest.md |
|-------------|---------------|-----------------------------------------|
| https://pygithub.readthedocs.io/en/stable/examples.html | examples.md | ../examples.md |
| https://pygithub.readthedocs.io/en/stable/examples/Repository.html | examples/Repository.md | Repository.md |
| https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html | github_objects/Repository.md | ../github_objects/Repository.md |
| https://pygithub.readthedocs.io/en/stable/index.html | index.md | ../index.md |

## Processing Examples

### Example Raw Content
```
- »
- [Examples](https://pygithub.readthedocs.io/en/stable/examples.html) »
- PullRequest
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/examples/PullRequest.rst.txt)

* * *

# PullRequest [¶](https://pygithub.readthedocs.io/en/stable/examples/PullRequest.html\#pullrequest "Permalink to this headline")
...
```

### Example Processed Content
```
» [Examples](../examples.md) » PullRequest  
[View page source](https://pygithub.readthedocs.io/en/stable/examples/PullRequest.html)

* * *

# PullRequest [¶](https://pygithub.readthedocs.io/en/stable/examples/PullRequest.html\#pullrequest "Permalink to this headline")
...
```

### Example for Page Without Breadcrumb

If a page doesn't have breadcrumb navigation, leave all links as they are and don't try to format non-existent breadcrumbs.

### Example for Page Without "View page source" Link

If the page doesn't have a "View page source" link, create one using the page's URL and add it at the top of the document:

```
» [Link](../page.md) » CurrentPage  
[View page source](https://pygithub.readthedocs.io/en/stable/page.html)
```

Or if there's no breadcrumb at all, just add:

```
[View page source](https://pygithub.readthedocs.io/en/stable/page.html)
```

## Best Practices

1. Process one file at a time to avoid excessive memory usage
2. Only modify the breadcrumb links and "View page source" link - DO NOT modify any other links
3. If a page doesn't have breadcrumbs, leave it as is except for adding a "View page source" link if needed
4. Use search and replace functionality to efficiently handle repetitive changes

## Troubleshooting

- If relative links aren't working, double-check the directory structure
- Ensure links are properly formatted with parentheses: `[Text](path/to/file.md)`
- For links within the same page (anchor links), leave them unchanged
- Pay special attention to breadcrumb links at the top of each page

## Tracking Processing Progress

To track which files have been processed separately from which have been scraped:

1. Create a copy of the sitemap.md file named processing_status.md:
   ```
   copy E:\code\python-mcp-servers\pygithub-mcp-server\docs\PyGithub\sitemap.md E:\code\python-mcp-servers\pygithub-mcp-server\docs\PyGithub\processing_status.md
   ```

2. Use this new file to track processing progress:
   - Start with all entries as `[ ]` (unchecked)
   - Update to `[x]` after successfully processing a file

3. This allows you to track scraping and processing progress independently

4. After processing a file, always update the processing_status.md file to mark that file as processed
