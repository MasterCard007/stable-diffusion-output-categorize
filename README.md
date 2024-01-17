
# File Metadata Extraction Script

## Overview
This Python script is designed for handling files and extracting their metadata. It is particularly useful for tasks involving batch processing of files and metadata analysis.

## Key Features
- **Metadata Extraction**: Extracts metadata from files using `exiftool`.
- **Parallel Processing**: Utilizes `ThreadPoolExecutor` for efficient processing of multiple files concurrently.
- **Environment Setup**: Sets up the necessary environment variables for consistent metadata extraction.

## Dependencies
- Python 3.x
- Libraries: `os`, `shutil`, `json`, `subprocess`
- `exiftool`: External tool required for metadata extraction.

## Installation
Ensure that Python 3.x is installed on your system along with the necessary libraries. Additionally, `exiftool` needs to be installed and accessible in the system's PATH.

## Usage
To use this script, you need to provide the file paths for which you want to extract metadata. The script processes these files and outputs their metadata. Example usage is as follows:

```python
import model_res

# Example file paths
file_paths = ["path/to/file1", "path/to/file2"]

# Get metadata
metadata = model_res.get_metadata(file_paths)
```

Note: This README is based on a partial view of the script. For more detailed information, please refer to the script itself.
