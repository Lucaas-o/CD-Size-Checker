# CD Size Checker

A command-line tool to check if files or directories fit on a CD of a specified size.

## Features

- Supports both files and directories.
- Allows predefined CD sizes or custom sizes.
- Filters files by extensions (e.g., mp3, wav).
- Provides detailed output including total size, number of files, largest file, and remaining CD space.
- Supports verbose mode for detailed processing logs.
- Can check multiple paths in a single run.

## Installation

1. Clone this repository.
2. Ensure Python is installed (version 3.6+).
3. Run the script using Python.

## Usage

### Checking a single directory

```bash
python main.py /path/to/directory --preset-size 700MB
```

### Checking a single file

```bash
python main.py /path/to/file.txt --cd-size 730.5
```

### Checking multiple paths

```bash
python main.py dir1 dir2 file1.txt --preset-size 800MB
```

### Filtering by file extensions

```bash
python main.py /path/to/directory --extensions mp3,wav --verbose
```

### Verbose mode

Add `--verbose` to see detailed processing of each file.

```bash
python main.py /path/to/directory --verbose
```

### Combining options

```bash
python main.py /path/to/directory --preset-size 700MB --extensions mp3 --verbose
```

## Command-Line Arguments

- `paths`: One or more paths to files or directories to check.
- `--cd-size`: Custom CD size in MB (e.g., `730.5`). Overrides `--preset-size`.
- `--preset-size`: Choose from common CD sizes (default: `700MB`).
- `--extensions`: Comma-separated list of file extensions to include (e.g., `mp3,wav`).
- `--verbose`: Show detailed output during processing.

## Example Output

### For a directory:

```
Checking /path/to/directory:
Total size: 650.00 MB (100 files)
Largest file: /path/to/largest/file.mp3 (100.00 MB)
CD capacity: 700.0 MB
Files fit on the CD! Remaining space: 50.00 MB
```

### For a single file:

```
Checking /path/to/file.txt:
Total size: 100.00 MB (1 files)
Largest file: /path/to/file.txt (100.00 MB)
CD capacity: 700.0 MB
Files fit on the CD! Remaining space: 600.00 MB
```

## Notes

- If no files match the specified extensions, the total size will be 0.
- Symbolic links are not followed for directories (default behavior of `os.walk()`).
- Permission errors or inaccessible files are skipped with warnings.
- CD size must be positive; otherwise, an error is displayed.
