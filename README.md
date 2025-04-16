# CD Size Checker

## Installation

Clone the repository:
```bash
git clone https://github.com/Lucaas-o/CD-Size-Checker.git
```

Navigate to the project directory:
```bash
cd cd_size_checker
```

Install dependencies (if any):
```bash
pip install -r requirements.txt
```

## Usage

Run the script from the command line to check if files fit on a CD. Example:
```bash
python cd_size_checker.py /path/to/files --cd-size 700
```

- `--cd-size`: Specify the CD capacity in MB (default: 700).

The script will output whether the files fit and display the total size.

## Dependencies

- Python 3.6+
- Standard libraries: `os`, `sys`
- Optional: `click` for enhanced CLI functionality (install via `pip install click`)

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Author

[Lucaas-o]
