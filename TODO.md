# TODO.md - CD Size Checker Development Tasks

## ✅ Completed Tasks

### Implement File & Directory Size Calculation
- `get_directory_size()` renamed to `get_path_size()` to handle both files and directories.
- Supports individual files using `os.path.isfile()`.
- Recursive size calculation using `os.walk()`.

### Support Multiple CD Sizes
- `--cd-size` flag added with default 700MB.
- Predefined sizes added: 650MB, 700MB, 800MB, miniCD, businessCard using `argparse` choices via `CD_PRESETS`.

### Create Command-Line Interface (CLI)
- CLI implemented using `argparse` with `paths` and `--cd-size` arguments.
- Note: `click` was considered but not used; listed in `requirements.txt` as unused.

### Add Error Handling
- Handled invalid directories and inaccessible files.
- Symbolic links ignored (`followlinks=False` in `os.walk()`).
- Handled permission errors with `try-except`.
- Validated `--cd-size` to ensure it's positive.

### Add Documentation
- Docstrings added to all functions (`get_path_size()`, `check_cd_fit()`, `main()`).
- `README.md` updated with usage examples, argument descriptions, and outputs.

### Add Support for File Type Filtering
- `--extensions` argument added to filter specific file types (e.g., `--extensions mp3,wav`).
- Uses string methods for extension matching.

### Create Sample Usage Guide
- Step-by-step usage guide added to `README.md` for checking music files, single files, and multiple paths.

### Enhance Output Details
- Output includes number of files, largest file (with path and size), and remaining CD space in `check_cd_fit()`.

### Add Verbose Mode
- `--verbose` flag added to show file-by-file processing details.
- Uses `tqdm.write()` to avoid cluttering the progress bar.

### Support Multiple Directories/Files
- `argparse` updated to accept multiple paths using `nargs='*'`.
- Processes each path sequentially with separated outputs.

### Improve Interactive Mode
- Automatically proceeds to the next step after entering one valid path.
- Feedback message: “Added: {path}”.

## 🔧 Remaining Tasks

### Write Unit Tests
- Tests planned for `get_path_size()` and `check_cd_fit()`.
- Should include cases like empty directories, single files, permission errors.
- Use `unittest` or `pytest` with temporary files.
- Not yet implemented due to complexity and file handling needs.

### Optimize Performance
- Consider using `multiprocessing` for large directories.
- `tqdm` used for user feedback, but not actual speed improvements.

## 💡 Proposed Features

### Add Exclusion Patterns
- Option: `--exclude` to skip files/directories (e.g., `*.log`, `temp/`).

### Add Output to File
- Option: `--output file.txt` to save results for later review.
