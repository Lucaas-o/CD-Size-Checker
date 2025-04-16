Updated TODO.md
CD Size Checker Development Tasks

 
Implement File Size Calculation

Created get_directory_size() to calculate file sizes (for directories).
Remaining: Extend to handle individual files (check os.path.isfile()).


 
Implement Directory Size Calculation

Implemented recursive directory size calculation using os.walk() in get_directory_size().


 
Support Multiple CD Sizes

Added --cd-size flag with default 700MB.
Remaining: Add predefined options (e.g., 650MB, 700MB, 800MB) using argparse choices or validation.


 
Create Command-Line Interface (CLI)

Implemented CLI using argparse with directory and --cd-size arguments.
Remaining: Consider switching to click for enhanced CLI features (requires updating requirements.txt).


 
Add Error Handling

Basic handling for invalid directories and inaccessible files.
Remaining: Handle symbolic links, permission errors, and validate --cd-size (e.g., must be positive).


 
Write Unit Tests

Test get_directory_size() and check_cd_fit() for various cases (e.g., empty directories, single files, errors).
Use unittest or pytest with temporary files/directories.


 
Add Documentation

Add detailed docstrings for all functions in main.py.
Update README.md with detailed usage examples and screenshots.


 
Optimize Performance

Optimize directory scanning for large file sets (e.g., use tqdm for progress bar or multiprocessing).
Consider caching file sizes for repeated checks.


 
Add Support for File Type Filtering

Allow users to include/exclude specific file types (e.g., --extensions mp3,wav).
Use os.path.splitext() or fnmatch for filtering.


 
Create Sample Usage Guide

Provide a step-by-step guide in README.md.
Include examples for common use cases (e.g., checking music files for an audio CD).


 
Enhance Output Details

Show additional stats (e.g., number of files, largest file, remaining CD space).
Calculate and display in check_cd_fit().


 
Add Verbose Mode

Add --verbose flag to show file-by-file sizes during scanning.
Implement in get_directory_size() with conditional printing.


 
Support Multiple Directories/Files

Allow checking multiple paths (e.g., python main.py dir1 dir2 file1.txt).
Update argparse to accept multiple arguments (nargs='+').



