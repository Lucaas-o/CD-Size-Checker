CD Size Checker Development Tasks

[ ] Implement File Size Calculation

Create a function to calculate the size of individual files.
Ensure accurate size reporting in bytes, converting to MB for user output.


[ ] Implement Directory Size Calculation

Develop a recursive function to calculate the total size of all files in a directory.
Handle nested directories correctly.


[ ] Support Multiple CD Sizes

Add support for common CD sizes (e.g., 650MB, 700MB, 800MB).
Allow users to specify custom sizes via command-line argument.


[ ] Create Command-Line Interface (CLI)

Use argparse or click to create a user-friendly CLI.
Support arguments for file/directory paths and CD size.


[ ] Add Error Handling

Handle invalid file paths or inaccessible files.
Warn if total size exceeds CD capacity.
Provide clear error messages for users.


[ ] Write Unit Tests

Test file and directory size calculations.
Test CLI functionality and edge cases (e.g., empty directories, oversized files).


[ ] Add Documentation

Include docstrings for all functions.
Update README.md with detailed usage examples and screenshots (if applicable).


[ ] Optimize Performance

Optimize directory scanning for large file sets.
Consider caching file sizes for repeated checks.


[ ] Add Support for File Type Filtering

Allow users to include/exclude specific file types (e.g., only .mp3 files).
Useful for audio CD preparation.


[ ] Create Sample Usage Guide

Provide a step-by-step guide in README.md.
Include examples for common use cases (e.g., checking music files for an audio CD).
